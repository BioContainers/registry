FROM node:5.11
RUN npm install -g grunt bower
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json /usr/src/app/
RUN npm install

COPY bower.json /usr/src/app/
RUN bower --allow-root install

COPY . /usr/src/app

CMD ["grunt", "build"]
