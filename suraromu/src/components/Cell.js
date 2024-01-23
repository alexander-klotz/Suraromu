import React, { useRef, useEffect} from 'react';


export default function Cell(props) {

    const outerDivRef = useRef(null);
    let content = "";
    // Type: normal=0 blocked=1 gateHori=2 gateVert=3 gateNumber=4 Start=5
    const classNames = ["cell", "blockedCell", "gateHoriCell", "gateVertCell", "gateNumberCell", "startCell"]
    const idx2D = [Math.floor(props.index/(props.puzzle.cols)), props.index%(props.puzzle.cols)]
    getCellType(idx2D)
    

    const handleMouseDown = event => {
        props.setquickDraw({ isMouseDown: true, prevCell: props.index });
        //console.log(`Mouse down at cell: ${props.index}`);
    };

    const handleMouseUp = (e) => {
        props.setquickDraw({ isMouseDown: false });
    };

    const handleMouseEnter = (e) => {
        if (props.quickDraw.isMouseDown) {
            //console.log(`Moved from cell ${props.quickDraw.prevCell} to ${props.index}`);
            props.setquickDraw({ prevCell: props.index });
        }
    };

    
    // TODO: maybe make this fixed by calculating it in the Grid.js
    useEffect(() => {
        const outerDiv = outerDivRef.current;
        const pElement = outerDiv.querySelector('p');
        let count = content.split("/").length
        const updateFontSize = () => {
            const fontSize = outerDiv.offsetHeight;
            pElement.style.fontSize = `${fontSize * 0.6/count}px`;
        };
        updateFontSize();

        const resizeObserver = new ResizeObserver(updateFontSize);
        resizeObserver.observe(outerDiv);

        return () => {
            resizeObserver.unobserve(outerDiv);
            resizeObserver.disconnect();
        };
    }, [content]);
    

    function getCellType(idx) {
        let type = 0

        if (props.puzzle.blockedCells.some(cell => cell.length === idx.length && cell.every((value, index) => value === idx[index]))) {
            type = 1;
        } else if (props.puzzle.startCell[0] === idx[0] && props.puzzle.startCell[1] === idx[1]) {
            type = 5;
            content = countGates(props.puzzle.gates).toString();
        } else if (props.vertiGateIdxs.some(cell => cell.length === idx.length && cell.every((value, index) => value === idx[index]))) {
            type = 3;
        } else if (props.horiGateIdxs.some(cell => cell.length === idx.length && cell.every((value, index) => value === idx[index]))) {
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
        return props.gateGrid[idx[0]][idx[1]]
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


    return(
        <div ref={outerDivRef} key={props.index} className={classNames[getCellType(idx2D)]} 
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onMouseEnter={handleMouseEnter}
        >
            <p className={"cellText" + (getCellType(idx2D) === 5 ? "start" : "")}>{content}</p>
        </div>  
        
    )
}