# AI Programming
A simple tutorial to build and use (existing) AI Models.


# Running the System

```shell
    docker compose up --build
```

# Accessing the developing container

```shell
docker compose exec developing  /bin/bash
```

# Pulling and Creating llava model - For image understanding

```shell
make pull_llava
```

# Understanding an image

1. Copy a JPEG image into the images directory.

Then run:

```shell
make understand_image images/IMG_8965.JPG
```

# Run you own personal bot:

```shell
make personal_bot Adrian
```

# Advanced usage for Mac users:

1. install [brew](https://brew.sh/)
2. brew install ollama
3. ```ollama serve```
4. In another terminal
```shell
docker compose exec developing  /bin/bash
python developing/pull_llava/main.py --host host.docker.internal
python developing/understand_image/understand_image.py images/IMG_8965.JPG --host host.docker.internal
python developing/personal_bot/personal_bot.py images --person Adrian --host host.docker.internal
```
