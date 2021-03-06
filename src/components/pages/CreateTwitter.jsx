import React from 'react';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { TextField } from '@material-ui/core';
import Button from '@material-ui/core/Button';
import Copyright from '../Copyright';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Navbar from '../Navbar';

const drawerWidth = 240;
const color = "#55ACEE";

const useStyles = makeStyles((theme) => ({
    root: {
        display: 'flex',
    },
    paper: {
        marginTop: theme.spacing(8),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    content: {
        flexGrow: 1,
        height: '100vh',
        overflow: 'auto',
    },
    appBarSpacer: theme.mixins.toolbar,
    appBar: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: drawerWidth,
        background: color
    },
    form: {
        width: '100%',
        marginTop: theme.spacing(1),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
    title: {
        align: 'left'
    },
}));

export default function CreateTwitter() {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <CssBaseline />

            <AppBar position="fixed" className={classes.appBar}>
                <Toolbar>
                    <Typography variant="h6" noWrap>
                        Create Twitter Config
                    </Typography>
                </Toolbar>
            </AppBar>
            <Navbar />
            <main className={classes.content}>
                <div className={classes.appBarSpacer} />
                <Container maxWidth="xs" className={classes.container}>
                    <form className={classes.form} noValidate>
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="configName"
                            label="Config Name"
                            name="configName"
                            autoComplete="configName"
                            autoFocus
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="dbName"
                            label="Database Name"
                            name="dbName"
                            autoComplete="dbName"
                            autoFocus
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="feed"
                            label="Feed"
                            name="feed"
                            autoComplete="feed"
                            autoFocus
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="numTweet"
                            label="Number of tweets to search"
                            name="numTweet"
                            autoComplete="Number of tweets to search"
                            autoFocus
                        />
                        <TextField
                            variant="outlined"
                            margin="normal"
                            required
                            fullWidth
                            id="keywords"
                            label="Keywords"
                            name="keywords"
                            autoComplete="keywords"
                            autoFocus
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                        >
                            Create config
                    </Button>
                    </form>
                    <Copyright />
                </Container>
            </main>
        </div>
    )
}