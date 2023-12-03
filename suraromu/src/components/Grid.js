import React from 'react'
import Cell from './Cell'
import VertLine from './VertLine'
import HoriLine from './HoriLine'
import { useRef, useEffect, useState, useMemo } from 'react';

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


  const vertiGateIdxs = useMemo(() => computeGateIdxs(props.puzzle.gates, "v"), [props.puzzle.gates]);
  const horiGateIdxs = useMemo(() => computeGateIdxs(props.puzzle.gates, "h"), [props.puzzle.gates]);

  function computeGateIdxs(gates, orientation) {
      let gateIdxs = [];
      for (let key in gates) {
          if (key === '0') {
              // all the unordered gates
              for (let gateKey in gates[key]) {
                  const curGate = gates[key][gateKey];
                  if(curGate.orientation === orientation){
                      const length = curGate.length;
                      gateIdxs = gateIdxs.concat(Array.from({ length }, (_, index) => {
                          return orientation === "h" ? [curGate.startCell[0], curGate.startCell[1] + index] : [curGate.startCell[0] + index, curGate.startCell[1]];
                      }));
                  }
              }
          } else {
              // all the ordered cells
              const curGate = gates[key];
              if(curGate.orientation === orientation){
                  if(curGate?.direction !== undefined){
                    const length = curGate.length;
                    gateIdxs = gateIdxs.concat(Array.from({ length }, (_, index) => {
                      if(curGate.direction === "w") return [curGate.startCell[0], curGate.startCell[1] - index]
                      if(curGate.direction === "e") return [curGate.startCell[0], curGate.startCell[1] + index]
                      if(curGate.direction === "s") return [curGate.startCell[0] + index, curGate.startCell[1]]
                      if(curGate.direction === "n") return [curGate.startCell[0] - index, curGate.startCell[1]]
                      return []
                    }));
                  }else{
                    const length = curGate.length;
                    gateIdxs = gateIdxs.concat(Array.from({ length }, (_, index) => {
                        return orientation === "h" ? [curGate.startCell[0], curGate.startCell[1] + index] : [curGate.startCell[0] + index, curGate.startCell[1]];
                    }));
                  }
                  
              }
          }
      }
      return gateIdxs;
  }

  // create a grid that stores the gate numbers
  let gateGrid = Array.from({ length: props.puzzle.rows }, () => Array(props.puzzle.cols).fill(""));
  for (let key in props.puzzle.gates) {
    if (key === '0') {
        // all the unordered gates
        for (let gateKey in props.puzzle.gates[key]) {
            const possibleGateCells = getBlockedGateCells(props.puzzle.gates[key][gateKey])
            for (let idx of possibleGateCells){
              if (idx[0] >= 0 && idx[0] < props.puzzle.rows && idx[1] >= 0 && idx[1] < props.puzzle.cols ){
                gateGrid[idx[0]][idx[1]] = '0'
              }
            }
            
        }
    } else {
        // all the ordered cells
        const possibleGateCells = getBlockedGateCells(props.puzzle.gates[key])
        for (let idx of possibleGateCells){
          if (idx[0] >= 0 && idx[0] < props.puzzle.rows && idx[1] >= 0 && idx[1] < props.puzzle.cols ){
            if(props.puzzle.gates[key]?.direction !== undefined){
              if(props.puzzle.gates[key].direction === "w") gateGrid[idx[0]][idx[1]] = key.toString() + "←";
              if(props.puzzle.gates[key].direction === "e") gateGrid[idx[0]][idx[1]] = key.toString() + "→";
              if(props.puzzle.gates[key].direction === "s") gateGrid[idx[0]][idx[1]] = key.toString() + "↓";
              if(props.puzzle.gates[key].direction === "n") gateGrid[idx[0]][idx[1]] = key.toString() + "↑";
              
              
            }else{
              gateGrid[idx[0]][idx[1]] = key.toString();
            }
            
          }
        }
    }
  }

  function getBlockedGateCells(gate) {
    const cells = []
    const row = gate.startCell[0]
    const col = gate.startCell[1]

    if(gate?.direction !== undefined){
      if (gate.direction === "w") cells.push([row, col+1])
      if (gate.direction === "e") cells.push([row, col-1])
      if (gate.direction === "s") cells.push([row-1, col])
      if (gate.direction === "n") cells.push([row+1, col])
    }
    else if(gate.orientation === "h") {
        cells.push([row, col-1])
        cells.push([row, col+gate.length])
    }else {
        cells.push([row-1, col])
        cells.push([row+gate.length, col])
    }

    return cells
  }

  const cells = Array.from({ length: rows*columns }).map((_, index) => {
    return (<Cell index={index} puzzle={props.puzzle} vertiGateIdxs={vertiGateIdxs} horiGateIdxs={horiGateIdxs} gateGrid={gateGrid} />)
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
        hoverable={props.puzzle.arrayHori[Math.floor(index/(columns-1))][index%(columns-1)] !== -1}
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
        hoverable={props.puzzle.arrayVert[Math.floor(index/(columns))][index%(columns)] !== -1}
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
