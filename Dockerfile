# Use Node.js 20
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the Docusaurus site
RUN npm run build

# Expose port
EXPOSE 3000

# Serve the built site
CMD ["npm", "run", "serve"]