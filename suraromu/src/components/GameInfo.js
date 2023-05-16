import React, { useState } from "react"
import { Tooltip } from '@mui/material';
import "./GameInfo.css"

const GameInfo = () => {
    
const [infoVisibility, setInfoVisibility] = useState(false);

    const showInfo = () => {
        setInfoVisibility(oldValue => !oldValue)
    };

    return(
        <>
            <Tooltip title="How to play">
                <button className="InfoButton" id="mydiv" onClick={showInfo}>?</button>
            </Tooltip>
            
            {infoVisibility && <div className="Info">The game consists of 3 main rules:<br />
            1. ASDfadsf<br />
            2. sdafsda<br />
            3. dasdfasd<br />
            
            To place lines simply click on the intersections and ...</div>}
        </>
    
    )
}

export default GameInfo
