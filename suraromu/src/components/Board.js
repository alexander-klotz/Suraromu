import React from 'react'
import Grid from './Grid'


export default function Board(props) {
  
  return (
    <div className="board">
      <Grid {...props}/>
    </div>
  );  
}  
