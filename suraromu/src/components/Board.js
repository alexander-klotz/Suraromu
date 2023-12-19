import React from 'react'
import Grid from './Grid'
import {useState} from 'react';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import ZoomOutIcon from '@mui/icons-material/ZoomOut';
import Button from '@mui/material/Button';


export default function Board(props) {
  
  const [size, setSize] = useState(0); // Initial size
  const buttonStyle = {
    color: "black",
  };

  const iconStyle = {
      fontSize: "30px",
  };

  return (
    <div className="board">
      <Button onClick={() => setSize(size - 10)} style={buttonStyle} startIcon={<ZoomInIcon style={iconStyle}/>}>
      </Button>
      <Button onClick={() => setSize(Math.min(80, size + 10))} style={buttonStyle} startIcon={<ZoomOutIcon style={iconStyle}/>}>
      </Button>

      <Grid {...props} size={size}/>
    </div>
  );  
}  
