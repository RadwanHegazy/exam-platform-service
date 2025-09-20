# Use Node.js 22.14.0
FROM node:22.14.0

# Create app directory
WORKDIR /app

# Copy package files
COPY . .

# Install dependencies
RUN npm install


# Start the application
CMD ["npm", "run", "server"]