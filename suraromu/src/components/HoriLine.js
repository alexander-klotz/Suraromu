import React, { useState } from "react"

export default function HoriLine(props) {
    
    const [color, setColor] = useState('blue');

    const changeColor = () => {
        setColor('red');
    };


    return(
    <div key={props.index} className="hori--line" style={{ backgroundColor: color }} onClick={changeColor}>
    </div>
    )
}