import CloseIcon from '@mui/icons-material/Close';
import React, { useState } from "react";

export default function VertLine(props) {

    const [isHovering, setIsHovering] = useState(false);
    const handleMouseOver = () => {
      setIsHovering(true);
    };
  
    const handleMouseOut = () => {
      setIsHovering(false);
    };
    
    return(
    <div key={props.index} className="vert--line--hitbox" onClick={props.handleLineClick} onMouseOver={handleMouseOver} onMouseOut={handleMouseOut}>
        {props.isSet === 1 && (!isHovering || props.toolType === 1) && 
            <div className="vert--line"></div>}
        {props.isSet === 2 && (!isHovering || props.toolType === 2) &&
            <CloseIcon style={{ color: 'red' }}/>}
        
        {/* hovering animations TODO: blocked cells from gates also need to be set to -1 in the initialization of the array!!!!*/ }
        {isHovering && props.hoverable && (props.toolType === 1 ? 
        props.isSet !== 1 && <div className="vert--line"></div>:
        props.isSet !== 2 && <CloseIcon style={{ color: 'red'}}/>
        )}    </div>
    )
}