from collections import Counter

from csvsample import sample


def test_random_sample():
    src = generate_csv(100000)
    sample_rate = 0.1
    sampled = list(sample(src, 'random', sample_rate=sample_rate))[1:]

    # Check sample size
    assert abs(len(sampled) / len(src) - sample_rate) < 0.01
    # Check elements
    assert set(src).issuperset(sampled)


def test_hash_sample():
    src = generate_csv(100000)
    sample_rate = 0.1
    sampled = list(sample(src, 'hash', sample_rate=sample_rate, col='a'))[1:]

    # Check sample size
    assert abs(len(sampled) / len(src) - sample_rate) < 0.01
    # Check elements
    assert set(src).issuperset(sampled)
    # Check consistency
    assert all(
        v == 10
        for v in Counter(row.split(',')[0] for row in sampled).values()
    )


def test_reservoir_sample():
    src = generate_csv(100000)
    sample_size = 10000
    sampled = list(sample(src, 'reservoir', sample_size=sample_size))[1:]

    # Check sample size
    assert sample_size == len(sampled)
    # Check elements
    assert set(src).issuperset(sampled)


def test_sampling_rate_zero():
    src = generate_csv(100000)
    assert 0 == len(list(sample(src, 'random', sample_rate=0))[1:])
    assert 0 == len(list(sample(src, 'hash', sample_rate=0, col='a'))[1:])
    assert 0 == len(list(sample(src, 'reservoir', sample_size=0))[1:])


def test_sampling_rate_one():
    src = generate_csv(100000)
    assert src == list(sample(src, 'random', sample_rate=1))
    assert src == list(sample(src, 'hash', sample_rate=1, col='a'))
    assert src == list(sample(src, 'reservoir', sample_size=len(src) - 1))


def test_seed():
    src = generate_csv(100000)
    no_seed_a = list(sample(src, 'random', sample_rate=0.1))
    no_seed_b = list(sample(src, 'random', sample_rate=0.1))
    seed0_a = list(sample(src, 'random', sample_rate=0.1, seed=0))
    seed0_b = list(sample(src, 'random', sample_rate=0.1, seed=0))
    seed1 = list(sample(src, 'random', sample_rate=0.1, seed=1))
    assert no_seed_a != no_seed_b
    assert seed0_a == seed0_b
    assert seed0_a != seed1


def test_to_buf():
    src = generate_csv(100000)
    buf = sample(src, 'random', sample_rate=0.1).to_buf()
    assert src[0] + '\n' == buf.readline()


def generate_csv(n):
    header = ['a,b']
    rows = [f'{int(i / 10)},{i}' for i in range(n)]
    return header + rows
