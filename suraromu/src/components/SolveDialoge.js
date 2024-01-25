import React, { useState, useEffect, useRef } from 'react';
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  AlertTitle,
  LinearProgress,
  Box,
  Snackbar,
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

  const ws = useRef(null);

  useEffect(() => {
      ws.current = new WebSocket('ws://localhost:5000/ws');
      ws.current.onopen = () => console.log("solver ws opened");
      ws.current.onclose = () => console.log("solver ws closed");

      const wsCurrent = ws.current;

      return () => {
          wsCurrent.close();
      };
  }, []);
  
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [openError, setOpenError] = useState(false);
  const [openSuccess, setOpenSuccess] = useState(false);
  const [abort, setAbort] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    handleAbort();
    setIsLoading(false);
  };

  useEffect(() => {
    if (abort) {
      setAbort(false);
    }
  }, [abort]);

  const handleAbort = () => {
    if (!ws.current) return;
    if (ws.current.readyState === WebSocket.OPEN) {
      console.log('solver abort')
      ws.current.send('abort');
    }
    setAbort(true);
    setIsLoading(false);
  };


  const updateArray = (solution, array) => {
    // Create a new array based on the boolean array
    console.log("help", solution, array)
    let newArray = solution.map((row, i) => 
        row.map((item, j) => {
          console.log("i:", i)
          console.log("j:", j)
          console.log("item:", item)
          console.log("array:", array[i][j])
          console.log("me", i, j, item, array[i][j])
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

    setIsLoading(true)
    let solverParams = getSolverPuzzle(props.puzzle)
    let solution = []

    ws.current.send(JSON.stringify(solverParams));
    
    ws.current.addEventListener('message', function (event) {
      
      if (event.data === "[]"){
        console.log('Solver did not find a solution: ', event.data);
        setIsLoading(false)
        // display error message to the user
        setOpenError(true)
        setTimeout(() => {
          handleClose()
        }, 4000);

        
      }

      else if(event.data[0] === "["){

        solution = JSON.parse(event.data)
        setIsLoading(false)

        // display success message to the user
        setOpenSuccess(true)
        setTimeout(() => {
          handleClose()
        }, 2000);

        
        let newArrayHori = updateArray(solution[0], [...props.puzzle.arrayHori]);
        let arrayVert = updateArray(solution[1], [...props.puzzle.arrayVert]);
    
        props.setPuzzle({
          ...props.puzzle,
          arrayHori: newArrayHori,
          arrayVert: arrayVert,
        })
        
      
      }
      console.log('Message from solver: ', event.data);
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
          <br/>
          <Box sx={{ width: '100%' }}>
            {isLoading && <LinearProgress />}
            {isLoading && <Button onClick={handleAbort} color="secondary" variant="contained">Abort</Button>}
          </Box>

          <Snackbar open={openError} autoHideDuration={4000} onClose={() => setOpenError(false)}>
            <Alert severity="error">
              <AlertTitle>Failure to solve</AlertTitle>
              Solver unable to find solution to the currently selected puzzle
            </Alert>
          </Snackbar>
          <Snackbar open={openSuccess} autoHideDuration={2000} onClose={() => setOpenSuccess(false)}>
            <Alert severity="success">
              Found solution
            </Alert>
          </Snackbar>


          
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>

        </DialogActions>
      </Dialog>
    </div>
  );
};

export default SolveDialoge;
