# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 14:08:57

## Overall Strategy Performance

| strategy          |   ('total_return', 'mean') |   ('total_return', 'std') |   ('sharpe_ratio', 'mean') |   ('sharpe_ratio', 'std') |   ('win_rate', 'mean') |   ('win_rate', 'std') |   ('profit_factor', 'mean') |   ('profit_factor', 'std') |   ('recovery_factor', 'mean') |   ('recovery_factor', 'std') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:------------------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|-----------------------:|----------------------:|----------------------------:|---------------------------:|------------------------------:|-----------------------------:|------------------------:|-----------------------------:|----------------------------:|
| AdaptiveBollinger |                0.0026      |               0.0217      |                0.0542      |               1.1123      |                 0.0939 |                0.1462 |                    inf      |                   nan      |                      inf      |                     nan      |                     343 |                       1.6801 |                     25.2008 |
| AdaptiveMACD      |                0.0531      |               0.1338      |                0.469       |               1.2212      |                 0.1523 |                0.2233 |                    inf      |                   nan      |                      inf      |                     nan      |                    1920 |                       1.6729 |                     25.0928 |
| Bollinger         |                8.01885e+40 |               3.10569e+41 |                2.82228e+39 |               1.09306e+40 |                 0.3408 |                0.2163 |                    inf      |                   nan      |                      inf      |                     nan      |                    1919 |                       0.008  |                      0.12   |
| BuyAndHold        |                6.3463      |               6.7649      |                8.42349e+08 |               3.25152e+09 |                 0      |                0      |                      2.2413 |                     1.0019 |                       17.2347 |                      15.7055 |                      15 |                       0.0018 |                      0.0264 |
| MACD              |               -0.0061      |               1.4545      |                5.42614e+06 |               2.10153e+07 |                 0.2067 |                0.1565 |                    inf      |                   nan      |                      inf      |                     nan      |                     526 |                       0.0117 |                      0.176  |

## Performance by Cryptocurrency

### BTC-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0265 |   -1.535       |     0.3288 |          0.5987 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |        inf      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |        inf      |
| ('AdaptiveMACD', 'D')      |         0.1694 |    2.2127      |     0.4841 |          1.2645 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |        inf      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |        inf      |
| ('Bollinger', 'D')         |        -1.0373 |   -0.0474      |     0.4564 |          0.7703 |
| ('Bollinger', 'M')         |        -0.4308 |   -0.7922      |     0      |          0      |
| ('Bollinger', 'W')         |        -1      |   -0.0883      |     0.4375 |          0.5656 |
| ('BuyAndHold', 'D')        |         5.0662 |   12.4383      |     0      |          1.3814 |
| ('BuyAndHold', 'M')        |         3.3585 |    4.27567e+06 |     0      |          4.26   |
| ('BuyAndHold', 'W')        |         5.0662 |   75.9434      |     0      |          2.3123 |
| ('MACD', 'D')              |        -0.5969 |   -1.9643      |     0.2083 |          0.7986 |
| ('MACD', 'M')              |         0      |    0           |     0      |        inf      |
| ('MACD', 'W')              |        -0.4134 |   -1.0366      |     0.4091 |          0.6779 |

### ETH-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |         0.0183 |         1.802  |     0.3269 |          1.8141 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |        inf      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |        inf      |
| ('AdaptiveMACD', 'D')      |         0.0972 |         1.3453 |     0.453  |          1.1622 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |        inf      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |        inf      |
| ('Bollinger', 'D')         |        -1      |        -0.0495 |     0.4358 |          0.8846 |
| ('Bollinger', 'M')         |        -0.0701 |        -2.3656 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.9966 |        -0.1079 |     0.4286 |          1.0163 |
| ('BuyAndHold', 'D')        |         2.302  |         4.8872 |     0      |          1.2275 |
| ('BuyAndHold', 'M')        |         1.4995 |      8608.97   |     0      |          2.65   |
| ('BuyAndHold', 'W')        |         2.302  |        14.5578 |     0      |          1.656  |
| ('MACD', 'D')              |        -0.5661 |        -1.69   |     0.1948 |          0.8268 |
| ('MACD', 'M')              |        -0.473  |        -0.6382 |     0      |          0      |
| ('MACD', 'W')              |        -0.3445 |        -0.6791 |     0.45   |          0.8664 |

### XRP-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |         0.0725 |    2.9592      |     0.3387 |          3.0575 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |        inf      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |        inf      |
| ('AdaptiveMACD', 'D')      |         0.495  |    3.821       |     0.4742 |          1.7821 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |        inf      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |        inf      |
| ('Bollinger', 'D')         |        -1.0019 |   -0.1122      |     0.5075 |          1.8519 |
| ('Bollinger', 'M')         |        -0.256  |   -1.1341      |     0      |          0      |
| ('Bollinger', 'W')         |        -0.9987 |   -0.1885      |     0.5667 |          0.7747 |
| ('BuyAndHold', 'D')        |         6.2078 |    8.3773      |     0      |          1.351  |
| ('BuyAndHold', 'M')        |         5.0083 |    3.51115e+07 |     0      |          3.8681 |
| ('BuyAndHold', 'W')        |         6.2078 |   59.2588      |     0      |          2.0987 |
| ('MACD', 'D')              |        -0.7501 |   -1.388       |     0.0769 |          0.8428 |
| ('MACD', 'M')              |         0.2077 |    2.8254      |     0.3333 |          1.5036 |
| ('MACD', 'W')              |        -0.9653 |   -0.5874      |     0.2353 |          0.24   |

### SOL-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |   -0.0056      |   -0.9914      |     0.1176 |          0.4189 |
| ('AdaptiveBollinger', 'M') |    0           |    0           |     0      |        inf      |
| ('AdaptiveBollinger', 'W') |    0           |    0           |     0      |        inf      |
| ('AdaptiveMACD', 'D')      |   -0.0498      |   -1.3575      |     0.4196 |          0.771  |
| ('AdaptiveMACD', 'M')      |    0           |    0           |     0      |        inf      |
| ('AdaptiveMACD', 'W')      |    0           |    0           |     0      |        inf      |
| ('Bollinger', 'D')         |    1.20283e+42 |    4.23342e+40 |     0.4548 |          0.8447 |
| ('Bollinger', 'M')         |    0.0271      |    3.7955      |     0.5    |        inf      |
| ('Bollinger', 'W')         |    1.52187e+06 |    7.02688e+13 |     0.3947 |          0.606  |
| ('BuyAndHold', 'D')        |   22.1705      |   29.1803      |     0      |          1.3753 |
| ('BuyAndHold', 'M')        |    8.6563      |    1.25958e+10 |     0      |          3.6263 |
| ('BuyAndHold', 'W')        |   22.1705      |  968.566       |     0      |          2.2007 |
| ('MACD', 'D')              |   -0.6559      |   -1.3966      |     0.3039 |          0.8752 |
| ('MACD', 'M')              |    5.0046      |    8.1392e+07  |     0      |          4.2435 |
| ('MACD', 'W')              |   -0.8181      |   -0.6992      |     0.3478 |          0.5758 |

### BNB-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.019  |        -1.4218 |     0.2969 |          0.6668 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |        inf      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |        inf      |
| ('AdaptiveMACD', 'D')      |         0.0853 |         1.0142 |     0.4531 |          1.1359 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |        inf      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |        inf      |
| ('Bollinger', 'D')         |        -1      |        -0.0702 |     0.4722 |          0.8754 |
| ('Bollinger', 'M')         |        -0.3144 |        -1.2851 |     0      |          0      |
| ('Bollinger', 'W')         |        -1      |        -0.0978 |     0.4583 |          0.7525 |
| ('BuyAndHold', 'D')        |         1.9402 |         4.4816 |     0      |          1.2229 |
| ('BuyAndHold', 'M')        |         1.298  |      3520.15   |     0      |          2.707  |
| ('BuyAndHold', 'W')        |         1.9402 |        11.8262 |     0      |          1.6822 |
| ('MACD', 'D')              |        -0.4965 |        -1.7368 |     0.2553 |          0.8361 |
| ('MACD', 'M')              |         0.7014 |       148.155  |     0      |          2.5873 |
| ('MACD', 'W')              |         0.0752 |         0.269  |     0.2857 |          1.1714 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    1.20283e+42 |
| Bollinger  | SOL-USD  | W           |    1.52187e+06 |
| BuyAndHold | SOL-USD  | D           |   22.1705      |
| BuyAndHold | SOL-USD  | W           |   22.1705      |
| BuyAndHold | SOL-USD  | M           |    8.65628     |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |   sharpe_ratio |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    4.23342e+40 |
| Bollinger  | SOL-USD  | W           |    7.02688e+13 |
| BuyAndHold | SOL-USD  | M           |    1.25958e+10 |
| MACD       | SOL-USD  | M           |    8.1392e+07  |
| BuyAndHold | XRP-USD  | M           |    3.51115e+07 |

### By win_rate
| strategy     | symbol   | timeframe   |   win_rate |
|:-------------|:---------|:------------|-----------:|
| Bollinger    | XRP-USD  | W           |   0.566667 |
| Bollinger    | XRP-USD  | D           |   0.507508 |
| Bollinger    | SOL-USD  | M           |   0.5      |
| AdaptiveMACD | BTC-USD  | D           |   0.484127 |
| AdaptiveMACD | XRP-USD  | D           |   0.474227 |

### By profit_factor
| strategy          | symbol   | timeframe   |   profit_factor |
|:------------------|:---------|:------------|----------------:|
| AdaptiveMACD      | BTC-USD  | W           |             inf |
| AdaptiveBollinger | BTC-USD  | W           |             inf |
| AdaptiveMACD      | BTC-USD  | M           |             inf |
| AdaptiveBollinger | BTC-USD  | M           |             inf |
| MACD              | BTC-USD  | M           |             inf |

## Strategy Analysis

### Risk-Adjusted Returns
| strategy          |   sharpe_ratio |   max_drawdown |   recovery_factor |
|:------------------|---------------:|---------------:|------------------:|
| AdaptiveBollinger |    0.0542      |        -0.007  |          inf      |
| AdaptiveMACD      |    0.469       |        -0.0254 |          inf      |
| Bollinger         |    2.82228e+39 |       -24.4558 |          inf      |
| BuyAndHold        |    8.42349e+08 |        -0.3674 |           17.2347 |
| MACD              |    5.42614e+06 |        -0.5071 |          inf      |

### Trading Efficiency
| strategy          |   ('win_rate', 'mean') |   ('profit_factor', 'mean') |   ('num_trades', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |
|:------------------|-----------------------:|----------------------------:|-------------------------:|------------------------:|-----------------------------:|
| AdaptiveBollinger |                 0.0939 |                    inf      |                  22.8667 |                     343 |                       1.6801 |
| AdaptiveMACD      |                 0.1523 |                    inf      |                 128      |                    1920 |                       1.6729 |
| Bollinger         |                 0.3408 |                    inf      |                 127.933  |                    1919 |                       0.008  |
| BuyAndHold        |                 0      |                      2.2413 |                   1      |                      15 |                       0.0018 |
| MACD              |                 0.2067 |                    inf      |                  35.0667 |                     526 |                       0.0117 |

### Performance by Timeframe
|                            |     total_return |   sharpe_ratio |   win_rate |
|:---------------------------|-----------------:|---------------:|-----------:|
| ('AdaptiveBollinger', 'D') |      0.0079      |    0.1626      |     0.2818 |
| ('AdaptiveBollinger', 'M') |      0           |    0           |     0      |
| ('AdaptiveBollinger', 'W') |      0           |    0           |     0      |
| ('AdaptiveMACD', 'D')      |      0.1594      |    1.4071      |     0.4568 |
| ('AdaptiveMACD', 'M')      |      0           |    0           |     0      |
| ('AdaptiveMACD', 'W')      |      0           |    0           |     0      |
| ('Bollinger', 'D')         |      2.40565e+41 |    8.46684e+39 |     0.4653 |
| ('Bollinger', 'M')         |     -0.2088      |   -0.3563      |     0.1    |
| ('Bollinger', 'W')         | 304373           |    1.40538e+13 |     0.4572 |
| ('BuyAndHold', 'D')        |      7.5374      |   11.8729      |     0      |
| ('BuyAndHold', 'M')        |      3.9641      |    2.52705e+09 |     0      |
| ('BuyAndHold', 'W')        |      7.5374      |  226.03        |     0      |
| ('MACD', 'D')              |     -0.6131      |   -1.6351      |     0.2079 |
| ('MACD', 'M')              |      1.0881      |    1.62784e+07 |     0.0667 |
| ('MACD', 'W')              |     -0.4932      |   -0.5466      |     0.3456 |

