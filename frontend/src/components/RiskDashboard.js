import React, { useState } from 'react';
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
      </Box>
      <Typography variant="h6">Results:</Typography>
      <List>
        {results.map((item, index) => (
          <ListItem key={index}>
            <ListItemText primary={item.name} secondary={`Prediction: ${item.prediction}`} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default Dashboard;
