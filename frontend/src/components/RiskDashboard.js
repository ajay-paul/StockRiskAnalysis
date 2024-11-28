import React, { useEffect, useState } from 'react';
import {
  TextField,
  Button,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Box,
} from '@mui/material';

const Dashboard = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [notifications, setNotifications] = useState([]);

  // Establish WebSocket connection for real-time notifications
  useEffect(() => {
    const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications((prevNotifications) => [...prevNotifications, data.message]);
    };

    return () => {
      socket.close();
    };
  }, []);

  // Fetch data for a specific query
  const fetchData = async () => {
    try {
      const response = await fetch('/api/data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Fetch predictions for the watchlist
  const fetchWatchlistPredictions = async () => {
    try {
      const response = await fetch('/api/watchlist-predictions', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
      });
      const data = await response.json();
      setResults(data.predictions || []);
    } catch (error) {
      console.error('Error fetching watchlist predictions:', error);
    }
  };

  return (
    <Paper elevation={3} style={{ padding: '20px' }}>
      <Typography variant="h5" gutterBottom>
        Stock Prediction Dashboard
      </Typography>
      <Box display="flex" gap="16px" mb={2}>
        <TextField
          fullWidth
          label="Enter stock symbol or query"
          variant="outlined"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={fetchData}>
          Search
        </Button>
        <Button variant="contained" color="secondary" onClick={fetchWatchlistPredictions}>
          Predict Watchlist
        </Button>
      </Box>

      <Typography variant="h6" gutterBottom>
        Results:
      </Typography>
      <List>
        {results.map((item, index) => (
          <ListItem key={index}>
            <ListItemText
              primary={item.stock_symbol || item.name}
              secondary={`Prediction: ${item.prediction}`}
            />
          </ListItem>
        ))}
      </List>

      <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
        Notifications:
      </Typography>
      <List>
        {notifications.map((notif, index) => (
          <ListItem key={index}>
            <ListItemText primary={notif} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default Dashboard;
