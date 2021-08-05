# Pull latest official node image
FROM node:10

# Set working directory
WORKDIR /usr/src/app/frontend

# add `/app/node_modules/.bin` to environment variables
ENV PATH /app/node_modules/.bin:$PATH

# Copy package files and install app dependencies
COPY package.json ./

RUN npm install

# Expose ports
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]