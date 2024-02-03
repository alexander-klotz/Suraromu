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
            
            {infoVisibility && 
                <div className="Info" style={{display: 'flex', flexDirection: 'column'}}>
                    <button className="InfoButton" id="mydiv" onClick={showInfo}>x</button>
                    <h2 style={{fontWeight: 'bold', textDecoration: 'underline'}}>
                        The game consists of 4 main rules:
                    </h2>
                    <br/>
                    <p>
                        1. Create single loop that never crosses, branches or meets in a cell.<br />
                        2. The loop has to pass all „gates“ (connected dotted lines), but only once.<br />
                        3. Starting/end point of the loop is the cell with the circled number and it contains the number of gates that need to be traversed.<br />
                        4. Numbers next to gates denote the order of passing with no number meaning arbitrary position of this gate in the ordering.<br />
                    </p>
                    <p>
                        To place lines simply click on the intersections of two cells. To help with solving there is also the possibility to block intersections. 
                        To continuously draw hold 'd' on the keyboard while moving the mouse.
                    </p>
                </div>}
        </>
    
    )
}

export default GameInfo
