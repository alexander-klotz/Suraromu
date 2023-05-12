import React, { useState } from "react"

export default function VertLine(props) {
    
    return(
    <div key={props.index} className="vert--line--hitbox" onClick={props.handleLineClick}>
        {props.isSet && <div className="vert--line"></div>}
    </div>
    )
}