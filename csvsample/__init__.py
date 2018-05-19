import fire

from .csvsample import CLI, sample, sample_url


def main():
    fire.Fire(CLI)
