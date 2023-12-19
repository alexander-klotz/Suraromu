import React, { useState } from 'react';
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';

import SmartToyOutlinedIcon from '@mui/icons-material/SmartToyOutlined';
import getSolverPuzzle from '../utils.js/convertForSolver'

const SolveDialoge = (props) => {

  const buttonStyle = {
    color: "black",
  };

  const iconStyle = {
    fontSize: "30px",
  };
  
  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };


  const updateArray = (solution, array) => {
    // Create a new array based on the boolean array
    let newArray = solution.map((row, i) => 
        row.map((item, j) => {
          if(item){
            return 1
          }else if (array[i][j] === 1){
            return 0
          }else{
            return array[i][j]
          }
        })
      );
    // Set the state with the new array
    return newArray
  };

  const handlePredifined = () => {
    

    let newArrayHori = updateArray(props.puzzle.solution[0], [...props.puzzle.arrayHori]);
    let arrayVert = updateArray(props.puzzle.solution[1], [...props.puzzle.arrayVert]);

    props.setPuzzle({
      ...props.puzzle,
      arrayHori: newArrayHori,
      arrayVert: arrayVert,
    })

    handleClose()
  };


  const handleSolver = () => {
    
    // MAYBe instead use some 
    // TODO: we either get the newArrayHor and Vert from the presaved solution (if useSolver is unchecked or we instead )

    let solverParams = getSolverPuzzle(props.puzzle)
    console.log(solverParams)  
    let solution = []
    // Frontend websocket
    const socket = new WebSocket('ws://localhost:5000/ws');

    socket.addEventListener('open', function (event) {
      socket.send(JSON.stringify(solverParams));
    });
    
    socket.addEventListener('message', function (event) {
        if(event.data[0] === "["){
          solution = JSON.parse(event.data)
          socket.close();
          
          let newArrayHori = updateArray(solution[0], [...props.puzzle.arrayHori]);
          let arrayVert = updateArray(solution[1], [...props.puzzle.arrayVert]);
      
          props.setPuzzle({
            ...props.puzzle,
            arrayHori: newArrayHori,
            arrayVert: arrayVert,
          })
          
          handleClose()
        
        }
        console.log('Message from server: ', event.data);
    });
    
    // To stop the calculation
    socket.addEventListener('open', function (event) {
        socket.send('stop');
    });
    
    
  };
  

  return (
<div style={{ display: 'flex', justifyContent: 'center'}}>
      <Button onClick={handleOpen} style={buttonStyle} startIcon={<SmartToyOutlinedIcon style={iconStyle}/>}>
        Solve
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Solve Puzzle</DialogTitle>
        <DialogContent style={{ display: 'flex', justifyContent: 'center' ,   flexDirection: "column",   alignItems: "flex-start",}}>
        <Button 
            onClick={handlePredifined} 
            color={"primary"} 
            variant="contained"
            disabled={!Object.hasOwn(props.puzzle, "solution")}
          >
            Use saved Solution
          </Button>


          <br/>
          <Button onClick={handleSolver} color="primary" variant="contained">
            Use SAT-Solver
          </Button>

          
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>

        </DialogActions>
      </Dialog>
    </div>
  );
};

export default SolveDialoge;
