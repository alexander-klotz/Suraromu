# use Node.js 18 image as base
FROM node:18-alpine

# set working directory
WORKDIR /app

# copy package.json file
COPY package.json .

# install dependencies
RUN npm install 

# copy the rest of the files
COPY . .

# expose port 80 for the web server
EXPOSE 3000

# start the web server
CMD [ "npm", "start" ]