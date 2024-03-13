# Meter Parser Script

Refer to the assignment and specification files in [docs](docs/) folder.

Author: Justin Lee <<tzlee@tzlee.com>>

## Python Environment Setup

The Python version used in this script is 3.11.

The easiest way to set up a consistent Python environment is to
[install Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/),
and then create a Python 3.11 virtual environment:

    conda create -n meterparser python=3.11

Then activate the virtual environment:

    conda activate meterparser

Install the dependencies required:

    pip install -r requirements.txt

## Running the script

Example:

    python meter_parser.py -v -o sql sample.csv sample.sql

This will parse the input file `sample.csv` and generate the output file `sample.sql`.

To get more information:

    python meter_parser.py -h


## Unit tests

To run unit tests, run in the top level directory:

    python -m unittest

All unit tests are in the [test](test/) directory. Only the NEM12 parser is
tested. The other parts of the application are not due to limited time for
this assignment.

## Technical Decisions

### Language: Python

Python was selected for the purposes of this assignment for its ease of use
especially for quick text/file processing, and easy installation/execution on
most Operating Systems as it is unclear what type of environment it will be
used in.

### Style of Application: CLI Tool

For the purposes of this assignment, the script was designed as a simple
CLI-type tool, so it is easy to run and test, and also with the assumption
that the data files will reside in a directory after being uploaded via a
B2B FTP process.

The business logic classes in the `nem12parser` and `outputgenerator` modules
could easily be reused in, for example, a web service.

### Design patterns

The application is written in a typical layered architecture, with
[meter_parser.py](meter_parser.py) as the presentation layer,
[nem12parser](nem12parser/) module as the business layer, and
[outputgenerator](outputgenerator/) module as the persistence layer.

For purposes of this assignment, a sample CSV output generator (as a
replacement of the default SQL output generator) is provided to demonstrate
*Dependency Inversion*.

Also, Python lacks the notion of *Interfaces* (as in OO languages like Java or
C#), so the use of Abstract Base Classes (ABC) mimicks a similar concept.

### Other engineering decisions

The provided SQL `CREATE TABLE` query seems to suggest the DBMS it was taken
from was Postgres. For the purposes of this assignment, SQLite3 was used
instead to test. As a result, the `CREATE TABLE` query is slightly different:

    CREATE TABLE meter_readings (
        id INT PRIMARY KEY,
        nmi VARCHAR(10) NOT NULL,
        timestamp CHAR(19) NOT NULL,
        consumption NUMERIC NOT NULL,
        UNIQUE (nmi, timestamp)
    );

Also for the purposes of this assignment, the Primary Key is type `INT`,
however I recognize that a larger number space (e.g. `BIGINT`) or UUID type
as originally provided in the assignment will be needed in production.

In addition, the `nmi` column length has been increased to `VARCHAR(13)` to
accomodate the suffix, as it is unclear whether the `nmi_suffix` is part of
the `nmi` and if the values of the same time period should be added together.
The provided sample data has repeated data for the same time period, although
coincidentally also using the same interval. It can not be assumed that the
intervals remain the same in other data files, so I did not perform any
further aggregation. I am unable to discern this detail from the
specificiations sheet: I might need deeper understanding or context of the
Energy Market industry.

Also since most DBMSes are unlikely to change, the SQL queries generated are
designed to generate multi-row `INSERT` for better performance and smaller
queries. The generated SQL should work for most SQL engines (including
Postgres and MySQL). However, some engines, e.g. Oracle requires a different
query format for `DATETIME`. If the DBMS is expected to change, then using an
ORM may be better, but may impact performance.

## Additional Notes

I did try to read the [Technical Delivery Specification](https://www.aemo.com.au/-/media/files/electricity/nem/retail_and_metering/b2b/b2b-procedure-technical-delivery-specification-v31.pdf)
to understand the delivery mechanism but I think there are alot of context required to
understand the entire document, such as what the entire payload of an aseXML message
looks like, and what many (industry-specific) abbreviations mean. Given the time constraints
around this take-home assignment, I was not able to fully research these information.

