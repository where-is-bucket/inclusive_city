# Stage 1: Build the application
FROM node:20.13.0 as builder

WORKDIR /usr/src/app

# Copy package files first for better caching
COPY app/package*.json ./
COPY app/vite.config.js ./

# Install dependencies
RUN npm install

# Copy all application files
COPY app .

# Build the application
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:stable

# Remove default nginx config
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY docker/nginx.conf /etc/nginx/conf.d

# Copy built files from builder stage
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]