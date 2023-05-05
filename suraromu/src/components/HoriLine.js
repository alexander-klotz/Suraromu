import React, { useState } from "react"

export default function HoriLine(props) {
    
    const [color, setColor] = useState(false);

    const changeColor = () => {
        setColor(oldValue => !oldValue)
    };


    return(
    <div key={props.index} className="hori--line--hitbox" onClick={changeColor}>
        {color && <div className="hori--line"></div>}
        
    </div>
    )
}


//<div key={props.index} className="hori--line">  </div>