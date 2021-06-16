#!/usr/bin/env python3
"""Rename a volume"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

__vendor__ = 'Goto Hayato'
__version__ ='0.1.0'
COMMAND_NAME = 'volumerename'
METADATA_ARG = 'docker-cli-plugin-metadata'
IMAGE = 'busybox'


def main():
	parser = gen_parser()
	args = parser.parse_args(clean_argv(sys.argv))
	volume_from = args.volume_from
	volume_to = args.volume_to
	dry_run = args.dry_run

	if volume_from == METADATA_ARG:
		print(metadata())
		sys.exit()

	validate_args(parser, volume_from, volume_to)

	try:
		rename_volume(volume_from, volume_to, dry_run=dry_run)
	except subprocess.CalledProcessError as e:
		sys.exit(prettify_error(e))

	print(f'finished: {volume_from} -> {volume_to}')


def metadata() -> str:
	"""Returns the metadata string."""
	meta = {
		'SchemaVersion': '0.1.0',	
		'Vendor': __vendor__,
		'Version': __version__,
		'ShortDescription': __doc__,
		'URL': '',
	}
	return json.dumps(meta)


def validate_args(parser, volume_from: str, volume_to: Optional[str]):
	"""Validate CLI arguments."""
	if not volume_to:
		parser.print_help()
		sys.exit()

	if not volume_exists(volume_from):
		sys.exit(f'Volume `{volume_from}` not found.')

	if volume_used(volume_from):
		sys.exit(f'Volume `{volume_from}` is being used.')

	if volume_exists(volume_to):
		sys.exit(f'Volume `{volume_to}` already exists.')


def clean_argv(raw_argv: list[str]) -> list[str]:
	"""Remove script name and command name."""
	argv = raw_argv[:]

	if Path(argv[0]).name == Path(__file__).name: 
		argv.pop(0)

	if argv and argv[0] == COMMAND_NAME:
		argv.pop(0)

	return argv


def gen_parser():
	"""Generate parser."""
	parser = argparse.ArgumentParser(__doc__)
	parser.add_argument('volume_from')
	parser.add_argument('volume_to', nargs='?')
	parser.add_argument('--dry-run', action='store_true')
	return parser


def volume_exists(volume: str) -> bool:
	"""Check if a volume exists."""
	result = subprocess.run(['docker', 'volume', 'inspect', volume], capture_output=True)
	return result.returncode == 0


def volume_used(volume: str) -> bool:
	"""Check if a volume is being used."""
	result = subprocess.run([
		'docker', 
		'ps', 
		f'--filter=volume={volume}',
		'--quiet',
	], capture_output=True)
	return result.returncode == 0 and result.stdout.decode().rstrip() != ''


def rename_volume(volume_from: str, volume_to: str, *, dry_run: bool):
	"""Rename a volume."""
	print(f'[1/3] create volume: {volume_to}')
	create_volume(volume_to, dry_run=dry_run)

	print(f'[2/3] copy volume: {volume_from} -> {volume_to}')
	copy_volume(volume_from, volume_to, dry_run=dry_run)

	print(f'[3/3] delete volume: {volume_from}')
	delete_volume(volume_from, dry_run=dry_run)


def create_volume(volume: str, *, dry_run: bool):
	"""Create a volume."""
	return run(['docker', 'volume', 'create', volume], dry_run=dry_run)


def copy_volume(volume_from: str, volume_to: str, *, dry_run: bool):
	"""Copy volume content."""
	return run([
		'docker', 
		'run', 
		'--rm', 
		'-it', 
		'-v', 
		f'{volume_from}:/from',
		'-v', 
		f'{volume_to}:/to',
		IMAGE,
		'sh',
		'-c',
		'cd /from; cp -av . /to',
	], dry_run=dry_run)


def delete_volume(volume: str, *, dry_run: bool):
	"""Delete a volume."""
	return run(['docker', 'volume', 'rm', volume], dry_run=dry_run)


def run(args: list[str], *, dry_run: bool):
	"""Run a command."""
	if dry_run:
		print(f'(dry run: {args})')
		return
	return subprocess.run(args, check=True, capture_output=True)


def prettify_error(error) -> str:
	"""Prittify subprocess.CalledProcessError error."""
	return '\n'.join([
		f'command: {error.args[1]}',
		f'code: {error.returncode}',
		f'stdout: {error.stdout.decode().rstrip()}',
		f'stderr: {error.stderr.decode().rstrip()}',
	])


if __name__ =="__main__":
	main()
