import React, { useState } from "react"
import "./GameInfo.css"

export default function GameInfo(props) {
    
const [infoVisibility, setInfoVisibility] = useState(false);

    const showInfo = () => {
        setInfoVisibility(oldValue => !oldValue)
    };

    return(
        <>
            <button className="InfoButton" id="mydiv" onClick={showInfo}>?</button>
            {infoVisibility && <div className="Info">The game consists of 3 main rules:<br />
            1. ASDfadsf<br />
            2. sdafsda<br />
            3. dasdfasd<br />
            
            To place lines simply click on the intersections and ...</div>}
        </>
    
    )
}
