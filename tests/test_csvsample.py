from collections import Counter

from csvsample import csvsample


def test_random_sample():
    n = 100000
    source = ['a'] + [str(i) for i in range(n)]
    sample_rate = 0.1
    sample = list(csvsample.random_sample(source, sample_rate))[1:]
    n_sample = len(sample)

    assert abs(n_sample / n - sample_rate) < 0.01
    assert set(source).issuperset(sample)


def test_hash_sample():
    n = 100000
    source = ['a,b'] + [f'{int(i / 10)},{i}' for i in range(n)]
    sample_rate = 0.1
    sample = list(csvsample.hash_sample(source, sample_rate, 'a'))
    n_sample = len(sample)

    assert abs(n_sample / n - sample_rate) < 0.01
    assert set(source).issuperset(sample)

    counter = Counter(row.split(',')[0] for row in sample[1:])
    assert all(v == 10 for _, v in counter.items())


def test_reservoir_sample():
    n = 100000
    source = ['a'] + [str(i) for i in range(n)]
    sample_size = 10000
    sample = list(csvsample.reservoir_sample(source, sample_size))[1:]
    n_sample = len(sample)

    assert sample_size == n_sample
    assert set(source).issuperset(sample)
