FROM node:16-alpine as build

WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy build output from previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy custom Nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 