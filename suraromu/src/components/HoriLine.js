import CloseIcon from '@mui/icons-material/Close';

export default function HoriLine(props) {
    
    return(
    <div key={props.index} className="hori--line--hitbox" onClick={props.handleLineClick}>
        {props.isSet === 1 && <div className="hori--line"></div>}
        {props.isSet === 2 && 
            <div className="line--blocked" style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%'
              }}>
                <CloseIcon style={{ color: 'red' }}/>
            </div>}
        
    </div>
    )
}