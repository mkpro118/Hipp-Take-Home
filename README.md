# Hipp-Take-Home
A Take Home exercise for Hipp Health

# Setup

- The recipe generator can be built locally if python, flask and openai are available.

- If docker is available, it can also be run as a docker container

## Requirements
- Needs a .env file to provide OpenAI API Key. The environment variable must be called `OpenAI_API_Key`.
- If running locally, needs `python`, `flask`, `openai`

## Setting up a local server

Run the following to setup a server
```bash
python3 app.py -fp <port> # -fp port is optional, defaults to 5000
```

Then navigate to [http://localhost:5000](http://localhost:5000) (change the port number here if you started the server with a different port)

## Setting up a server in a docker container

Note: this may take some time on the very first run to build the image.

Simply run
```bash
docker compose up -d
```
Then navigate to [http://localhost:80](http://localhost:80)
