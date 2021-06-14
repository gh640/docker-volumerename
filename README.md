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

## Reference

- [Rename docker volume · Issue #31154 · moby/moby · GitHub](https://github.com/moby/moby/issues/31154)
- [CLI Plugins Design · Issue #1534 · docker/cli · GitHub](https://github.com/docker/cli/issues/1534)
- [cli-plugins: add concept of experimental plugin, only enabled in experimental mode by tiborvass · Pull Request #1898 · docker/cli · GitHub](https://github.com/docker/cli/pull/1898)
- [Basic framework for writing and running CLI plugins by ijc · Pull Request #1564 · docker/cli · GitHub](https://github.com/docker/cli/pull/1564)
