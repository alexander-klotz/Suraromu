
export default function Cell(props) {
    
    const classNames = ["cell", "blockedCell", "gateHoriCell", "gateVertCell", "gateNumberCell", "startCell"]
    return(
    <div key={props.index} className={classNames[props.type]}>
    </div>
    )
}