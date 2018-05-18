import itertools
import random
from sys import stdin

import xxhash
import csv


class CLI:
    @staticmethod
    def random(sample_rate, seed=None):
        yield from random_sample(stdin, sample_rate, seed)

    @staticmethod
    def hash(sample_rate, colname, seed=None):
        yield from hash_sample(stdin, sample_rate, colname, seed)

    @staticmethod
    def reservoir(sample_size, seed=None):
        yield from reservoir_sample(stdin, sample_size, seed)


def random_sample(lines, sample_rate, seed=None):
    """Performs random sampling with given `sample_rate`, and returns generator
    containing sampled CSV.

    Sampling with the same `seed` always yields the same result.

    :param lines: list or generator of CSV rows
    :param sample_rate: sampling rate between 0.0 to 1.0
    :param seed: initial seed value for random function (default: random)
    """
    lines = (l.strip() for l in lines)

    # Header
    yield next(lines)

    # Rows
    rnd = random.Random(seed)
    for line in lines:
        if rnd.random() < sample_rate:
            yield line


def hash_sample(lines, sample_rate, colname, seed=None):
    """Performs hash-based sampling with given `sample_rate` by applying a hash
    function to columns in `colname``, and returns generator containing sampled
    CSV.

    Sampling with the same `seed` always yields the same result.

    :param lines: list or generator of CSV rows
    :param sample_rate: sampling rate between 0.0 to 1.0
    :param colname: name of column to apply hash function
    :param seed: initial seed value for hash function (default: random)
    """
    lines = (l.strip() for l in lines)
    lines_to_parse, lines_to_return = itertools.tee(lines, 2)

    # Header
    parsed = csv.reader(lines_to_parse)
    header = next(parsed)
    col_index = header.index(colname)
    yield next(lines_to_return)

    # Rows
    if seed is None:
        seed = random.randint(0, 0xFFFFFFFFFFFFFFFF)
    xxh = xxhash.xxh64('xxhash', seed=seed)

    for row, line in zip(parsed, lines_to_return):
        xxh.reset()
        xxh.update(row[col_index])
        if xxh.intdigest() / 0xFFFFFFFFFFFFFFFF < sample_rate:
            yield line


def reservoir_sample(lines, sample_size, seed=None):
    """Performs reservoir sampling with given `sample_size`, and returns
    generator containing sampled CSV.

    Sampling with the same `seed` always yields the same result.

    :param lines: list or generator of CSV rows
    :param sample_size: sample size
    :param seed: initial seed value for random function (default: random)
    """
    lines = (l.strip() for l in lines)
    lines = iter(lines)

    # Header
    yield next(lines)

    # Rows
    rnd = random.Random(seed)
    buckets = []

    # 1. Initial phase to fill reservoir
    k = 0
    try:
        for i in range(sample_size):
            buckets.append((k, next(lines)))
            k += 1
    except StopIteration:
        yield from (value for _, value in buckets)

    # 2. Probabilistic update
    for line in lines:
        position = rnd.randint(0, k)
        if position < sample_size:
            buckets[position] = (k, line)
        k += 1

    yield from (e[1] for e in sorted(buckets, key=lambda x: x[0]))
