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
import getRandomPuzzle from '../utils.js/PuzzleAPI';

const NewGameDialoge = (props) => {

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

  const handleConfirm = () => {
  
    //TODO: check if puzzle should be generated instead or if it should be a random one from the saved ones
    // (maybe the saved ones should also be from the same api or where should they be saved??) 
    const newPuzzle = getRandomPuzzle()
    console.log(newPuzzle)
    props.changeRows(newPuzzle.rows)
    props.changeCols(newPuzzle.columns)
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
