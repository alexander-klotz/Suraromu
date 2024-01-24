import Button from '@mui/material/Button';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CloseIcon from '@mui/icons-material/Close';
import TimelineIcon from '@mui/icons-material/Timeline';

const Toolbar = (props) => {

    const handleChoiceClick = (choice) => {
        props.setToolType(choice);
    };

    const theme = createTheme({
        
            palette: {
                primary: {
                    main: '#000',
                },
                secondary: {
                    main: '#111',
                },
            },
        
    })

    return (
        <div style={{ display: 'flex', justifyContent: 'space-evenly'}}>
        <ThemeProvider theme={theme}>
            <Button
                style={{marginLeft:"20%"}}
                onClick={() => handleChoiceClick(1)}
                variant={props.toolType === 1 ? 'contained' : 'outlined'}
            >
                <TimelineIcon style={{ color: 'green', paddingRight:"20%"}}/> Line
            </Button>
            <Button
                style={{marginRight:"20%"}}
                onClick={() => handleChoiceClick(2)}
                variant={props.toolType === 2 ? 'contained' : 'outlined'}
            >
                <CloseIcon style={{ color: 'red', paddingRight:"5%"}}/> BlockLine
            </Button>
        </ThemeProvider>
        </div>
    );
};

export default Toolbar;
