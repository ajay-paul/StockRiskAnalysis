import React from 'react';
import { Typography, Box } from '@mui/material';

const Footer = () => {
  return (
    <Box mt={4} textAlign="center" py={2} bgcolor="#f4f4f4">
      <Typography variant="body2" color="textSecondary">
        © 2024 Stock Risk Analysis. All rights reserved.
      </Typography>
    </Box>
  );
};

export default Footer;
