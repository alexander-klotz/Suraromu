import React from 'react'
import Cell from './Cell'
import VertLine from './VertLine'
import HoriLine from './HoriLine'

function Grid(props) {

  function handleLineClick(rowIndex, colIndex, array, changeArray) {
    // Create a copy of the existing array
    const newArray = [...array];
    
    // Update the value at the specified indices
    newArray[rowIndex][colIndex] = !newArray[rowIndex][colIndex];
    // Set the updated array as the new state
    changeArray(newArray);
  };

  console.log(props)

  const rows = props.rows
  const columns = props.columns
  const cellSize = Math.min(100/columns, 100/rows) 
  
  const gridStyleBoard = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, ${cellSize}%)`,
    gridTemplateRows: `repeat(${rows}, ${cellSize}%)`,
    gap: '0px',
    margin: "auto",
    padding: '0rem',
    width: "80%",
    maxWidth: "60rem",
    aspectRatio: "1/1",
    left: 0,
    right: 0,
    top: 0,
    bottom: "auto",
    position: "absolute",
    justifyContent: "center",
    
  };

  const cells = Array.from({ length: rows*columns }).map((_, index) => (
    <Cell index={index}/>
  ));

  const backgroundBoard = <div style={gridStyleBoard}>{cells}</div>

  const gridStyleHoriLines = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns-1}, ${cellSize}%)`,
    gridTemplateRows: `repeat(${rows}, ${cellSize*0.50}%)`,
    margin: "auto",
    padding: '0rem',
    width: "80%",
    rowGap: `${cellSize*0.5}%`,
    maxWidth: "60rem",
    aspectRatio: "1/1",
    left: 0,
    right: 0,
    top: `${cellSize*0.175}%`,
    bottom: "auto",
    position: "absolute",
    justifyContent: "center",
    
  };

  const horiLines = Array.from({ length: rows*(columns-1)}).map((_, index) => {
    return (    
      <HoriLine 
        index={index} 
        handleLineClick={() => 
          handleLineClick(Math.floor(index/(columns)), index%(columns), props.arrayHori, props.changeArrayHori)} 
        isSet={props.arrayHori[Math.floor(index/(columns))][index%(columns)]}
      />
    )
  }

  );

  const horiLinesGrid = <div style={gridStyleHoriLines}>{horiLines}</div>
  
  const gridStyleVertLines = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, ${cellSize*0.5}%)`,
    gridTemplateRows: `repeat(${rows-1}, ${cellSize}%)`,
    margin: "auto",
    padding: '0rem',
    columnGap: `${cellSize*0.5}%`,
    width: "80%",
    maxWidth: "60rem",
    aspectRatio: "1/1",
    left: 0,
    right: 0,
    top: `${cellSize*0.35}%`,
    bottom: "auto",
    position: "absolute",
    justifyContent: "center",
  
    
  };

  const vertLines = Array.from({ length: (rows-1)*columns }).map((_, index) => {
    return (
      <VertLine 
      index={index} 
      handleLineClick={() => 
        handleLineClick(Math.floor(index/(columns)), index%(columns), props.arrayVert, props.changeArrayVert)} 
      isSet={props.arrayVert[Math.floor(index/(columns))][index%(columns)]}
    />
    )
  }

  );

  const vertLinesGrid = <div style={gridStyleVertLines}>{vertLines}</div>

  
  const gridStyle = {
    position: "relative",
    aspectRatio: "1/1",
  }

  return (
    <div className='Grid' style={gridStyle}>
      {backgroundBoard}
      {vertLinesGrid}
      {horiLinesGrid}
    </div>
  )
}

export default Grid;
