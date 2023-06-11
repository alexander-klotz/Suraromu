import './App.css';
import Board from './components/Board';
import { useState } from 'react';
import GameInfo from './components/GameInfo';
import Controls from './components/Controls';

function App() {


  const createInitialArray = (rows, cols) => {
    const newArray = [];
    for (let i = 0; i < rows; i++) {
      newArray.push(new Array(cols).fill(false));
    }
    return newArray;
  };

  const [puzzle, setPuzzle] = useState({
    rows: 10,
    cols: 10,
    arrayHori: createInitialArray(10, 9),
    arrayVert: createInitialArray(9, 10)
  });


  function changeSize(newRows, newCols) {
    console.log("rows will be set");
  
    const newArrayHori = createInitialArray(newRows, newCols - 1);
    const newArrayVert = createInitialArray(newRows - 1, newCols);
    console.log("(changerows): ", newArrayHori, newArrayVert)

    setPuzzle((prevState) => ({
      ...prevState,
      rows: newRows,
      cols: newCols,
      arrayHori: newArrayHori,
      arrayVert: newArrayVert
    }));
  
    console.log("rows are set");
  }


  function deleteConnections(){
    setPuzzle((prevState) => ({
      ...prevState,
      arrayHori: createInitialArray(prevState.rows, prevState.cols-1),
      arrayVert: createInitialArray(prevState.rows-1, prevState.cols)
    }));
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

        



        
        <Controls deleteFunction={deleteConnections} changeSize={changeSize}/>
        <Board puzzle={puzzle} setPuzzle={setPuzzle}/>
        
        <GameInfo/>
      </div>
    </>


  );
}


export default App;