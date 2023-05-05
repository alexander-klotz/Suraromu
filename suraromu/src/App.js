import './App.css';
import Board from './components/Board';
import { useState } from 'react'

function App() {

  const [rows, setRows] = useState(10)
  const [cols, setCols] = useState(10)

  function changeRows(event){
    setRows(event.target.value)
  }

  function changeCols(event){
    setCols(event.target.value)
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

        
        <br></br>
        <div id="controls"></div>

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
        
        <Board rows={rows} columns={cols} />
      </div>
    </>


  );
}


export default App;
