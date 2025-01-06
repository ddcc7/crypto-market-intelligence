# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 21:21:04

## Overall Strategy Performance

| strategy          |   ('total_return', 'mean') |   ('total_return', 'std') |   ('sharpe_ratio', 'mean') |   ('sharpe_ratio', 'std') |   ('win_rate', 'mean') |   ('win_rate', 'std') |   ('profit_factor', 'mean') |   ('profit_factor', 'std') |   ('recovery_factor', 'mean') |   ('recovery_factor', 'std') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:------------------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|-----------------------:|----------------------:|----------------------------:|---------------------------:|------------------------------:|-----------------------------:|------------------------:|-----------------------------:|----------------------------:|
| AdaptiveBollinger |                     0.0026 |                    0.0217 |                0.0542      |               1.1123      |                 0.0939 |                0.1462 |                    667.104  |                   487.311  |                      667.097  |                     487.323  |                     343 |                       2.2336 |                     33.5041 |
| AdaptiveMACD      |                     0.0532 |                    0.1338 |                0.4694      |               1.2217      |                 0.1523 |                0.2233 |                    667.074  |                   487.353  |                      667.352  |                     486.949  |                    1920 |                       2.2274 |                     33.4111 |
| Bollinger         |                    -0.351  |                    0.3014 |               -0.624       |               1.4574      |                 0.2643 |                0.2001 |                     67.2545 |                   258.037  |                       66.0149 |                     258.379  |                     439 |                       0.527  |                      7.9051 |
| BuyAndHold        |                     6.0297 |                    6.7536 |                7.17421e+08 |               2.77752e+09 |                 0      |                0      |                      2.1296 |                     0.8888 |                       16.3056 |                      15.7396 |                      15 |                       0.0029 |                      0.0429 |
| MACD              |                    -0.0135 |                    1.4312 |                4.63354e+06 |               1.79456e+07 |                 0.2087 |                0.1557 |                     67.7274 |                   257.907  |                       67.1245 |                     258.098  |                     526 |                       0.0133 |                      0.2001 |
| Optimized         |                    -0.2618 |                    0.3077 |               -1.0636      |               0.9182      |                 0.2839 |                0.193  |                      0.57   |                     0.463  |                       -0.6289 |                       0.5355 |                    2730 |                       0.4842 |                      7.2625 |

## Performance by Cryptocurrency

### BTC-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0265 |   -1.535       |     0.3288 |          0.5987 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.1698 |    2.2182      |     0.4841 |          1.2651 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.2432 |   -0.7101      |     0.4051 |          0.9749 |
| ('Bollinger', 'M')         |        -0.394  |   -0.8054      |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5108 |   -1.0097      |     0.3636 |          0.683  |
| ('BuyAndHold', 'D')        |         4.9899 |   12.2469      |     0      |          1.3782 |
| ('BuyAndHold', 'M')        |         3.3036 |    3.71831e+06 |     0      |          4.2353 |
| ('BuyAndHold', 'W')        |         4.9899 |   73.5221      |     0      |          2.2939 |
| ('MACD', 'D')              |        -0.5919 |   -1.9467      |     0.2083 |          0.8019 |
| ('MACD', 'M')              |         0      |    0           |     0      |       1000      |
| ('MACD', 'W')              |        -0.4134 |   -1.0366      |     0.4091 |          0.6779 |
| ('Optimized', 'D')         |        -0.6219 |   -1.9765      |     0.4783 |          0.8387 |
| ('Optimized', 'M')         |        -0.1107 |   -2.4383      |     0      |          0      |
| ('Optimized', 'W')         |        -0.5367 |   -1.2936      |     0.4096 |          0.5633 |

### ETH-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |         0.0183 |         1.802  |     0.3269 |          1.8141 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.0972 |         1.3453 |     0.453  |          1.1622 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.0367 |        -0.0929 |     0.4231 |          1.0347 |
| ('Bollinger', 'M')         |        -0.0454 |        -2.6551 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.1064 |        -0.2443 |     0.4444 |          1.0426 |
| ('BuyAndHold', 'D')        |         2.2256 |         4.7287 |     0      |          1.2239 |
| ('BuyAndHold', 'M')        |         1.4417 |      6662.43   |     0      |          2.616  |
| ('BuyAndHold', 'W')        |         2.2256 |        13.6763 |     0      |          1.6396 |
| ('MACD', 'D')              |        -0.5554 |        -1.6606 |     0.1948 |          0.8319 |
| ('MACD', 'M')              |        -0.473  |        -0.6382 |     0      |          0      |
| ('MACD', 'W')              |        -0.3445 |        -0.6791 |     0.45   |          0.8664 |
| ('Optimized', 'D')         |         0.1538 |         0.4245 |     0.5015 |          1.0626 |
| ('Optimized', 'M')         |        -0.3617 |        -0.7881 |     0.25   |          0.0709 |
| ('Optimized', 'W')         |         0.1963 |         0.6788 |     0.439  |          1.218  |

### XRP-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |         0.0725 |         2.9592 |     0.3387 |          3.0575 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.495  |         3.821  |     0.4742 |          1.7821 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.662  |        -0.9526 |     0.4366 |          0.9342 |
| ('Bollinger', 'M')         |        -0.2163 |        -1.3001 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.3556 |        -0.4714 |     0.2667 |          1.0727 |
| ('BuyAndHold', 'D')        |         5.9802 |         8.0698 |     0      |          1.3461 |
| ('BuyAndHold', 'M')        |         2.0482 |     45508.7    |     0      |          2.412  |
| ('BuyAndHold', 'W')        |         5.9802 |        54.6207 |     0      |          2.0743 |
| ('MACD', 'D')              |        -0.7419 |        -1.3729 |     0.0962 |          0.8499 |
| ('MACD', 'M')              |         0.1696 |         1.8984 |     0.3333 |          1.4577 |
| ('MACD', 'W')              |        -0.9653 |        -0.5874 |     0.2353 |          0.24   |
| ('Optimized', 'D')         |         0.0152 |         0.229  |     0.3333 |          1.197  |
| ('Optimized', 'M')         |        -0.173  |        -1.5282 |     0      |          0      |
| ('Optimized', 'W')         |        -0.0993 |        -1.4588 |     0      |          0      |

### SOL-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0056 |   -0.9914      |     0.1176 |          0.4189 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |        -0.0498 |   -1.3575      |     0.4196 |          0.771  |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.8854 |   -1.4455      |     0.4648 |          0.8258 |
| ('Bollinger', 'M')         |         0.0409 |    4.0743      |     0      |       1000      |
| ('Bollinger', 'W')         |        -0.9038 |   -0.5595      |     0.3333 |          0.5975 |
| ('BuyAndHold', 'D')        |        21.8417 |   28.7486      |     0      |          1.374  |
| ('BuyAndHold', 'M')        |         8.5192 |    1.07575e+10 |     0      |          3.5864 |
| ('BuyAndHold', 'W')        |        21.8417 |  934.557       |     0      |          2.1921 |
| ('MACD', 'D')              |        -0.6509 |   -1.3861      |     0.3039 |          0.8773 |
| ('MACD', 'M')              |         4.9193 |    6.95029e+07 |     0      |          4.1691 |
| ('MACD', 'W')              |        -0.8181 |   -0.6992      |     0.3478 |          0.5758 |
| ('Optimized', 'D')         |        -0.6758 |   -1.4437      |     0.4495 |          0.8814 |
| ('Optimized', 'M')         |        -0.0528 |   -1.4968      |     0.25   |          0.3952 |
| ('Optimized', 'W')         |        -0.8363 |   -0.6951      |     0.3425 |          0.5602 |

### BNB-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.019  |        -1.4218 |     0.2969 |          0.6668 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.0853 |         1.0142 |     0.4531 |          1.1359 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.1371 |        -0.3571 |     0.4625 |          1.0139 |
| ('Bollinger', 'M')         |        -0.2181 |        -1.8205 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5915 |        -1.0107 |     0.3636 |          0.6381 |
| ('BuyAndHold', 'D')        |         1.8968 |         4.3812 |     0      |          1.2202 |
| ('BuyAndHold', 'M')        |         1.2641 |      2994.39   |     0      |          2.6818 |
| ('BuyAndHold', 'W')        |         1.8968 |        11.3506 |     0      |          1.67   |
| ('MACD', 'D')              |        -0.4889 |        -1.7104 |     0.266  |          0.84   |
| ('MACD', 'M')              |         0.6763 |       126.079  |     0      |          2.552  |
| ('MACD', 'W')              |         0.0752 |         0.269  |     0.2857 |          1.1714 |
| ('Optimized', 'D')         |        -0.4297 |        -1.301  |     0.4749 |          0.9205 |
| ('Optimized', 'M')         |        -0.1198 |        -2.0889 |     0      |          0      |
| ('Optimized', 'W')         |        -0.2743 |        -0.7774 |     0.3293 |          0.8425 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| BuyAndHold | SOL-USD  | W           |       21.8417  |
| BuyAndHold | SOL-USD  | D           |       21.8417  |
| BuyAndHold | SOL-USD  | M           |        8.51924 |
| BuyAndHold | XRP-USD  | D           |        5.98018 |
| BuyAndHold | XRP-USD  | W           |        5.98018 |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |    sharpe_ratio |
|:-----------|:---------|:------------|----------------:|
| BuyAndHold | SOL-USD  | M           |     1.07575e+10 |
| MACD       | SOL-USD  | M           |     6.95029e+07 |
| BuyAndHold | BTC-USD  | M           |     3.71831e+06 |
| BuyAndHold | XRP-USD  | M           | 45508.7         |
| BuyAndHold | ETH-USD  | M           |  6662.43        |

### By win_rate
| strategy     | symbol   | timeframe   |   win_rate |
|:-------------|:---------|:------------|-----------:|
| Optimized    | ETH-USD  | D           |   0.501471 |
| AdaptiveMACD | BTC-USD  | D           |   0.484127 |
| Optimized    | BTC-USD  | D           |   0.478324 |
| Optimized    | BNB-USD  | D           |   0.474916 |
| AdaptiveMACD | XRP-USD  | D           |   0.474227 |

### By profit_factor
| strategy          | symbol   | timeframe   |   profit_factor |
|:------------------|:---------|:------------|----------------:|
| AdaptiveMACD      | BTC-USD  | W           |            1000 |
| AdaptiveBollinger | BTC-USD  | W           |            1000 |
| AdaptiveMACD      | BTC-USD  | M           |            1000 |
| MACD              | BTC-USD  | M           |            1000 |
| AdaptiveBollinger | BTC-USD  | M           |            1000 |

## Strategy Analysis

### Risk-Adjusted Returns
| strategy          |   sharpe_ratio |   max_drawdown |   recovery_factor |
|:------------------|---------------:|---------------:|------------------:|
| AdaptiveBollinger |    0.0542      |        -0.007  |          667.097  |
| AdaptiveMACD      |    0.4694      |        -0.0254 |          667.352  |
| Bollinger         |   -0.624       |        -0.5247 |           66.0149 |
| BuyAndHold        |    7.17421e+08 |        -0.3674 |           16.3056 |
| MACD              |    4.63354e+06 |        -0.5059 |           67.1245 |
| Optimized         |   -1.0636      |        -0.3953 |           -0.6289 |

### Trading Efficiency
| strategy          |   ('win_rate', 'mean') |   ('profit_factor', 'mean') |   ('num_trades', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |
|:------------------|-----------------------:|----------------------------:|-------------------------:|------------------------:|-----------------------------:|
| AdaptiveBollinger |                 0.0939 |                    667.104  |                  22.8667 |                     343 |                       2.2336 |
| AdaptiveMACD      |                 0.1523 |                    667.074  |                 128      |                    1920 |                       2.2274 |
| Bollinger         |                 0.2643 |                     67.2545 |                  29.2667 |                     439 |                       0.527  |
| BuyAndHold        |                 0      |                      2.1296 |                   1      |                      15 |                       0.0029 |
| MACD              |                 0.2087 |                     67.7274 |                  35.0667 |                     526 |                       0.0133 |
| Optimized         |                 0.2839 |                      0.57   |                 182      |                    2730 |                       0.4842 |

### Performance by Timeframe
|                            |   total_return |   sharpe_ratio |   win_rate |
|:---------------------------|---------------:|---------------:|-----------:|
| ('AdaptiveBollinger', 'D') |         0.0079 |    0.1626      |     0.2818 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |
| ('AdaptiveMACD', 'D')      |         0.1595 |    1.4083      |     0.4568 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |
| ('Bollinger', 'D')         |        -0.3929 |   -0.7116      |     0.4384 |
| ('Bollinger', 'M')         |        -0.1666 |   -0.5013      |     0      |
| ('Bollinger', 'W')         |        -0.4936 |   -0.6591      |     0.3543 |
| ('BuyAndHold', 'D')        |         7.3869 |   11.635       |     0      |
| ('BuyAndHold', 'M')        |         3.3154 |    2.15226e+09 |     0      |
| ('BuyAndHold', 'W')        |         7.3869 |  217.545       |     0      |
| ('MACD', 'D')              |        -0.6058 |   -1.6153      |     0.2138 |
| ('MACD', 'M')              |         1.0584 |    1.39006e+07 |     0.0667 |
| ('MACD', 'W')              |        -0.4932 |   -0.5466      |     0.3456 |
| ('Optimized', 'D')         |        -0.3117 |   -0.8135      |     0.4475 |
| ('Optimized', 'M')         |        -0.1636 |   -1.6681      |     0.1    |
| ('Optimized', 'W')         |        -0.3101 |   -0.7092      |     0.3041 |

