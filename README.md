# Asset allocation calculator

This is a script that calculates monthly allocation percentages for a given list of assets and a given list of initial allocation percentages for each asset using a quantitative approach.

Developed and tested in Linux, using Python 3.8.0.


## WARNING

This script is **NOT INTENDED** to and MUST **NOT** be used  as investiment advisory or recommendation. It is made only with the purpose of study or curiosity.

## Author

- Inácio Medeiros (inaciogmedeiros@gmail.com)

## Setting up the project

Initially, clone this repository:

```bash
$ git clone https://github.com/inaciomdrs/Asset-Allocation-Calculator.git
$ cd Asset-Allocation-Calculator
```

Then, enter in the downloaded directory and create and activate a python virtualenv:

```bash
$ python -m venv .asset_allocation
$ source .asset_allocation/bin/activate
```

Next, install the project requirements:

```bash
(.asset_allocation) $ pip install -r requirements.txt
```

Now you are ready to run the script!

## Usage

Once you have set up the project, you can run using one of the following commands:

```bash
(.asset_allocation) $ python asset_allocation_calculator.py <list_of_assets>
```

Or 

```bash
(.asset_allocation) $ python asset_allocation_calculator.py <list_of_assets> --perc <list_of_percentages>
```

Where `<list_of_assets>` must be a list of valid tickers for [Yahoo Finance](https://finance.yahoo.com/). 

If `<list_of_percentages>` is not passed, the script will assume equal initial percentages for each asset.

### Usage example


Suppose you have a plan of allocating half of your investment capital in the [IVV](https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf) ETF and the other half in the [EWL](https://www.ishares.com/us/products/239685/ishares-msci-switzerland-capped-etf) ETF. To calculate which percentage of your investment capital should be spent in each ETF, run the command below. If the summation of percentages destined to IVV and EWL is not 100%, the rest is directed to Fixed Income. In the output below, each line is a month, and each column is the capital percentage to be allocated in each asset.


```bash
$ python asset_allocation_calculator.py IVV EWL
[*********************100%***********************]  1 of 1 completed
[*********************100%***********************]  1 of 1 completed

      IVV   EWL  Fixed Income
Jan   0.0   0.0         100.0
Fev   0.0   0.0         100.0
Mar   0.0   8.0          92.0
Abr  16.0  14.0          70.0
Mai   4.0   0.0          96.0
Jun   0.0   0.0         100.0
Jul   6.0   6.0          88.0
Ago   4.0   0.0          96.0
Set   0.0   0.0         100.0
Out   6.0   6.0          88.0
Nov  12.0  10.0          78.0
Dez   6.0  14.0          80.0
```