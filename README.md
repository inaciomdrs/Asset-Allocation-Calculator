# Asset allocation calculator

This is the repository of a script that calculates monthly allocation percentages for a given list of assets and a given list of initial allocation percentages for each asset using a quantitative approach.

Developed and tested in Linux, using Python 3.8.0.


## WARNING

The script is **NOT INTENDED** to and **MUST <u>NOT</u>** be used  as investiment advisory or recommendation. It is made only with the purpose of study or curiosity.

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


## How it works


The script receives a list of assets and (optionally) a list of 
initial percentages, each percentage corresponding respectively
to each asset. If no percentages are given, the script assume
that each asset have an equal percentage (neutral allocation).
The following steps are performed for each asset separately and
individually. Final results are then merged in a single "table",
which is printed on the screen.


**Step 1: Download data**

The script initially downloads dialy OHLC (Open, High, Low, Close) data for each
asset from 2000-01-01 to "today". If the asset does not have data available for
2000-01-01, it takes from the earliest possible date.


**Step 2: Metrics calculation**

Once the data is available, the script then calculates, for each month of each
year, the percentual variation from the close of first day to the close of the
last day.


Theses percentual numbers are then grouped by month (for example,
there will be a group of percentual variations for January from each year, another
one for February etc.), ordered by year. Next, (Mathematical Expectation)[https://www.quora.com/How-can-we-find-a-mathematical-expectation-for-a-trading-strategy], (Maximum Drawdown)[https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp] and (Kelly Criterion)[https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/kelly-criterion/] (among other metrics) are calculated for each group.


**Step 3: Percentages definition**

Now we have 12 groups, each one regarding a specific month, and each one with their own metrics.
The percentages definitions for each month runs as follows: if a given month has Mathematical
Expectation lower than zero or a Maximum Drawdown higher or equal than the average month
one, then the percentage associated to that month will be zero. If this is not the case,
the percentage that will be given is the fraction of initial percentage given to the asset 
corresponding to half-Kelly Criterion percent. For example, suppose that the initial percentage
given to an asset was 60%, and that Kelly Criterion for January is 40%. Thus, the percent allocation
for the asset in January will be 12% (20% of 60%).


**Step 4: Percentages definition**

Suppose you are working with more than one asset, and the summation of defined percentages for a 
given month is less than 100%. In this case, the script will "put the rest" in "Fixed Income".


## Usage example


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