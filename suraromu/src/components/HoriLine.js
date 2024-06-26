import CloseIcon from '@mui/icons-material/Close';
import React, { useState } from "react";

export default function HoriLine(props) {

    const [isHovering, setIsHovering] = useState(false);
    const handleMouseOver = () => {
      setIsHovering(true);
    };
  
    const handleMouseOut = () => {
      setIsHovering(false);
    };

    
    return(
    <div key={props.index} className="hori--line--hitbox" onClick={props.handleLineClick} onMouseOver={handleMouseOver} onMouseOut={handleMouseOut}>
        {props.isSet === 1 && (!isHovering || props.toolType === 1) && 
            <div className="hori--line"></div>}
        {props.isSet === 2 && (!isHovering || props.toolType === 2) &&
            <CloseIcon style={{ color: 'red' }}/>}
        
        {/* hovering animations */}
        {isHovering && props.hoverable && (props.toolType === 1 ? 
        props.isSet !== 1 && <div className="hori--line"></div>:
        props.isSet !== 2 && <CloseIcon style={{ color: 'red'}}/>
        )}
        
    </div>
    )
}