
export default function Controls(props) {

    return (
        
        <div id="controls">

            <button className="controlButton">
                <span class="material-symbols-outlined">add_circle</span>
            </button>

            <button className="controlButton">
                <span class="material-symbols-outlined">check_circle</span>
            </button>

            <button className="controlButton">
                <span class="material-symbols-outlined">smart_toy</span>
            </button>

            <button className="controlButton">
                <span class="material-symbols-outlined" onClick={props.deleteFunction}>delete</span>
            </button>
        
        </div>
    )

}