## csvsample

``csvsample`` extracts some rows from CSV file to create randomly sampled CSV.

### Features

*   The size of original file does not need to be specified beforehand.
    It means that the sampling process can be applied to data stream with
    unknown size such as system logs, no matter how large the amount of data
    is.
*   All methods accepts optional ``seed`` value. The same data set with the
    same sampling rate always yields exactly the same result, which is good
    for reproducibility.


### Sampling methods

*   ``csvsample.random_sample()`` performs random sampling using pseudo random
    number generator.
*   ``csvsample.hash_sample()`` performs hash-based sampling using
    extremely-fast hash function (xxhash)
*   ``csvsample.reservoir_sample()`` performs
    [reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling).
    It works by randomly choosing a sample of ``sample_size`` items from a list
    or a generator ``lines`` containing ``n`` items, where ``n`` is either a
    very large or unknown number.


### Command-line interface

``csvsample`` alos provides command-line interface.

Following URL contains a CSV file from [DataHub](https://datahub.io/):

    > curl -sL https://bit.ly/2ItnHvK | head
    region,year,population
    WORLD,1950,2536274.721
    WORLD,1951,2583816.786
    WORLD,1952,2630584.384
    WORLD,1953,2677230.358

A number of rows including header is 18019:

    > curl -sL https://bit.ly/2ItnHvK | wc -l
    18019

Let's make 10% of random sample:

    > curl -sL https://bit.ly/2ItnHvK | csvsample random 0.1 > sample.csv

    > wc -l sample.csv
    1777 sample.csv

    > head -n 5 sample.csv
    region,year,population
    WORLD,1952,2630584.384
    WORLD,1972,3851545.181
    WORLD,1977,4229201.257
    WORLD,1988,5148556.956

You may use reservoir sampling method to obtain exact number of rows:

    > curl -sL https://bit.ly/2ItnHvK | csvsample reservoir 100 > sample.csv
    
    > wc -l sample.csv
    100 sample.csv
