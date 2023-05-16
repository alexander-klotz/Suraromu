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

  const [rows, setRows] = useState(10)
  const [cols, setCols] = useState(10)
  const [arrayHori, setArrayHori] = useState(createInitialArray(9, 10));
  const [arrayVert, setArrayVert] = useState(createInitialArray(10, 9));


  function changeRows(event){
    setRows(event.target.value)
    setArrayHori(createInitialArray(event.target.value, cols-1));
    setArrayVert(createInitialArray(event.target.value-1, cols));
  }

  function changeCols(event){
    setCols(event.target.value)
    setArrayHori(createInitialArray(rows, event.target.value-1));
    setArrayVert(createInitialArray(rows-1, event.target.value));
  }

  function deleteConnections(){
    setArrayHori(createInitialArray(rows, cols-1));
    setArrayVert(createInitialArray(rows-1, cols));
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

        



        
        <Controls deleteFunction={deleteConnections}/>
        <Board rows={rows} columns={cols} arrayHori={arrayHori} arrayVert={arrayVert} changeArrayHori={setArrayHori} changeArrayVert={setArrayVert} />
        
        <GameInfo/>
      </div>
    </>


  );
}


export default App;


/*
       <input 
        id="rowinp" 
        type="range" 
        min="0" max="30"
        value={rows} 
        onChange={changeRows}
        step="1"/>
        <input 
        id="colinp" 
        type="range"
        value={cols} 
        onChange={changeCols} 
        min="0" max="30" 
        step="1"/>

*/