FROM node:12.13.0-alpine as build-stage

# Create app directory
WORKDIR /app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json nginx.conf ./

RUN npm install
COPY . ./
RUN npm run build

FROM nginx:1.17.6
COPY --from=build-stage /app/dist/ /etc/nginx/html/
# Copy the default nginx.conf provided by tiangolo/node-frontend
COPY --from=build-stage /app/nginx.conf /etc/nginx/nginx.conf
RUN apt-get update && apt-get install -y curl && apt-get install -y iputils-ping
