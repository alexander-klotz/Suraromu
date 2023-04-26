import React from 'react'
import Cell from './Cell'
import VertLine from './VertLine'
import HoriLine from './HoriLine'

function Grid(props) {
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
    bottom: 0,
    position: "absolute",
    
  };

  const cells = Array.from({ length: rows*columns }).map((_, index) => (
    <Cell index={index}/>
  ));

  const backgroundBoard = <div style={gridStyleBoard}>{cells}</div>

  const gridStyleVertLines = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns-1}, ${cellSize-3}%)`,
    gridTemplateRows: `repeat(${rows}, ${cellSize-3}%)`,
    margin: "auto",
    padding: '0rem',
    width: "80%",
    gap: "3%",
    maxWidth: "60rem",
    aspectRatio: "1/1",
    left: 0,
    right: 0,
    paddingTop: "1.5%",
    bottom: 0,
    position: "relative",
    justifyContent: "center",
    
  };

  const vertLines = Array.from({ length: rows*(columns-1) }).map((_, index) => (
    <VertLine index={index}/>
  ));

  const vertLinesGrid = <div style={gridStyleVertLines}>{vertLines}</div>
  
  const gridStyleHoriLines = {
    display: 'grid',
    gridTemplateColumns: `repeat(${columns}, ${cellSize-3}%)`,
    gridTemplateRows: `repeat(${rows-1}, ${cellSize-3}%)`,
    margin: "auto",
    padding: '0rem',
    
    width: "80%",
    gap: "3%",
    maxWidth: "60rem",
    aspectRatio: "1/1",
    left: "1.5%",
    right: 0,
    top: `${cellSize+1.5}%`,
    bottom: 0,
    position: "absolute",
  
    
  };

  const horiLines = Array.from({ length: (rows-1)*columns }).map((_, index) => (
    <HoriLine index={index}/>
  ));

  const horiLinesGrid = <div style={gridStyleHoriLines}>{horiLines}</div>


  return (
    <div className='Grid'>
      {backgroundBoard}
      {vertLinesGrid}
      {horiLinesGrid}
    </div>
  )
}

export default Grid;
