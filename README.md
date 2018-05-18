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


### Install

You can install ``csvsample`` via ``pip``:

   pip install csvsample


### API

``csvsample.random_sample(lines, sample_rate, seed=None)`` performs random
sampling using pseudo random number generator:

    from csvsample import csvsample

    with open('input.csv', 'r') as i:
        with open('output.csv', 'w') as o:
            o.writelines(csvsample.random_sample(i, 0.1))

``csvsample.hash_sample(lines, sample_rate, column_name, seed=None)`` performs
hash-based sampling using extremely-fast hash function.

Let's say that instead of saving all users' log, you want to randomly select
10% of users and only save logs of those selected users. Simple random sampling
won't work. You can use hash-based sampling. "Consistent" nature of the
algorithm guarantees that any user ID selected once will always be selected
again:

    sample = csvsample.hash_sample(lines, 0.1, 'user_id')

``csvsample.reservoir_sample(line, sample_size, seed=None)`` performs reservoir
sampling. Let's say that you have an URL of 100GB csv file. Since you don't
have enough disk space, you just want to save small portion of sample which is
representative and unbiased.

[reservoir sampling](https://en.wikipedia.org/wiki/Reservoir_sampling) method
allows you to acquire random sample without saving entire data first:

    sample = csvsample.reservoir_sample(lines, 1000)

Now ``sample`` variable contains exactly 1,000 randomly selected lines.


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
