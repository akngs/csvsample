import fire

from .csvsample import CLI, random_sample, hash_sample, reservoir_sample


def main():
    fire.Fire(CLI)
