import Button from '@mui/material/Button';
import { createTheme, ThemeProvider } from '@mui/material/styles';

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
        <div style={{ display: 'flex', justifyContent: 'space-evenly' }}>
        <ThemeProvider theme={theme}>
            <Button
                onClick={() => handleChoiceClick(1)}
                variant={props.toolType === 1 ? 'contained' : 'outlined'}
            >
                Line
            </Button>
            <Button
                onClick={() => handleChoiceClick(2)}
                variant={props.toolType === 2 ? 'contained' : 'outlined'}
            >
                BlockLine
            </Button>
        </ThemeProvider>
        </div>
    );
};

export default Toolbar;
