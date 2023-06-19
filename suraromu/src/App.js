import './App.css';
import Board from './components/Board';
import { useState } from 'react';
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
    startCell: [1, 2],
    blockedCells: [[4,3], [5,6], [0,0]],
    gates: {
        1: {orientation: "h", 
            length: 2,
            startCell: [3, 2]}, 
        3: {orientation: "v", 
            length: 2,
            startCell: [5, 3]},  
        0: [{orientation: "h", 
                length: 1,
                startCell: [7, 7]}]
    } 
  });

  const [history, setHistory] = useState([structuredClone(puzzle)]);


  function setNewPuzzle(newPuzzle) {
  
    const newArrayHori = createInitialArray(newPuzzle.rows, newPuzzle.cols - 1);
    const newArrayVert = createInitialArray(newPuzzle.rows - 1, newPuzzle.cols);

    setPuzzle({
      ...newPuzzle,
      arrayHori: newArrayHori,
      arrayVert: newArrayVert
      }
    );


    setHistory((prevHistory) => [...prevHistory, structuredClone(puzzle)]);
  
  }


  function deleteConnections(){
    setPuzzle((prevState) => ({
      ...prevState,
      arrayHori: createInitialArray(prevState.rows, prevState.cols-1),
      arrayVert: createInitialArray(prevState.rows-1, prevState.cols)
    }));

    setHistory((prevHistory) => [...prevHistory, structuredClone(puzzle)]);
  }

  return (
    <>
      <div className="App">
        <header className="App-header">
          <h1>
            スラローム
          </h1>
          <p>
            Suraromu
          </p>
        </header>

        



        <Toolbar toolType={toolType} setToolType={setToolType}/>
        <Controls deleteFunction={deleteConnections} setNewPuzzle={setNewPuzzle} setPuzzle={setPuzzle} setHistory={setHistory} history={history}/>
        <Board puzzle={puzzle} setPuzzle={setPuzzle} setHistory={setHistory} history={history} toolType={toolType}/>
        
        <GameInfo/>
      </div>
    </>


  );
}


export default App;