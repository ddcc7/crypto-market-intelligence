# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 14:06:43

## Overall Strategy Performance

| strategy   |   ('total_return', 'mean') |   ('total_return', 'std') |   ('sharpe_ratio', 'mean') |   ('sharpe_ratio', 'std') |   ('win_rate', 'mean') |   ('win_rate', 'std') |   ('profit_factor', 'mean') |   ('profit_factor', 'std') |   ('recovery_factor', 'mean') |   ('recovery_factor', 'std') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:-----------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|-----------------------:|----------------------:|----------------------------:|---------------------------:|------------------------------:|-----------------------------:|------------------------:|-----------------------------:|----------------------------:|
| Bollinger  |                8.30699e+40 |               3.21729e+41 |                2.92367e+39 |               1.13233e+40 |                 0.3408 |                0.2163 |                     inf     |                    nan     |                      inf      |                     nan      |                    1919 |                       0.009  |                      0.1352 |
| BuyAndHold |                6.3461      |               6.7676      |                8.441e+08   |               3.25821e+09 |                 0      |                0      |                       2.241 |                      1.002 |                       17.2341 |                      15.7124 |                      15 |                       0.002  |                      0.0293 |
| MACD       |               -0.0058      |               1.4548      |                5.43733e+06 |               2.10587e+07 |                 0.2067 |                0.1565 |                     inf     |                    nan     |                      inf      |                     nan      |                     526 |                       0.0085 |                      0.1275 |

## Performance by Cryptocurrency

### BTC-USD

|                     |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:--------------------|---------------:|---------------:|-----------:|----------------:|
| ('Bollinger', 'D')  |        -1.0373 |   -0.0474      |     0.4564 |          0.7703 |
| ('Bollinger', 'M')  |        -0.4308 |   -0.7922      |     0      |          0      |
| ('Bollinger', 'W')  |        -1      |   -0.0883      |     0.4375 |          0.5656 |
| ('BuyAndHold', 'D') |         5.0662 |   12.4382      |     0      |          1.3814 |
| ('BuyAndHold', 'M') |         3.3584 |    4.27551e+06 |     0      |          4.26   |
| ('BuyAndHold', 'W') |         5.0662 |   75.9428      |     0      |          2.3123 |
| ('MACD', 'D')       |        -0.5969 |   -1.9643      |     0.2083 |          0.7986 |
| ('MACD', 'M')       |         0      |    0           |     0      |        inf      |
| ('MACD', 'W')       |        -0.4134 |   -1.0366      |     0.4091 |          0.6779 |

### ETH-USD

|                     |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:--------------------|---------------:|---------------:|-----------:|----------------:|
| ('Bollinger', 'D')  |        -1      |        -0.0495 |     0.4358 |          0.8854 |
| ('Bollinger', 'M')  |        -0.066  |        -2.4108 |     0      |          0      |
| ('Bollinger', 'W')  |        -0.9965 |        -0.1079 |     0.4286 |          1.0184 |
| ('BuyAndHold', 'D') |         2.2893 |         4.8612 |     0      |          1.2269 |
| ('BuyAndHold', 'M') |         1.4899 |      8253.97   |     0      |          2.6443 |
| ('BuyAndHold', 'W') |         2.2893 |        14.41   |     0      |          1.6532 |
| ('MACD', 'D')       |        -0.5643 |        -1.6853 |     0.1948 |          0.8276 |
| ('MACD', 'M')       |        -0.473  |        -0.6382 |     0      |          0      |
| ('MACD', 'W')       |        -0.3445 |        -0.6791 |     0.45   |          0.8664 |

### XRP-USD

|                     |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:--------------------|---------------:|---------------:|-----------:|----------------:|
| ('Bollinger', 'D')  |        -1.0019 |   -0.1122      |     0.5075 |          1.8519 |
| ('Bollinger', 'M')  |        -0.257  |   -1.1303      |     0      |          0      |
| ('Bollinger', 'W')  |        -0.9987 |   -0.1885      |     0.5667 |          0.7743 |
| ('BuyAndHold', 'D') |         6.2136 |    8.3851      |     0      |          1.3511 |
| ('BuyAndHold', 'M') |         5.0132 |    3.54222e+07 |     0      |          3.8689 |
| ('BuyAndHold', 'W') |         6.2136 |   59.3797      |     0      |          2.0994 |
| ('MACD', 'D')       |        -0.7503 |   -1.3883      |     0.0769 |          0.8427 |
| ('MACD', 'M')       |         0.2087 |    2.8527      |     0.3333 |          1.5048 |
| ('MACD', 'W')       |        -0.9653 |   -0.5874      |     0.2353 |          0.24   |

### SOL-USD

|                     |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:--------------------|---------------:|---------------:|-----------:|----------------:|
| ('Bollinger', 'D')  |    1.24605e+42 |    4.3855e+40  |     0.4548 |          0.8446 |
| ('Bollinger', 'M')  |    0.027       |    3.792       |     0.5    |        inf      |
| ('Bollinger', 'W')  |    1.51744e+06 |    6.97662e+13 |     0.3947 |          0.6059 |
| ('BuyAndHold', 'D') |   22.1749      |   29.1859      |     0      |          1.3754 |
| ('BuyAndHold', 'M') |    8.6581      |    1.26218e+10 |     0      |          3.6268 |
| ('BuyAndHold', 'W') |   22.1749      |  969.018       |     0      |          2.2008 |
| ('MACD', 'D')       |   -0.656       |   -1.3967      |     0.3039 |          0.8752 |
| ('MACD', 'M')       |    5.0057      |    8.15598e+07 |     0      |          4.2445 |
| ('MACD', 'W')       |   -0.8181      |   -0.6992      |     0.3478 |          0.5758 |

### BNB-USD

|                     |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:--------------------|---------------:|---------------:|-----------:|----------------:|
| ('Bollinger', 'D')  |        -1      |        -0.0702 |     0.4722 |          0.8752 |
| ('Bollinger', 'M')  |        -0.3156 |        -1.2791 |     0      |          0      |
| ('Bollinger', 'W')  |        -1      |        -0.0978 |     0.4583 |          0.7521 |
| ('BuyAndHold', 'D') |         1.9421 |         4.4859 |     0      |          1.223  |
| ('BuyAndHold', 'M') |         1.2995 |      3544.85   |     0      |          2.7081 |
| ('BuyAndHold', 'W') |         1.9421 |        11.8471 |     0      |          1.6827 |
| ('MACD', 'D')       |        -0.4968 |        -1.7379 |     0.2553 |          0.8359 |
| ('MACD', 'M')       |         0.7025 |       149.191  |     0      |          2.5888 |
| ('MACD', 'W')       |         0.0752 |         0.269  |     0.2857 |          1.1714 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    1.24605e+42 |
| Bollinger  | SOL-USD  | W           |    1.51744e+06 |
| BuyAndHold | SOL-USD  | D           |   22.1749      |
| BuyAndHold | SOL-USD  | W           |   22.1749      |
| BuyAndHold | SOL-USD  | M           |    8.65808     |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |   sharpe_ratio |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    4.3855e+40  |
| Bollinger  | SOL-USD  | W           |    6.97662e+13 |
| BuyAndHold | SOL-USD  | M           |    1.26218e+10 |
| MACD       | SOL-USD  | M           |    8.15598e+07 |
| BuyAndHold | XRP-USD  | M           |    3.54222e+07 |

### By win_rate
| strategy   | symbol   | timeframe   |   win_rate |
|:-----------|:---------|:------------|-----------:|
| Bollinger  | XRP-USD  | W           |   0.566667 |
| Bollinger  | XRP-USD  | D           |   0.507508 |
| Bollinger  | SOL-USD  | M           |   0.5      |
| Bollinger  | BNB-USD  | D           |   0.472222 |
| Bollinger  | BNB-USD  | W           |   0.458333 |

### By profit_factor
| strategy   | symbol   | timeframe   |   profit_factor |
|:-----------|:---------|:------------|----------------:|
| MACD       | BTC-USD  | M           |       inf       |
| Bollinger  | SOL-USD  | M           |       inf       |
| BuyAndHold | BTC-USD  | M           |         4.26    |
| MACD       | SOL-USD  | M           |         4.2445  |
| BuyAndHold | XRP-USD  | M           |         3.86885 |

## Strategy Analysis

### Risk-Adjusted Returns
| strategy   |   sharpe_ratio |   max_drawdown |   recovery_factor |
|:-----------|---------------:|---------------:|------------------:|
| Bollinger  |    2.92367e+39 |       -24.4556 |          inf      |
| BuyAndHold |    8.441e+08   |        -0.3674 |           17.2341 |
| MACD       |    5.43733e+06 |        -0.507  |          inf      |

### Trading Efficiency
| strategy   |   ('win_rate', 'mean') |   ('profit_factor', 'mean') |   ('num_trades', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |
|:-----------|-----------------------:|----------------------------:|-------------------------:|------------------------:|-----------------------------:|
| Bollinger  |                 0.3408 |                     inf     |                 127.933  |                    1919 |                       0.009  |
| BuyAndHold |                 0      |                       2.241 |                   1      |                      15 |                       0.002  |
| MACD       |                 0.2067 |                     inf     |                  35.0667 |                     526 |                       0.0085 |

### Performance by Timeframe
|                     |    total_return |   sharpe_ratio |   win_rate |
|:--------------------|----------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |      2.4921e+41 |    8.771e+39   |     0.4653 |
| ('Bollinger', 'M')  |     -0.2085     |   -0.3641      |     0.1    |
| ('Bollinger', 'W')  | 303488          |    1.39532e+13 |     0.4572 |
| ('BuyAndHold', 'D') |      7.5372     |   11.8713      |     0      |
| ('BuyAndHold', 'M') |      3.9638     |    2.5323e+09  |     0      |
| ('BuyAndHold', 'W') |      7.5372     |  226.119       |     0      |
| ('MACD', 'D')       |     -0.6129     |   -1.6345      |     0.2079 |
| ('MACD', 'M')       |      1.0888     |    1.6312e+07  |     0.0667 |
| ('MACD', 'W')       |     -0.4932     |   -0.5466      |     0.3456 |

