import './App.css';
import Board from './components/Board';
import { useState, useEffect} from 'react';
import GameInfo from './components/GameInfo';
import Controls from './components/Controls';
import Toolbar from './components/Toolbar';

function App() {

  const createInitialArray = (rows, cols) => {
    const newArray = [];
    for (let i = 0; i < rows; i++) {
      newArray.push(new Array(cols).fill(0));
    }
    return newArray;
  };

  const [toolType, setToolType] = useState(1);

  const [puzzle, setPuzzle] = useState({
    rows: 10,
    cols: 10,
    arrayHori: createInitialArray(10, 9),
    arrayVert: createInitialArray(9, 10),
    startCell: [0, 0],
    blockedCells: [],
    gates: {
    } 
  });

  useEffect(() => {
    if(shouldTrack){
      console.log("puzzle:", puzzle);
      setHistory((prevHistory) => [...prevHistory, structuredClone(puzzle)]);
    }else{
      setShouldTrack(true)
    }

  }, [puzzle]);
  

  const [history, setHistory] = useState([structuredClone(puzzle)]);
  const [shouldTrack, setShouldTrack] = useState(true);
  
  function blockLine(row, col, arr){
    if (row >= 0 && row < arr.length && col >= 0 && col < arr[row].length) {
      arr[row][col] = -1;
    }
  }

  function getBlockedGateCells(gate) {
    const cells = []
    const row = gate.startCell[0]
    const col = gate.startCell[1]

    if(gate.orientation === "h") {
        cells.push([row, col-1])
        cells.push([row, col+gate.length])
    }else {
        cells.push([row-1, col])
        cells.push([row+gate.length, col])
    }

    return cells
  }

  function setNewPuzzle(newPuzzle) {
  
    const newArrayHori = createInitialArray(newPuzzle.rows, newPuzzle.cols - 1);
    const newArrayVert = createInitialArray(newPuzzle.rows - 1, newPuzzle.cols);
  
    // set the blocked lines from the blockedCells
    for (let blockedCell of newPuzzle.blockedCells){

      let row = blockedCell[0]
      let col = blockedCell[1]
      blockLine(row, col-1, newArrayHori)
      blockLine(row, col, newArrayHori)
      blockLine(row-1, col, newArrayVert)
      blockLine(row, col, newArrayVert)
    }

    // set the blocked lines from the gateCells
    for (let key in newPuzzle.gates) {
      if (key === '0') {
        // all the unordered gates
        for (let gateKey in newPuzzle.gates[key]) {
          const possibleGateCells = getBlockedGateCells(newPuzzle.gates[key][gateKey])
          for (let idx in possibleGateCells){
            let row = possibleGateCells[idx][0]
            let col = possibleGateCells[idx][1]
            
            blockLine(row, col-1, newArrayHori)
            blockLine(row, col, newArrayHori)
            blockLine(row-1, col, newArrayVert)
            blockLine(row, col, newArrayVert)
          }
        }
      } else {
        // all the ordered cells
        const possibleGateCells = getBlockedGateCells(newPuzzle.gates[key])
        
        for (let idx in possibleGateCells){
          let row = possibleGateCells[idx][0]
          let col = possibleGateCells[idx][1]
          blockLine(row, col-1, newArrayHori)
          blockLine(row, col, newArrayHori)
          blockLine(row-1, col, newArrayVert)
          blockLine(row, col, newArrayVert)
        }
      }
    }

    setPuzzle({
      ...newPuzzle,
      arrayHori: newArrayHori,
      arrayVert: newArrayVert
      }
    );
  
  }

  function clearArray(array) {
    for (let i = 0; i < array.length; i++) {
      const row = array[i];
      for (let j = 0; j < row.length; j++) {
        const cell = row[j];
        if (cell !== -1) {
          array[i][j] = 0;
        }
      }
    }
    return array;
  }

  function deleteConnections(){
    setPuzzle((prevState) => {
      const arrayHoriNew = clearArray(prevState.arrayHori)
      const arrayVertNew = clearArray(prevState.arrayVert)
      return ({
      ...prevState,
      arrayHori: arrayHoriNew,
      arrayVert: arrayVertNew,
    })});
  }

  return (
    <>
      <div className="App">
        <header className="App-header">
          <h1 style={{ marginBottom: '0' }}>
            スラローム
          </h1>
          <p style={{ marginTop: '0', fontSize: "1.3rem"}}>
            Suraromu
          </p>
        </header>

        
        
        <Controls deleteFunction={deleteConnections} setNewPuzzle={setNewPuzzle} setPuzzle={setPuzzle} setHistory={setHistory} history={history} puzzle={puzzle} setShouldTrack={setShouldTrack} createInitialArray={createInitialArray}/>
        <Toolbar toolType={toolType} setToolType={setToolType}/>
        <Board puzzle={puzzle} setPuzzle={setPuzzle} setHistory={setHistory} history={history} toolType={toolType}/>
        
        <GameInfo/>
      </div>
    </>


  );
}


export default App;