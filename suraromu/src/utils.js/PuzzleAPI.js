

const puzzles = [
    {
        rows: 10,
        cols: 10,
        startCell: [1, 2],
        blockedCells: [[4,3], [5,6], [0,0]],
        gates: {
            1: {orientation: "h", 
                length: 2,
                startCell: [3, 2]}, 
            3: {orientation: "v", 
                length: 2,
                startCell: [6, 3]},  
            0: [{orientation: "h", 
                    length: 1,
                    startCell: [7, 7]}]
        } 

    },

    {
        rows: 20,
        cols: 10,
        startCell: [1, 2],
        blockedCells: [[4,3], [5,6], [0,0]],
        gates: {
            4: {orientation: "h", 
                length: 2,
                startCell: [3, 8]}, 
            5: {orientation: "v", 
                length: 2,
                startCell: [6, 6]},  
            0: [{orientation: "h", 
                    length: 1,
                    startCell: [9, 7]}]
        } 

    },

    {
        rows: 10,
        cols: 20,
        startCell: [1, 2],
        blockedCells: [[4,3], [5,6], [0,0]],
        gates: {
            8: {orientation: "h", 
                length: 2,
                startCell: [3, 2]}, 
            9: {orientation: "v", 
                length: 2,
                startCell: [6, 6]},  
            0: [{orientation: "h", 
                    length: 1,
                    startCell: [7, 7]}]
        } 

    },

]

export default function getRandomPuzzle() {
    return puzzles[Math.floor(Math.random() * puzzles.length)]
}


export default function getPuzzles(difficulty, size) {

    let sortedPuzzles = []
    if (difficulty === 'easy'){
        let unsortedPuzzles = puzzles['0'].concat(puzzles['1'])
        sortedPuzzles = unsortedPuzzles.sort((a, b) => (a.rows * a.cols) - (b.rows * b.cols));
    }
    else if (difficulty === 'medium'){
        let unsortedPuzzles = puzzles['2'].concat(puzzles['3'])
        sortedPuzzles = unsortedPuzzles.sort((a, b) => (a.rows * a.cols) - (b.rows * b.cols));
    }
    else if (difficulty === 'hard'){
        let unsortedPuzzles = puzzles['4'].concat(puzzles['5'], puzzles['6'], puzzles['8'])
        sortedPuzzles = unsortedPuzzles.sort((a, b) => (a.rows * a.cols) - (b.rows * b.cols));
    }

    const partSize = Math.ceil(sortedPuzzles.length / 3);

    if (size === 'small') return sortedPuzzles.slice(0, partSize);
    if (size === 'medium') return sortedPuzzles.slice(partSize, partSize * 2);
    if (size === 'big') return sortedPuzzles.slice(partSize * 2);

    return []
}

