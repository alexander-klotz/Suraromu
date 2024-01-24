import Button from '@mui/material/Button';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import NewGameDialoge from './NewGameDialoge';
import UndoIcon from '@mui/icons-material/Undo';
import SolveDialoge from './SolveDialoge'
import EditGameDialoge from './EditGameDialoge'

export default function Controls(props) {


    const buttonStyle = {
        color: "black",
    };

    const iconStyle = {
        fontSize: "30px",
    };

    const handleUndo = () => {
        if (props.history.length > 1) {
          const previousState = props.history[props.history.length - 2];
          const newHistory = props.history.slice(0, props.history.length - 1);
          
          props.setShouldTrack(false);
          props.setPuzzle(previousState);
          props.setHistory(newHistory);
        }
      };

    return (
        
        <div id="controls">

            <NewGameDialoge {...props}/>

            <EditGameDialoge {...props}/>

            <SolveDialoge {...props}/>
            
            <Button onClick={props.deleteFunction} style={buttonStyle} startIcon={<DeleteOutlinedIcon style={iconStyle}/>}>
                Delete
            </Button>

            <Button onClick={handleUndo} disabled={props.history.length === 1} style={buttonStyle} startIcon={<UndoIcon style={iconStyle}/>}>
                Undo
            </Button>
        
        </div>
    )

}