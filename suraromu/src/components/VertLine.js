import React, { useState } from "react"

export default function VertLine(props) {
    
    const [color, setColor] = useState('blue');

    const changeColor = () => {
        setColor('red');
    };

    return(
    <div key={props.index} className="vert--line" style={{ backgroundColor: color }} onClick={changeColor}>
    </div>
    )
}