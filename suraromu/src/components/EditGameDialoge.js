import React, { useState, useEffect, useRef } from 'react';
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  InputLabel,
} from '@mui/material';

import EditIcon from '@mui/icons-material/Edit';

const EditGameDialoge = (props) => {

  const buttonStyle = {
    color: "black",
  };

  const iconStyle = {
    fontSize: "30px",
  };

  const [open, setOpen] = useState(false);
  const [selectedAttribute, setSelectedAttribute] = useState(Object.keys(props.puzzle)[0]);
  const [attributeValue, setAttributeValue] = useState(props.puzzle[selectedAttribute]);
  const [error, setError] = useState(null);

  const handleOpen = () => {
    setAttributeValue(JSON.stringify(props.puzzle[selectedAttribute], null));
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleConfirm = () => {
    try {
      console.log(attributeValue, selectedAttribute)
      if (selectedAttribute === "rows"){
        props.setPuzzle({
          ...props.puzzle,
          [selectedAttribute]: JSON.parse(attributeValue),
          arrayHori: props.createInitialArray(JSON.parse(attributeValue), props.puzzle["cols"]-1),
          arrayVert: props.createInitialArray(JSON.parse(attributeValue)-1, props.puzzle["cols"])
        })
        
      }
      else if (selectedAttribute === "cols"){
        props.setPuzzle({
          ...props.puzzle,
          [selectedAttribute]: JSON.parse(attributeValue),
          arrayHori: props.createInitialArray(props.puzzle["rows"], JSON.parse(attributeValue)-1),
          arrayVert: props.createInitialArray(props.puzzle["rows"]-1, JSON.parse(attributeValue))
        })
      }else{
        props.setPuzzle({
          ...props.puzzle,
          [selectedAttribute]: JSON.parse(attributeValue),
        })
      }



      handleClose();
    } catch (e) {
      setError('Invalid JSON');
    }
  };

  const handleAttributeChange = (event) => {
    setSelectedAttribute(event.target.value);
    setAttributeValue(JSON.stringify(props.puzzle[event.target.value], null));
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center'}}>
      <Button style={buttonStyle} startIcon={<EditIcon style={iconStyle}/>} onClick={handleOpen}>
        Edit
      </Button>
      <Dialog open={open} onClose={handleClose} fullWidth={true} maxWidth={'md'}>
        <DialogTitle>Edit current puzzle</DialogTitle>
        <DialogContent >
          <p style={{color: "red"}}>
          Warning advanced feature!
          Only change something if you know what you are doing
          </p>

          <InputLabel id="attribute-label">Attribute</InputLabel>
          <Select
            labelId="attribute-label"
            value={selectedAttribute}
            onChange={handleAttributeChange}
          >
            {Object.keys(props.puzzle).map((key) => (
              <MenuItem value={key}>{key}</MenuItem>
            ))}
          </Select>
          <TextField
            style={{minWidth: "100%"}}
            error={!!error}
            helperText={error}
            multiline
            minRows={3}
            value={attributeValue}
            onChange={(e) => setAttributeValue(e.target.value)}
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

export default EditGameDialoge;

