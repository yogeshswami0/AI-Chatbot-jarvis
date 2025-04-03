import React, { useState, useEffect } from 'react';
import { 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton, 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  Container,
  TextField,
  Paper,
  CircularProgress,
  Button,
  Card,
  CardContent,
  Snackbar,
  Alert
} from '@mui/material';
import {
  Menu as MenuIcon,
  Mic as MicIcon,
  Settings as SettingsIcon,
  History as HistoryIcon,
  Send as SendIcon,
  PlayArrow as PlayIcon
} from '@mui/icons-material';
import axios from 'axios';
import { styled } from '@mui/material/styles';

const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

function App() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleStart = () => {
    setIsStarted(true);
    setChatHistory([{
      type: 'assistant',
      content: 'Hello! I am JARVIS, your AI assistant. How can I help you today?'
    }]);
  };

  useEffect(() => {
    // Check backend connection on component mount
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await axios.get('http://localhost:5000/health');
      setIsConnected(response.data.status === 'ok');
    } catch (error) {
      setIsConnected(false);
      setError('Cannot connect to the backend server. Please make sure it is running.');
    }
  };

  const handleSendMessage = async (text = message) => {
    if (!text.trim()) return;
    if (!isConnected) {
      setError('Cannot connect to the backend server. Please make sure it is running.');
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: text
      });

      if (response.data.status === 'success') {
        setChatHistory(prev => [...prev, 
          { type: 'user', content: text },
          { type: 'assistant', content: response.data.response }
        ]);
        setMessage('');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      if (error.response) {
        setError(`Server error: ${error.response.data.error || 'Failed to send message'}`);
      } else if (error.request) {
        setError('Cannot connect to the server. Please check if the backend is running.');
      } else {
        setError('Failed to send message. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceInput = async () => {
    if (!isConnected) {
      setError('Cannot connect to the backend server. Please make sure it is running.');
      return;
    }

    setIsListening(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/listen');
      if (response.data.status === 'success' && response.data.text) {
        setMessage(response.data.text);
        handleSendMessage(response.data.text);
      } else {
        setError('No speech detected. Please try again.');
      }
    } catch (error) {
      console.error('Error with voice input:', error);
      if (error.response) {
        setError(`Server error: ${error.response.data.error || 'Failed to recognize speech'}`);
      } else if (error.request) {
        setError('Cannot connect to the server. Please check if the backend is running.');
      } else {
        setError('Failed to recognize speech. Please try again.');
      }
    } finally {
      setIsListening(false);
    }
  };

  if (!isStarted) {
    return (
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)'
        }}
      >
        <Card sx={{ maxWidth: 400, p: 4 }}>
          <CardContent>
            <Typography variant="h4" component="h1" gutterBottom align="center">
              JARVIS AI Assistant
            </Typography>
            <Typography variant="body1" paragraph align="center">
              Your personal AI assistant ready to help you with any task.
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Button
                variant="contained"
                size="large"
                startIcon={<PlayIcon />}
                onClick={handleStart}
                sx={{
                  background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                  borderRadius: 3,
                  padding: '10px 30px'
                }}
              >
                Start JARVIS
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerToggle}
            edge="start"
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            JARVIS AI Assistant
          </Typography>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center',
            bgcolor: isConnected ? '#4caf50' : '#f44336',
            color: 'white',
            px: 2,
            py: 0.5,
            borderRadius: 1,
            fontSize: '0.875rem'
          }}>
            {isConnected ? 'Connected' : 'Disconnected'}
          </Box>
        </Toolbar>
      </AppBar>

      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
        variant="persistent"
        anchor="left"
        open={drawerOpen}
      >
        <Toolbar />
        <List>
          <ListItem button>
            <ListItemIcon>
              <HistoryIcon />
            </ListItemIcon>
            <ListItemText primary="Chat History" />
          </ListItem>
          <ListItem button>
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItem>
        </List>
      </Drawer>

      <Main open={drawerOpen}>
        <Toolbar />
        <Container maxWidth="md">
          <Paper 
            elevation={3} 
            sx={{ 
              p: 2, 
              mb: 2, 
              height: '60vh', 
              overflow: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: 2,
              background: '#f5f5f5'
            }}
          >
            {chatHistory.map((chat, index) => (
              <Box
                key={index}
                sx={{
                  display: 'flex',
                  justifyContent: chat.type === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <Paper
                  elevation={1}
                  sx={{
                    p: 2,
                    maxWidth: '70%',
                    bgcolor: chat.type === 'user' ? '#e3f2fd' : '#ffffff',
                    borderRadius: 2,
                  }}
                >
                  <Typography>{chat.content}</Typography>
                </Paper>
              </Box>
            ))}
            {isLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                <CircularProgress />
              </Box>
            )}
          </Paper>

          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                }
              }}
            />
            <IconButton 
              color="primary" 
              onClick={handleVoiceInput}
              disabled={isListening}
              sx={{
                bgcolor: isListening ? '#ffcdd2' : '#e3f2fd',
                '&:hover': {
                  bgcolor: isListening ? '#ffcdd2' : '#bbdefb',
                },
                animation: isListening ? 'pulse 1.5s infinite' : 'none',
                '@keyframes pulse': {
                  '0%': {
                    transform: 'scale(1)',
                  },
                  '50%': {
                    transform: 'scale(1.1)',
                  },
                  '100%': {
                    transform: 'scale(1)',
                  },
                },
              }}
            >
              <MicIcon />
            </IconButton>
            <IconButton 
              color="primary" 
              onClick={() => handleSendMessage()}
              disabled={isLoading || !message.trim()}
              sx={{
                bgcolor: '#e3f2fd',
                '&:hover': {
                  bgcolor: '#bbdefb',
                }
              }}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </Container>
      </Main>

      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setError(null)} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default App; 