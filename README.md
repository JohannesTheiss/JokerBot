# JokerBot 🤖

**IMPORTANT!!!** You need to create a `.env` file in the root directory of this project and add a `DISCORD_TOKEN` to it.
###### .env
```
DISCORD_TOKEN=YOUR_TOKEN
```
## Install
#### Clone the repository (for production)
```
$ git clone --depth 1 https://github.com/JohannesTheiss/JokerBot 
```
#### Start the docker daemon and container
```
$ sudo systemctl start docker
$ ./build-docker.sh
```
##### Attach to the live logs of the container
```
$ docker attach --sig-proxy=false joker_bot
```
##### Stop the running docker container
```
docker container stop joker_bot
```

## Development
#### Clone the repository (for development)
```
$ git clone https://github.com/JohannesTheiss/JokerBot 
```
#### Create / update the `requirements.txt`
Install [`pipreqs`](https://github.com/bndr/pipreqs)
```
$ pip install pipreqs
$ pipreqs /path/to/project
```

#### Install CONDA env
```
$ conda env create -f environment.yml
$ conda activate discord
```
