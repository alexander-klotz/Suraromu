
// TODO: maybe change this so we specify not only start, orientation, and length of gate
// TODO: also maybe change the way all other gates are saved in 0.   
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
                startCell: [3, 2]}, 
            5: {orientation: "v", 
                length: 2,
                startCell: [6, 6]},  
            0: [{orientation: "h", 
                    length: 1,
                    startCell: [7, 7]}]
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

