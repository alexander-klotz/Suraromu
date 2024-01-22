# Backend
from fastapi import FastAPI, WebSocket, BackgroundTasks
from time import sleep
from fastapi.middleware.cors import CORSMiddleware
from generator import Generator
import json
import random

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


def generateRandomInteger(s):
    if s == 'small':
        return random.randint(10, 15), random.randint(10, 15)
    elif s == 'medium':
        return random.randint(15, 20), random.randint(15, 20)
    elif s == 'big':
        return random.randint(21, 35), random.randint(21, 35)
    else:
        return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    
    triesCounter = 1
    maxTries = 10
    while triesCounter <= maxTries:

        # TODO: currently we get stuck here if we are on the second iteration we need to change the control flow to fix this
        data = await websocket.receive_text()

        if data != "stop":
            await websocket.send_text("starting generation")
            
            data = json.loads(data)
            data = convertToTuple(data)

            randRows, randCols = generateRandomInteger(data["size"])


            test = Generator(randRows, randCols, data["difficulty"])
            rows, cols, startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, solution = test.generate(triesCounter)
            if rows != None:
                print("DONE UNIQUE PUZZLE FOUND after ", triesCounter, "iterations")
                puzzle = convertPuzzleForWeb(rows, cols, startIndex, convertedVerticalSolverGates, convertedHorizontalSolverGates, blockedCells, solution)
        

                await websocket.send_text(json.dumps(puzzle, default=int))
                await websocket.send_text("generation finished")
                
            else:
                await websocket.send_text(f"attempt Nr. {triesCounter} out of {maxTries} failed")
            triesCounter += 1

        elif data == "stop":
            await websocket.send_text("generation stopped")
            await websocket.close()


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
        "solution": [
            # ... add the rest of your solution here ...
        ]
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

    # TODO: convert the gates to the webpage gates

    # TODO: add the solution from the solver
    print(puzzle)
    return puzzle


def convert_int64_values(data):
    if isinstance(data, dict):
        return {k: convert_int64_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_int64_values(v) for v in data]
    else:
        print(data, type(data))
        return data

def convertToTuple(data):
    if isinstance(data, list) and all(isinstance(i, int) for i in data):
        return tuple(data)
    elif isinstance(data, list):
        return [convertToTuple(i) for i in data]
    elif isinstance(data, dict):
        return {int(k) if k.lstrip('-').isdigit() else k: convertToTuple(v) for k, v in data.items()}
    else:
        return data