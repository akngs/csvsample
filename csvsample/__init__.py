import fire

from . import csvsample


def main():
    fire.Fire(csvsample.CLI)
