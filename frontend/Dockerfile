# Use Node.js LTS version as the base image
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy the entire frontend codebase
COPY . .

# Expose the port
EXPOSE 3000

# Start the development server
CMD ["npm", "start"]
