# Backend
from fastapi import FastAPI, WebSocket, BackgroundTasks
from time import sleep
from fastapi.middleware.cors import CORSMiddleware
from solver import SuraromuSolver
import json

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        
        if data != "stop":
            await websocket.send_text("Calculation started")
            data = json.loads(data)
            data = convertToTuple(data)
            # TODO: maybe use multiprocessing to achieve the option to stop the calculation
            solver = SuraromuSolver(data["rows"], data["cols"], data["startIndex"], data["gcv"], data["gch"], data["blockedCells"])
            solution = solver.solvePuzzle()
            print(solution)
            await websocket.send_text(json.dumps(solution))
        elif data == "stop":
            await websocket.send_text("Calculation stopped")
            await websocket.close()


def convertToTuple(data):
    if isinstance(data, list) and all(isinstance(i, int) for i in data):
        return tuple(data)
    elif isinstance(data, list):
        return [convertToTuple(i) for i in data]
    elif isinstance(data, dict):
        return {int(k) if k.lstrip('-').isdigit() else k: convertToTuple(v) for k, v in data.items()}
    else:
        return data