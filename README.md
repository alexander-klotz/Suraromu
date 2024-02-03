# Info
This application to play/solve/generate the logic puzzle Suraromu was the main focus of my bachelor project. 

# First step
First please install [Docker](https://www.docker.com/). 
This makes running this application much more convenient and saves you the time of having to install everything neccessary individually.

# Install node modules
From the directory of this README file first move down into the suraromu folder. Then install the node modules using the second command
1. Change directory to `suraromu`:

    ```bash
    cd suraromu 
    ```

2. Install the node modules:

    ```bash
    npm install 
    ```


# Front-end + Back-end build and run
Make sure you are in the same directory as this README file and the docker-compose.yaml and then run the following command:
```bash
docker-compose up
```
The first time this is executed it can take a few minutes since everything needs to be installed.

# Playing the game

Once everything is successfully started up you should be able to reach the webapp in the browser of your choice via `localhost:3000`
The web-server might take some more time to deploy once build since it's currently just the development build.
