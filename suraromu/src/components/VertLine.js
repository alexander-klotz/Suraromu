import React, { useState } from "react"

export default function VertLine(props) {
    
    const [color, setColor] = useState(false);

    const changeColor = () => {
        setColor(oldValue => !oldValue)
    };

    return(
    <div key={props.index} className="vert--line--hitbox" onClick={changeColor}>
        {color && <div className="vert--line"></div>}
    </div>
    )
}