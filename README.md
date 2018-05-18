## csvsample

``csvsample`` extracts some rows from CSV file to create randomly sampled CSV.

Features:

*   The size of population does not need to be specified beforehand. It means
    that the sampling process can be applied to data stream with unknown size
    such as system logs, no matter how large the amount of data is.
*   All methods accepts optional ``seed`` value. The same data set with the
    same sampling rate always yields exactly the same result, which is good
    for reproducibility.


Sampling methods:

*   ``csvsample.random_sample()`` performs random sampling using pseudo random
    number generator.
*   ``csvsample.hash_sample()`` performs hash-based sampling using
    extremely-fast hash function (xxhash)
*   ``csvsample.reservoir_sample()`` performs
    [reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling).
    It works by randomly choosing a sample of ``sample_size`` items from a list
    or a generator ``lines`` containing ``n`` items, where ``n`` is either a
    very large or unknown number.
