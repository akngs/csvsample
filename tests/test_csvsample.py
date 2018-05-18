from collections import Counter

from csvsample.csvsample import random_sample, hash_sample, reservoir_sample


def test_random_sample():
    src = generate_csv(100000)
    sample_rate = 0.1
    sample = list(random_sample(src, sample_rate))[1:]

    # Check sample size
    assert abs(len(sample) / len(src) - sample_rate) < 0.01
    # Check elements
    assert set(src).issuperset(sample)


def test_hash_sample():
    src = generate_csv(100000)
    sample_rate = 0.1
    sample = list(hash_sample(src, sample_rate, 'a'))[1:]

    # Check sample size
    assert abs(len(sample) / len(src) - sample_rate) < 0.01
    # Check elements
    assert set(src).issuperset(sample)
    # Check consistency
    assert all(
        v == 10
        for v in Counter(row.split(',')[0] for row in sample).values()
    )


def test_reservoir_sample():
    src = generate_csv(100000)
    sample_size = 10000
    sample = list(reservoir_sample(src, sample_size))[1:]

    # Check sample size
    assert sample_size == len(sample)
    # Check elements
    assert set(src).issuperset(sample)


def test_sampling_rate_zero():
    src = generate_csv(100000)
    assert 0 == len(list(random_sample(src, 0))[1:])
    assert 0 == len(list(hash_sample(src, 0, 'a'))[1:])
    assert 0 == len(list(reservoir_sample(src, 0))[1:])


def test_sampling_rate_one():
    src = generate_csv(100000)
    assert src == list(random_sample(src, 1))
    assert src == list(hash_sample(src, 1, 'a'))
    assert src == list(reservoir_sample(src, len(src) - 1))


def test_seed():
    src = generate_csv(100000)
    no_seed_a = list(random_sample(src, 0.1))
    no_seed_b = list(random_sample(src, 0.1))
    seed0_a = list(random_sample(src, 0.1, 0))
    seed0_b = list(random_sample(src, 0.1, 0))
    seed1 = list(random_sample(src, 0.1, 1))
    assert no_seed_a != no_seed_b
    assert seed0_a == seed0_b
    assert seed0_a != seed1


def generate_csv(n):
    header = ['a,b']
    rows = [f'{int(i / 10)},{i}' for i in range(n)]
    return header + rows
