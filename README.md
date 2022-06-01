# JokerBot 🤖

**IMPORTANT!!!** You need to create a `.env` file in the root directory of this project and add a `DISCORD_TOKEN` to it.
###### .env
```
DISCORD_TOKEN=YOUR_TOKEN
```
## Install
#### Clone the repository (for production)
```
git clone --depth 1 https://github.com/JohannesTheiss/JokerBot 
```
### native Python
```
pip install -r requirements.txt
python run.py
```
### Docker
#### Start the docker daemon and container
```
sudo systemctl start docker
./build-docker.sh
```
##### Attach to the live logs of the container
```
docker attach --sig-proxy=false joker_bot
```
##### Stop the running docker container
```
docker container stop joker_bot
```
##### Start the installed docker container
```
docker run -v $PWD/logs:/app/logs -v $PWD/json:/app/json --detach --rm --name=joker_bot joker_bot
```

## Development
#### Clone the repository (for development)
```
git clone https://github.com/JohannesTheiss/JokerBot 
```
#### Create / update the `requirements.txt`
Install [`pipreqs`](https://github.com/bndr/pipreqs)
```
pip install pipreqs
pipreqs /path/to/project
```

#### Install CONDA env
```
conda env create -f environment.yml
conda activate discord
```

#### Build the docker images for another host (e.g. linux/arm/v7)
Run this docker image to get multi-arch support (https://github.com/multiarch/qemu-user-static)
```
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```
or you can install QEMU as static linked.
Create a new builder
```
docker buildx create --name piBuilder
docker buildx use piBuilder
docker buildx inspect --bootstrap
```

Build the image and load it to your local docker
```
docker buildx build --platform linux/arm/v7 --tag=joker_bot --load .
```

Create a tar with the new image
```
docker save joker_bot:latest > joker_bot_img.tar
```

Push the image to the other host and load it
```
docker load < joker_bot_img.tar
```

Create a new docker container with the JokerBot-Image
```
docker container create -v $PWD/logs:/app/logs -v $PWD/json:/app/json --rm --name=joker_bot joker_bot
```


##### Useful docker commands
```
# list all installed images
docker image ls -a

# list all installed container
docker container ls -a

# start the joker_bot container
docker container start joker_bot

# stop the joker_bot container
docker container stop joker_bot
```