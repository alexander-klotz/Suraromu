from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from solver import SuraromuSolver
import json
import multiprocessing
import asyncio

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def solve(solver, solutions):
    returnValue = solver.solvePuzzle()
    solutions.value = returnValue

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    manager = multiprocessing.Manager()
    solutions = manager.Value(object, None)

    p = None
    while True:
        try:
            data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
            
            if data != "abort":
                await websocket.send_text("Calculation started")
                solutions.value = None
                data = json.loads(data)
                data = convertToTuple(data)
                print("Started solving")
                solver = SuraromuSolver(data["rows"], data["cols"], data["startIndex"], data["gcv"], data["gch"], data["blockedCells"])
                
                p = multiprocessing.Process(target=solve, args=(solver, solutions))
                p.start()
                
            elif data == "abort":
                if p is not None and p.is_alive():
                    p.terminate()  # Terminate the process
                    print("terminated process", flush=True)
                await websocket.send_text("Calculation stopped")



        except asyncio.TimeoutError:
            if p != None and not p.is_alive() and solutions.value != None:
                p = None
                print("DONE SOLUTION FOUND", flush=True)
                await websocket.send_text(json.dumps(solutions.value))
                solutions.value = None
            continue  # No message received, continue to the next iteration

        
            

def convertToTuple(data):
    if isinstance(data, list) and all(isinstance(i, int) for i in data):
        return tuple(data)
    elif isinstance(data, list):
        return [convertToTuple(i) for i in data]
    elif isinstance(data, dict):
        return {int(k) if k.lstrip('-').isdigit() else k: convertToTuple(v) for k, v in data.items()}
    else:
        return data