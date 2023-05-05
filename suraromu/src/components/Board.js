import React from 'react'
import Grid from './Grid'


export default function Board(props) {
  
  const rows = props.rows
  const columns = props.columns

  
  return (
    <div className="board">
      <Grid rows={rows} columns={columns}/>
    </div>
  );  
}  
