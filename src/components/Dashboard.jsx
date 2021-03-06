import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Copyright from './Copyright';
import Navbar from './Navbar';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
  },
  appBar: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    background: "#49392C"
  },
  appBarButtons: {
      marginLeft: 'auto',
      color: '#FFFFFF'
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    height: '100vh',
    overflow: 'auto',
  },
  container: {
    paddingTop: theme.spacing(4),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(10),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',

  },
  fixedHeight: {
    height: 240,
  },
}));

function getConfigs(){
    //get request for configs from user
    return [{ title: "T", links: 12, enabled: false }];
}

export default function Dashboard() {
  const classes = useStyles();

  const [configs, setConfigs] = useState([{ title: "T", links: 12, enabled: false }]);

  const resetConfigs = () => {
      setConfigs(oldArray => [getConfigs()]);
  };
  
  return (
    <div className={classes.root}>
      <CssBaseline />
      
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar>
          <Typography variant="h6" noWrap>
            Monke Scrapr
          </Typography>
          <Button className={classes.appBarButtons}>Logout</Button>
        </Toolbar>
      </AppBar>

      <Navbar />

      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container maxWidth="lg" className={classes.container}>
            <Grid container spacing={3}>
                {configs.map((item, index) =>{
                    return <Grid item xs={3} md={3} lg={4} key={index}><Paper elevation={5} className={classes.paper} key={index+"a"}>Data</Paper></Grid>
                })}
            </Grid>           
          <Copyright/>
        </Container>
      </main>
    </div>
  );
}