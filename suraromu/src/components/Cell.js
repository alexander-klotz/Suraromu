import React, { useRef, useEffect } from 'react';
import $ from 'jquery';

export default function Cell(props) {

    const outerDivRef = useRef(null);
    let content = "";

    useEffect(() => {
        const outerDiv = $(outerDivRef.current);
        const pElement = outerDiv.find('p');

        const updateFontSize = () => {
            const fontSize = outerDiv.height();
            pElement.css('font-size', fontSize*0.7);
        };

        // Initial font-size update
        updateFontSize();

        // ResizeObserver
        const resizeObserver = new ResizeObserver(updateFontSize);
        resizeObserver.observe(outerDiv[0]);

        // Clean up the ResizeObserver on unmount
        return () => {
            resizeObserver.unobserve(outerDiv[0]);
            resizeObserver.disconnect();
        };
    }, []);


    // Type: normal=0 blocked=1 gateHori=2 gateVert=3 gateNumber=4 Start=5
    const classNames = ["cell", "blockedCell", "gateHoriCell", "gateVertCell", "gateNumberCell", "startCell"]
    const idx2D = [Math.floor(props.index/(props.puzzle.cols)), props.index%(props.puzzle.cols)]

    let vertiGateIdxs = []
    let horiGateIdxs = []
    for (let key in props.puzzle.gates) {
        if (key === '0') {
            // all the unordered gates
            for (let gateKey in props.puzzle.gates[key]) {
                const curGate = props.puzzle.gates[key][gateKey]
                const length = curGate.length
                if(curGate.orientation === "h"){
                    horiGateIdxs = horiGateIdxs.concat(Array.from({ length }, (_, index) => [curGate.startCell[0], curGate.startCell[1] + index]))
                }
                if(curGate.orientation === "v"){
                    vertiGateIdxs = vertiGateIdxs.concat(Array.from({ length }, (_, index) => [curGate.startCell[0] + index, curGate.startCell[1]]))
                }

            }
        } else {
            // all the ordered cells
            const curGate = props.puzzle.gates[key]
            const length = curGate.length
            if(curGate.orientation === "h"){
                horiGateIdxs = horiGateIdxs.concat(Array.from({ length }, (_, index) => [curGate.startCell[0], curGate.startCell[1] + index]))
            }
            if(curGate.orientation === "v"){
                vertiGateIdxs = vertiGateIdxs.concat(Array.from({ length }, (_, index) => [curGate.startCell[0] + index, curGate.startCell[1]]))
            }
            
        }
    }


    function getCellType(idx) {
        let type = 0

        if (props.puzzle.blockedCells.some(cell => JSON.stringify(cell) === JSON.stringify(idx))) {
            type = 1;
        } else if (props.puzzle.startCell[0] === idx[0] && props.puzzle.startCell[1] === idx[1]) {
            type = 5;
            content = countGates(props.puzzle.gates).toString();
        }else if (vertiGateIdxs.some(cell => JSON.stringify(cell) === JSON.stringify(idx))) {
            type = 3;
        }else if (horiGateIdxs.some(cell => JSON.stringify(cell) === JSON.stringify(idx))) {
                type = 2;
        } else {
            switch(gateNumberCell(idx)) {
                case "0":
                    type = 4;
                    break;
                case "":
                    break;
                default:
                    type = 4;    
                    content = gateNumberCell(idx)
                    break;
            }
        }

        return type
    }

    // returns string == blocked gate cell numbering ("0" for unnumbered and "" if it's a non gateNumberCell)
    function gateNumberCell(idx) {
        for (let key in props.puzzle.gates) {
            if (key === '0') {
                // all the unordered gates
                for (let gateKey in props.puzzle.gates[key]) {
                    const possibleGateCells = getBlockedGateCells(props.puzzle.gates[key][gateKey])
                    if(possibleGateCells.some(cell => JSON.stringify(cell) === JSON.stringify(idx))) {
                        return "0";
                    }
                }
            } else {
                // all the ordered cells
                const possibleGateCells = getBlockedGateCells(props.puzzle.gates[key])
                if(possibleGateCells.some(cell => JSON.stringify(cell) === JSON.stringify(idx))) {
                    return key.toString();
                }
            }
        }
        return ""
    }

    function getBlockedGateCells(gate) {
        const cells = []
        const row = gate.startCell[0]
        const col = gate.startCell[1]

        if(gate.orientation === "h") {
            cells.push([row, col-1])
            cells.push([row, col+gate.length])
        }else {
            cells.push([row-1, col])
            cells.push([row+gate.length, col])
        }

        return cells
    }


    function countGates(gatesObject) {
        let count = 0;
      
        for (const key in gatesObject) {
          if (key === '0') {
            // If the key is '0', count the number of objects in the array
            count += gatesObject[key].length;
          } else {
            count++;
          }
        }
      
        return count;
      }


    // TODO maybe try to get the hori and vert lines back to this to get them centered and also be able to set them to blocked
    return(
        <div ref={outerDivRef} key={props.index} className={classNames[getCellType(idx2D)]}>
            <p className={"cellText" + (getCellType(idx2D) === 5 ? "start" : "")}>{content}</p>
        </div>  
        
    )
}