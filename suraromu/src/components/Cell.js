import React, { useRef, useEffect } from 'react';
import $ from 'jquery';

export default function Cell(props) {

    const outerDivRef = useRef(null);

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


    const classNames = ["cell", "blockedCell", "gateHoriCell", "gateVertCell", "gateNumberCell", "startCell"]
    const idx2D = [Math.floor(props.index/(props.puzzle.cols)), props.index%(props.puzzle.cols)]

    function getCellType(idx) {
        let type = 0

        if (props.puzzle.blockedCells.some(cell => JSON.stringify(cell) === JSON.stringify(idx))) {
            type = 1;
        } else if (props.puzzle.startCell[0] === idx[0] && props.puzzle.startCell[1] === idx[1]) {
            type = 5;
        }
        return type
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

    function getCellContent(idx) {
        switch (getCellType(idx)) {
            case 5:
                return countGates(props.puzzle.gates).toString()
            default:
                return ""
          }
    } 

    
    return(
        <div ref={outerDivRef} key={props.index} className={classNames[getCellType(idx2D)]}>
            <p className={"cellText" + (getCellContent(idx2D)!==""?"start":"")}>{getCellContent(idx2D)}</p>
        </div>  
        
    )
}