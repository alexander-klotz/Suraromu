import Button from '@mui/material/Button';
import AddCircleOutlineOutlinedIcon from '@mui/icons-material/AddCircleOutlineOutlined';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import DoneOutlineOutlinedIcon from '@mui/icons-material/DoneOutlineOutlined';
import SmartToyOutlinedIcon from '@mui/icons-material/SmartToyOutlined';

export default function Controls(props) {


    const buttonStyle = {
        color: "black",
    };

    const iconStyle = {
        fontSize: "30px", // Adjust the size as needed
    };

    return (
        
        <div id="controls">

            <Button style={buttonStyle} startIcon={<AddCircleOutlineOutlinedIcon style={iconStyle}/>}>
                New
            </Button>

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