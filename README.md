# `docker-volumerename`

Docker CLI plugin to rename volumes.

## Requirements

- Docker for Mac
	- Docker >= 1.19.3
- Python 3

## Installation

```bash
mkdir ~/.docker/cli-plugins
cd ~/.docker/cli-plugins
curl -o docker-volumerename https://raw.githubusercontent.com/gh640/docker-volumerename/main/docker-volumerename.py
chmod u+x docker-volumerename
```

## Usage

```bash
docker volumerename [-h] [--dyr-run] volume_from volume_to
```

See detail with `docker volumerename --help`.
