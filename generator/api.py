from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from generator import Generator
import json
import random
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

def generate(generator, genPuzzle):
    triesCounter = 1
    maxTries = 5
    while triesCounter <= maxTries:
        rows, cols, startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, solution = generator.generate(triesCounter)
        if rows != None:
            print("DONE UNIQUE PUZZLE FOUND after ", triesCounter, "tries")
            returnValue = convertPuzzleForWeb(rows, cols, startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, solution)
            break
        triesCounter += 1
    genPuzzle.value = returnValue

def generateRandomSize(s):
    if s == 'small':
        return random.randint(8, 12), random.randint(8, 12)
    elif s == 'medium':
        return random.randint(12, 17), random.randint(12, 17)
    elif s == 'big':
        return random.randint(17, 25), random.randint(17, 25)
    else:
        return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    manager = multiprocessing.Manager()
    genPuzzle = manager.Value(object, None)


    p = None
    while True:
        try:
            data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
            
            if data != "abort":
                await websocket.send_text("starting generation")
                genPuzzle.value = None

                data = json.loads(data)
                data = convertToTuple(data)

                randRows, randCols = generateRandomSize(data["size"])
                generator = Generator(randRows, randCols, data["difficulty"])
                p = multiprocessing.Process(target=generate, args=(generator, genPuzzle))
                p.start()
                
            elif data == "abort":
                if p is not None and p.is_alive():
                    p.terminate()  # Terminate the process
                    print("terminated process")
                await websocket.send_text("Generation stopped")

        except asyncio.TimeoutError:
            if p != None and not p.is_alive() and genPuzzle.value != None:
                p = None
                await websocket.send_text(json.dumps(genPuzzle.value, default=int))
            continue  # No message received, continue to the next iteration



def convertPuzzleForWeb(rows, cols, startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, solution):
    puzzle = {
        "author": "generator by A.K.",
        "solver": "SAT solver",
        "rows": rows,
        "cols": cols,
        "blockedCells": [],
        "startCell": [int(startIndex[0]), int(startIndex[1])],
        "gates": {
        },
        "solution": solution
    }

    blockedCells = [list(tup) for tup in blockedCells]

    unorderedGates = []
    
    # webpage and solver have a different notion of gate orientation
    for horizontalGateKey in convertedVerticalSolverGates:
        gate = convertedVerticalSolverGates[horizontalGateKey]
        startCell = min(gate, key=sum)
        gateLength = len(gate)
        if horizontalGateKey < 0:
            
            newGate = {"orientation": "h", "startCell": [startCell[0], startCell[1]], "length": gateLength}
            unorderedGates.append(newGate)
        else:
            puzzle["gates"][str(horizontalGateKey)] = {"orientation": "h", "startCell": [startCell[0], startCell[1]], "length": gateLength}
            if [startCell[0], startCell[1] - 1] in blockedCells:
                blockedCells.remove([startCell[0], startCell[1] - 1])
            if [startCell[0], startCell[1] + gateLength] in blockedCells:
                blockedCells.remove([startCell[0], startCell[1] + gateLength])


    for verticalGateKey in convertedHorizontalSolverGates:
        gate = convertedHorizontalSolverGates[verticalGateKey]
        startCell = min(gate, key=sum)
        gateLength = len(gate)
        if verticalGateKey < 0:
            newGate = {"orientation": "v", "startCell": [startCell[0], startCell[1]], "length": gateLength}
            unorderedGates.append(newGate)
        else:
            puzzle["gates"][str(verticalGateKey)] = {"orientation": "v", "startCell": [startCell[0], startCell[1]], "length": gateLength}
            if [startCell[0] - 1, startCell[1]] in blockedCells:
                blockedCells.remove([startCell[0] - 1, startCell[1]])
            if [startCell[0] + gateLength, startCell[1]] in blockedCells:
                blockedCells.remove([startCell[0] + gateLength, startCell[1]])


    puzzle["gates"]["0"] = unorderedGates
    puzzle["blockedCells"] = blockedCells

    return puzzle


def convertToTuple(data):
    if isinstance(data, list) and all(isinstance(i, int) for i in data):
        return tuple(data)
    elif isinstance(data, list):
        return [convertToTuple(i) for i in data]
    elif isinstance(data, dict):
        return {int(k) if k.lstrip('-').isdigit() else k: convertToTuple(v) for k, v in data.items()}
    else:
        return data