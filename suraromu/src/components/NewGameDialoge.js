import React, { useState } from 'react';
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
} from '@mui/material';

import AddCircleOutlineOutlinedIcon from '@mui/icons-material/AddCircleOutlineOutlined';
import getPuzzles from '../utils.js/premadePuzzles';

const NewGameDialoge = (props) => {

  const createInitialArray = (rows, cols) => {
    const newArray = [];
    for (let i = 0; i < rows; i++) {
      newArray.push(new Array(cols).fill(0));
    }
    return newArray;
  };

  const buttonStyle = {
    color: "black",
  };

  const iconStyle = {
    fontSize: "30px",
  };
  
  const [open, setOpen] = useState(false);
  const [objectData, setObjectData] = useState({
    size: 'small',
    difficulty: 'easy',
    generated: false,
    puzzle: ''
  });

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleValueChange = (property, value) => {
    setObjectData((prevState) => ({
      ...prevState,
      [property]: value,
    }));
  };

  const puzzles = getPuzzles(objectData.difficulty, objectData.size)
  const puzzleOptions = Array.from({ length: puzzles.length }, (_, index) => index);

  const handleConfirm = () => {
    
    let newPuzzle = {
      rows: 10,
      cols: 10,
      arrayHori: createInitialArray(10, 9),
      arrayVert: createInitialArray(9, 10),
      startCell: [0, 0],
      blockedCells: [],
      gates: {
      }}
    if (objectData.puzzle !== ''){
      newPuzzle = puzzles[objectData.puzzle]
    }
    
    props.setNewPuzzle(newPuzzle)

    handleClose()
  };

  return (
<div style={{ display: 'flex', justifyContent: 'center'}}>
      <Button onClick={handleOpen} style={buttonStyle} startIcon={<AddCircleOutlineOutlinedIcon style={iconStyle}/>}>
        New
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Edit Object</DialogTitle>
        <DialogContent style={{ display: 'flex', justifyContent: 'center' ,   flexDirection: "column",   alignItems: "flex-start",}}>
          <FormControl sx={{ m: 1, minWidth: 200}}>
            <InputLabel id="size-select-label">Size</InputLabel>
            <Select
              labelId="size-select-label"
              id="size-select"
              value={objectData.size}
              onChange={(event) => handleValueChange('size', event.target.value)}
              label="Size"
            >
              <MenuItem value="small">Small</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="big">Big</MenuItem>
            </Select>
          </FormControl>
          <FormControl sx={{ m: 1, minWidth: 200}}>
            <InputLabel id="difficulty-select-label">Difficulty</InputLabel>
            <Select
              labelId="difficulty-select-label"
              id="difficulty-select"
              value={objectData.difficulty}
              onChange={(event) => handleValueChange('difficulty', event.target.value)}
              label="Difficulty"
            >
              <MenuItem value="easy">Easy</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="hard">Hard</MenuItem>
            </Select>
          </FormControl>
          {!objectData.generated && 
              <FormControl sx={{ m: 1, minWidth: 200}}>
                <InputLabel id="puzzle-select-label">Puzzle</InputLabel>
                <Select
                  labelId="puzzle-select-label"
                  id="puzzle-select"
                  value={objectData.puzzle}
                  onChange={(event) => handleValueChange('puzzle', event.target.value)}
                  label="Puzzle"
                >
                  {puzzleOptions.map((option) => (
                    <MenuItem key={option} value={option}>
                      {option}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            }
          <FormControlLabel sx={{ m: 1, minWidth: 200}}
            control={
              <Checkbox
                checked={objectData.generated}
                onChange={(event) => handleValueChange('generated', event.target.checked)}
                color="primary"
              />
            }
            label="Generated"
          />

          
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleConfirm} color="primary" variant="contained">
            Confirm
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default NewGameDialoge;
