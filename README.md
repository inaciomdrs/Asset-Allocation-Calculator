# Asset allocation calculator

This is a script that calculates monthly allocation percentages for a given list of assets and a given list of initial allocation percentages for each asset using a quantitative approach.

Developed and tested in Python 3.8.0.


## WARNING

This script is **NOT INTENDED** to and MUST **NOT** be used  as investiment advisory or recommendation. It is made only with the purpose of study or curiosity.

## Author

- Inácio Medeiros (inaciogmedeiros@gmail.com)

## Installation

- Create a python virtualenv
- Install  the requirements with `pip install -r requirements.txt`

## Usage

`python asset_allocation_calculator.py <list_of_assets>`

OR

`python asset_allocation_calculator.py <list_of_assets> --perc <list_of_percentages>`


Where `<list_of_assets>` must be a list of valid tickers for [Yahoo Finance](https://finance.yahoo.com/). 

If `<list_of_percentages>` is not passed, the script will assume equal initial percentages for each asset.

### Example

```
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

Each line is a month, and each column is the capital percentage to be allocated in each asset.