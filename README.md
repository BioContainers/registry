BioContainers Web
==============================
[![Build Status](https://travis-ci.org/BioContainers/BioContainers.github.io.svg?branch=master)](https://travis-ci.org/BioContainers/BioContainers.github.io)


This project contains the [main page of biocontainers](https://biocontainers.pro) and the [registry page](https://biocontainers.pro/registry).


BioContainers Tool Registry
---------------------------------

This project provides a web UI for [BioContainers](https://biocontainers.pro)

* This application is written in JavaScript, and you can deploy this application easily.
* This application doesn't store any user data.
* You can find the necessary information simply from the Docker Registry [documentation](http://biocontainers.pro/docs/101/biocontainers-registry/).


How to Test
------------------------

- To test the application go to **dist** directory and install `npm install -g http-server`, then use `httop-server` to test the app:

```
http-server -o
```

We have already deployed this web-ui to our [github pages](http://worksap-ate.github.io/docker-registry-ui/#/).

- Please set your docker-registry IP at "Set Registry IP" option. 
- And you can use the Web UI.

How to Install to your own server
--------------------------------------

Download the source code and put these files to a web server.

- Show all biocontainers in dockerhub and quay.io.
- Search for containers using the **Search Box**
    * If user wants to search in the entire hub just like the docker hub, then he can use the search option given at the top. The phrase he wants to search for will search in the entire hub.
- Filter by word
- Sort
    * User can use the sort option to sort the items accorsing to the alphabetical order whether it is ascending or decending.
- Show the containers description.

Contributing
--------------------

Please for the master branch, create a PR and after accepting the PR your changes will be seen in http://biocontainers.pro