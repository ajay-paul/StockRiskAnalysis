import React from 'react';
import { Container, Box } from '@mui/material';
import Header from './components/Header';
import Footer from './components/Footer';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Container maxWidth="lg">
      <Header />
      <Box my={4}>
        <Dashboard />
      </Box>
      <Footer />
    </Container>
  );
}

export default App;
