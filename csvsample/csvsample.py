import csv
import itertools
import random
from io import StringIO
from sys import stdin
from urllib import request
import xxhash


class CLI:
    @staticmethod
    def random(sample_rate, seed=None):
        yield from sample(stdin, 'random', sample_rate=sample_rate, seed=seed)

    @staticmethod
    def hash(sample_rate, col, seed=None):
        yield from sample(stdin, 'hash', col=col, sample_rate=sample_rate,
                          seed=seed)

    @staticmethod
    def reservoir(sample_size, seed=None):
        yield from sample(stdin, 'reservoir', sample_size=sample_size,
                          seed=seed)


def sample(lines, sampling_method, **kwargs):
    seed = kwargs.get('seed', None)

    if sampling_method == 'random':
        sample_rate = kwargs['sample_rate']
        sampler = random_sample(lines, sample_rate, seed)
    elif sampling_method == 'hash':
        sample_rate = kwargs['sample_rate']
        col = kwargs['col']
        sampler = hash_sample(lines, sample_rate, col, seed)
    elif sampling_method == 'reservoir':
        sample_size = kwargs['sample_size']
        sampler = reservoir_sample(lines, sample_size, seed)
    else:
        raise ValueError('Unknown method: ' + sampling_method)

    return Generator(sampler)


def sample_url(url, sampling_method, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    with request.urlopen(url) as f:
        lines = (l.decode(encoding) for l in f.readlines())
        return sample(lines, sampling_method, **kwargs)


class Generator:
    def __init__(self, generator):
        self._generator = generator

    def __iter__(self):
        return self._generator

    def to_buf(self):
        """Turn self into io.StringIO"""
        buf = StringIO()
        buf.writelines(row + '\n' for row in self)
        buf.seek(0)
        return buf


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


def hash_sample(lines, sample_rate, col, seed=None):
    """Performs hash-based sampling with given `sample_rate` by applying a hash
    function to columns in `col``, and returns generator containing sampled CSV.

    Sampling with the same `seed` always yields the same result.

    :param lines: list or generator of CSV rows
    :param sample_rate: sampling rate between 0.0 to 1.0
    :param col: name of column to apply hash function
    :param seed: initial seed value for hash function (default: random)
    """
    lines = (l.strip() for l in lines)
    lines_to_parse, lines_to_return = itertools.tee(lines, 2)

    # Header
    parsed = csv.reader(lines_to_parse)
    header = next(parsed)
    col_index = header.index(col)
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
