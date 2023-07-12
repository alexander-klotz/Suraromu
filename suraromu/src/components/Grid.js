import React from 'react'
import Cell from './Cell'
import VertLine from './VertLine'
import HoriLine from './HoriLine'
import { useRef, useEffect, useState } from 'react';

function Grid(props) {

  const gridContainerRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(0);
  const [containerHeight, setContainerHeight] = useState(0);

  useEffect(() => {
    const handleResize = () => {
      if (gridContainerRef.current) {
        const { width, height } = gridContainerRef.current.getBoundingClientRect();
        setContainerWidth(width);
        setContainerHeight(height);
      }
    };

    // Initial calculation
    handleResize();

    // Recalculate on window resize
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  function handleLineClick(rowIndex, colIndex, orient, array) {
    
    // skip since it's a invalid line
    if(array[rowIndex][colIndex] === -1) {
      return 
    }

    // Create a copy of the existing array
    const newArray = [...array];


    // Update the value at the specified indices


    if(newArray[rowIndex][colIndex] === 0) {
      //normal empty line
      newArray[rowIndex][colIndex] = props.toolType
    } else if(newArray[rowIndex][colIndex] === 1) {
      //filled line
      newArray[rowIndex][colIndex] = props.toolType === 1 ? 0 : 2
    } else if(newArray[rowIndex][colIndex] === 2){
      //crossed out line
      newArray[rowIndex][colIndex] =  props.toolType === 1 ? 1 : 0
    }
    

    
    // Set the updated array as the new state
    if (orient === "h"){
      props.setPuzzle((prevState) => ({
        ...prevState,
        arrayHori: newArray,
      }));
    }

    if (orient === "v"){
      props.setPuzzle((prevState) => {
        return ({
        ...prevState,
        arrayVert: newArray,
      })}
      );
      
    }

    props.setHistory((prevHistory) => [...prevHistory, structuredClone(props.puzzle)]);
  };

  const rows = props.puzzle.rows
  const columns = props.puzzle.cols
  const cellSize = Math.min(100/columns, 100/rows) 

  const cellWidth = containerWidth / columns;
  const cellHeight = containerHeight / rows;
  
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

  const cells = Array.from({ length: rows*columns }).map((_, index) => {
    return (<Cell index={index} puzzle={props.puzzle}/>)
  }
    
  );

  const backgroundBoard = <div ref={gridContainerRef} style={gridStyleBoard}>{cells}</div>

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
    top: `${Math.min(cellHeight, cellWidth)*0.25}px`,
    bottom: "auto",
    position: "absolute",
    justifyContent: "center",
    
  };

  const horiLines = Array.from({ length: rows*(columns-1)}).map((_, index) => {
    return (    
      <HoriLine 
        index={index} 
        handleLineClick={() => 
          handleLineClick(Math.floor(index/(columns-1)), index%(columns-1), "h", props.puzzle.arrayHori)} 
        isSet={props.puzzle.arrayHori[Math.floor(index/(columns-1))][index%(columns-1)]}
        toolType={props.toolType}
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
    top: `${Math.min(cellHeight, cellWidth)*0.5}px`,
    bottom: "auto",
    position: "absolute",
    justifyContent: "center",
  
    
  };

  const vertLines = Array.from({ length: (rows-1)*columns}).map((_, index) => {
    
    return (
      <VertLine 
        index={index} 
        handleLineClick={() => 
          handleLineClick(Math.floor(index/(columns)), index%(columns), "v", props.puzzle.arrayVert)} 
        isSet={props.puzzle.arrayVert[Math.floor(index/(columns))][index%(columns)]}
        toolType={props.toolType}
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
