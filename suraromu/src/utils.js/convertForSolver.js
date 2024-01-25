export default function getSolverPuzzle(puzzle) {
    let blockedCells = [...puzzle.blockedCells]
    let rows = puzzle.rows
    let cols = puzzle.cols
    let startIndex = puzzle.startCell
    
    // gate needs to be traversed vertical so it is a horizontal dotted line and in the website denotet as "h"
    let gcv = {}
    // gate needs to be traversed horizontal so it is a vertical dotted line and in the website denotet as "v"
    let gch = {}

    for (let number in puzzle.gates) {
        if (puzzle.gates.hasOwnProperty(number)) {

            if (number === "0") {
                // unordered gates
                let negativeNumber = -1
                let unorderedGates = puzzle.gates[number]
                for (const gate of unorderedGates){
                    addGate(gate, negativeNumber, gch, gcv, blockedCells, rows, cols)
                    negativeNumber = negativeNumber - 1
                }

            }else{
                // ordered gates
                addGate(puzzle.gates[number], number, gch, gcv, blockedCells, rows, cols)
            }

        }
    }

    return {
        blockedCells: blockedCells,
        rows: rows,
        cols: cols,
        startIndex: startIndex,
        gcv: gcv,
        gch: gch
    }
}

function addGate(gate, index, gch, gcv, blockedCells, rows, cols){
    let startCell = gate.startCell
    let len = gate.length
    let orient = gate.orientation

    let cells = []
    let direction = orient === "v" ? [1, 0] : [0, 1]

    let blockedIndex1 = [startCell[0] - 1 * direction[0], startCell[1] - 1 * direction[1]]
    let blockedIndex2 = [startCell[0] + len * direction[0], startCell[1] + len * direction[1]]

    if (blockedIndex1[0] >= 0 && blockedIndex1[1] >= 0) {
        blockedCells.push(blockedIndex1)
    }

    if (blockedIndex2[0] < rows && blockedIndex2[1] < cols) {
        blockedCells.push(blockedIndex2)
    } 

    for (let i = 0; i < len; i++) {
        let index = [startCell[0] + i * direction[0], startCell[1] + i * direction[1]];
        cells.push(index);
    }

    if (orient === "v"){
        gch[index] = cells
    }else{
        gcv[index] = cells
    }

}