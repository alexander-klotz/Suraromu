# Info
This application to play/solve/generate the logic puzzle Suraromu was the main focus of my bachelor thesis (contact me if you want access to the full thesis). You can either install this using Docker as described in the first part or manually installing the neccessary packages.
 
![Suraromu webpage](./examples/webpageView.PNG "Suraromu webpage")

# 1. Dockerized Version
The dockerized version has some issues with interrupting the solver and generator since docker does not support multiprocessing.

## 1.1 First step
First please install [Docker](https://www.docker.com/). 
This makes running this application much more convenient and saves you the time of having to install everything neccessary individually.

## 1.2 Install node modules
From the directory of this README file first move down into the suraromu folder. Then install the node modules using the second command
1. Change directory to `suraromu`:

    ```bash
    cd suraromu 
    ```

2. Install the node modules:

    ```bash
    npm install 
    ```


## 1.3 Front-end + Back-end build and run
Make sure you are in the same directory as this README file and the docker-compose.yaml and then run the following command:
```bash
docker-compose up
```
The first time this is executed it can take a few minutes since everything needs to be installed.

# 2. Manual install
This install process is more complex but should give the ability to properly terminate the solving/generation process.

## 2.1 Required software
First please make sure that atleast `python 3.11.5` is installed (ealier version might also work but were not tested). Additionally you will need to have `Node.js` and `npm` installed.

## 2.2 Install python packages
For the solver and generator to work you will have to install the neccessary python packages listed in the respective requirements.txt files. This can be done using the following commands:

1. Install python packages for the generator
    ```bash
    pip install -r ./generator/requirements.txt
    ```
2.  Install python packages for the solver 
    ```bash
    pip install -r ./solver/requirements.txt
    ```

## 2.3 Install node modules
From the directory of this README file first move down into the suraromu folder. Then install the node modules using the second command.
1. Change directory to `suraromu`:

    ```bash
    cd suraromu 
    ```
2. Install the node modules:

    ```bash
    npm install 
    ```


## 2.4 Front-end + Back-end build and run
It is recommended to start each component in a different shell. Additionally it's best to start the generator and solver first and then the front-end. However the front-end can be also run without the generator and solver.

1. Start solver:
    ```bash
    python -m uvicorn api:app --host 0.0.0.0 --port 5000 --reload
    ```
2. Start generator:
    ```bash
    python -m uvicorn api:app --host 0.0.0.0 --port 4000 --reload
    ```
3. Start React front-end:
    ```bash
    npm start
    ```


# 3. Playing the game

Once everything is successfully started up you should be able to reach the webapp in the browser of your choice via `localhost:3000`
The web-server might take some time to deploy fully deploy the first time.



