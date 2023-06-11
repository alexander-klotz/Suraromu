import Button from '@mui/material/Button';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import DoneOutlineOutlinedIcon from '@mui/icons-material/DoneOutlineOutlined';
import SmartToyOutlinedIcon from '@mui/icons-material/SmartToyOutlined';
import NewGameDialoge from './NewGameDialoge';

export default function Controls(props) {


    const buttonStyle = {
        color: "black",
    };

    const iconStyle = {
        fontSize: "30px",
    };

    return (
        
        <div id="controls">

            <NewGameDialoge {...props}/>

            <Button style={buttonStyle} startIcon={<DoneOutlineOutlinedIcon style={iconStyle}/>}>
                Check
            </Button>

            <Button style={buttonStyle} startIcon={<SmartToyOutlinedIcon style={iconStyle}/>}>
                Solve
            </Button>
            
            <Button onClick={props.deleteFunction} style={buttonStyle} startIcon={<DeleteOutlinedIcon style={iconStyle}/>}>
                Delete
            </Button>
        
        </div>
    )

}