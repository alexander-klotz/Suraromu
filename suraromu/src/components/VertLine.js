import CloseIcon from '@mui/icons-material/Close';

export default function VertLine(props) {
    
    return(
    <div key={props.index} className="vert--line--hitbox" onClick={props.handleLineClick}>
        {props.isSet === 1 && <div className="vert--line"></div>}
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