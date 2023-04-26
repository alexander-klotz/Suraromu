import './App.css';
import Board from './components/Board';

function App() {
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
        <Board rows={10} columns={10} />
      </div>
    </>


  );
}


export default App;
