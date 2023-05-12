import React, { useState } from "react"

export default function HoriLine(props) {
    
    return(
    <div key={props.index} className="hori--line--hitbox" onClick={props.handleLineClick}>
        {props.isSet && <div className="hori--line"></div>}
        
    </div>
    )
}