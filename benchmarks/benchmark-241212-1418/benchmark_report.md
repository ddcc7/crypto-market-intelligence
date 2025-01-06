# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 14:20:01

## Overall Strategy Performance

| strategy          |   ('total_return', 'mean') |   ('total_return', 'std') |   ('sharpe_ratio', 'mean') |   ('sharpe_ratio', 'std') |   ('win_rate', 'mean') |   ('win_rate', 'std') |   ('profit_factor', 'mean') |   ('profit_factor', 'std') |   ('recovery_factor', 'mean') |   ('recovery_factor', 'std') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:------------------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|-----------------------:|----------------------:|----------------------------:|---------------------------:|------------------------------:|-----------------------------:|------------------------:|-----------------------------:|----------------------------:|
| AdaptiveBollinger |                     0.0026 |                    0.0217 |                0.0542      |               1.1123      |                 0.0939 |                0.1462 |                    667.104  |                   487.311  |                      667.097  |                     487.323  |                     343 |                       1.6449 |                     24.6732 |
| AdaptiveMACD      |                     0.0531 |                    0.1338 |                0.469       |               1.2211      |                 0.1523 |                0.2233 |                    667.074  |                   487.353  |                      667.352  |                     486.949  |                    1920 |                       1.6023 |                     24.0341 |
| Bollinger         |                    -0.362  |                    0.297  |               -0.6187      |               1.3524      |                 0.2639 |                0.1998 |                     67.2511 |                   258.038  |                       66.0078 |                     258.381  |                     440 |                       0.44   |                      6.5994 |
| BuyAndHold        |                     6.1584 |                    6.8567 |                8.52214e+08 |               3.29939e+09 |                 0      |                0      |                      2.1462 |                     0.8996 |                       16.647  |                      15.9671 |                      15 |                       0.002  |                      0.0293 |
| MACD              |                    -0.0057 |                    1.4563 |                5.50503e+06 |               2.13208e+07 |                 0.2067 |                0.1565 |                     67.7365 |                   257.905  |                       67.1529 |                     258.091  |                     526 |                       0.0092 |                      0.1386 |

## Performance by Cryptocurrency

### BTC-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0265 |   -1.535       |     0.3288 |          0.5987 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.1693 |    2.2122      |     0.4841 |          1.2644 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.2535 |   -0.7403      |     0.4051 |          0.9718 |
| ('Bollinger', 'M')         |        -0.403  |   -0.804       |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5175 |   -1.0174      |     0.3636 |          0.6754 |
| ('BuyAndHold', 'D')        |         5.0738 |   12.4572      |     0      |          1.3818 |
| ('BuyAndHold', 'M')        |         3.3639 |    4.33521e+06 |     0      |          4.2625 |
| ('BuyAndHold', 'W')        |         5.0738 |   76.1865      |     0      |          2.3141 |
| ('MACD', 'D')              |        -0.5974 |   -1.966       |     0.2083 |          0.7983 |
| ('MACD', 'M')              |         0      |    0           |     0      |       1000      |
| ('MACD', 'W')              |        -0.4134 |   -1.0366      |     0.4091 |          0.6779 |

### ETH-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |         0.0183 |         1.802  |     0.3269 |          1.8141 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.0972 |         1.3453 |     0.453  |          1.1622 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.0367 |        -0.0929 |     0.4177 |          1.0347 |
| ('Bollinger', 'M')         |        -0.0681 |        -2.3876 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.1246 |        -0.2824 |     0.4444 |          1.0317 |
| ('BuyAndHold', 'D')        |         2.2958 |         4.8745 |     0      |          1.2273 |
| ('BuyAndHold', 'M')        |         1.4949 |      8434.05   |     0      |          2.6472 |
| ('BuyAndHold', 'W')        |         2.2958 |        14.4856 |     0      |          1.6546 |
| ('MACD', 'D')              |        -0.5652 |        -1.6877 |     0.1948 |          0.8272 |
| ('MACD', 'M')              |        -0.473  |        -0.6382 |     0      |          0      |
| ('MACD', 'W')              |        -0.3445 |        -0.6791 |     0.45   |          0.8664 |

### XRP-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |         0.0725 |         2.9592 |     0.3387 |          3.0575 |
| ('AdaptiveBollinger', 'M') |         0      |         0      |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.495  |         3.821  |     0.4742 |          1.7821 |
| ('AdaptiveMACD', 'M')      |         0      |         0      |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |         0      |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.6723 |        -0.9673 |     0.4366 |          0.93   |
| ('Bollinger', 'M')         |        -0.2542 |        -1.1408 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.3723 |        -0.4878 |     0.2667 |          1.0563 |
| ('BuyAndHold', 'D')        |         6.1975 |         8.3636 |     0      |          1.3508 |
| ('BuyAndHold', 'M')        |         2.1431 |     63460.6    |     0      |          2.4417 |
| ('BuyAndHold', 'W')        |         6.1975 |        59.0458 |     0      |          2.0976 |
| ('MACD', 'D')              |        -0.7497 |        -1.3873 |     0.0769 |          0.8431 |
| ('MACD', 'M')              |         0.206  |         2.7777 |     0.3333 |          1.5016 |
| ('MACD', 'W')              |        -0.9653 |        -0.5874 |     0.2353 |          0.24   |

### SOL-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0056 |   -0.9914      |     0.1176 |          0.4189 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |        -0.0498 |   -1.3575      |     0.4196 |          0.771  |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.8836 |   -1.4423      |     0.4648 |          0.8275 |
| ('Bollinger', 'M')         |         0.0259 |    3.7709      |     0      |       1000      |
| ('Bollinger', 'W')         |        -0.9052 |   -0.5599      |     0.3333 |          0.5934 |
| ('BuyAndHold', 'D')        |        22.2009 |   29.2199      |     0      |          1.3755 |
| ('BuyAndHold', 'M')        |         8.6689 |    1.27788e+10 |     0      |          3.63   |
| ('BuyAndHold', 'W')        |        22.2009 |  971.734       |     0      |          2.2015 |
| ('MACD', 'D')              |        -0.6564 |   -1.3976      |     0.3039 |          0.875  |
| ('MACD', 'M')              |         5.0124 |    8.25753e+07 |     0      |          4.2505 |
| ('MACD', 'W')              |        -0.8181 |   -0.6992      |     0.3478 |          0.5758 |

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
| ('Bollinger', 'M')         |        -0.2307 |        -1.7553 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5966 |        -1.0166 |     0.3636 |          0.6315 |
| ('BuyAndHold', 'D')        |         1.9368 |         4.4736 |     0      |          1.2227 |
| ('BuyAndHold', 'M')        |         1.2953 |      3475.25   |     0      |          2.705  |
| ('BuyAndHold', 'W')        |         1.9368 |        11.7879 |     0      |          1.6812 |
| ('MACD', 'D')              |        -0.4959 |        -1.7347 |     0.2553 |          0.8364 |
| ('MACD', 'M')              |         0.6994 |       146.271  |     0      |          2.5844 |
| ('MACD', 'W')              |         0.0752 |         0.269  |     0.2857 |          1.1714 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| BuyAndHold | SOL-USD  | W           |       22.2009  |
| BuyAndHold | SOL-USD  | D           |       22.2009  |
| BuyAndHold | SOL-USD  | M           |        8.66891 |
| BuyAndHold | XRP-USD  | D           |        6.19753 |
| BuyAndHold | XRP-USD  | W           |        6.19753 |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |    sharpe_ratio |
|:-----------|:---------|:------------|----------------:|
| BuyAndHold | SOL-USD  | M           |     1.27788e+10 |
| MACD       | SOL-USD  | M           |     8.25753e+07 |
| BuyAndHold | BTC-USD  | M           |     4.33521e+06 |
| BuyAndHold | XRP-USD  | M           | 63460.6         |
| BuyAndHold | ETH-USD  | M           |  8434.05        |

### By win_rate
| strategy     | symbol   | timeframe   |   win_rate |
|:-------------|:---------|:------------|-----------:|
| AdaptiveMACD | BTC-USD  | D           |   0.484127 |
| AdaptiveMACD | XRP-USD  | D           |   0.474227 |
| Bollinger    | SOL-USD  | D           |   0.464789 |
| Bollinger    | BNB-USD  | D           |   0.4625   |
| AdaptiveMACD | BNB-USD  | D           |   0.453089 |

### By profit_factor
| strategy          | symbol   | timeframe   |   profit_factor |
|:------------------|:---------|:------------|----------------:|
| AdaptiveMACD      | BTC-USD  | W           |            1000 |
| AdaptiveBollinger | BTC-USD  | W           |            1000 |
| MACD              | BTC-USD  | M           |            1000 |
| AdaptiveMACD      | BTC-USD  | M           |            1000 |
| AdaptiveBollinger | BTC-USD  | M           |            1000 |

## Strategy Analysis

### Risk-Adjusted Returns
| strategy          |   sharpe_ratio |   max_drawdown |   recovery_factor |
|:------------------|---------------:|---------------:|------------------:|
| AdaptiveBollinger |    0.0542      |        -0.007  |          667.097  |
| AdaptiveMACD      |    0.469       |        -0.0254 |          667.352  |
| Bollinger         |   -0.6187      |        -0.5301 |           66.0078 |
| BuyAndHold        |    8.52214e+08 |        -0.3674 |           16.647  |
| MACD              |    5.50503e+06 |        -0.507  |           67.1529 |

### Trading Efficiency
| strategy          |   ('win_rate', 'mean') |   ('profit_factor', 'mean') |   ('num_trades', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |
|:------------------|-----------------------:|----------------------------:|-------------------------:|------------------------:|-----------------------------:|
| AdaptiveBollinger |                 0.0939 |                    667.104  |                  22.8667 |                     343 |                       1.6449 |
| AdaptiveMACD      |                 0.1523 |                    667.074  |                 128      |                    1920 |                       1.6023 |
| Bollinger         |                 0.2639 |                     67.2511 |                  29.3333 |                     440 |                       0.44   |
| BuyAndHold        |                 0      |                      2.1462 |                   1      |                      15 |                       0.002  |
| MACD              |                 0.2067 |                     67.7365 |                  35.0667 |                     526 |                       0.0092 |

### Performance by Timeframe
|                            |   total_return |   sharpe_ratio |   win_rate |
|:---------------------------|---------------:|---------------:|-----------:|
| ('AdaptiveBollinger', 'D') |         0.0079 |    0.1626      |     0.2818 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |
| ('AdaptiveMACD', 'D')      |         0.1594 |    1.407       |     0.4568 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |
| ('Bollinger', 'D')         |        -0.3966 |   -0.72        |     0.4373 |
| ('Bollinger', 'M')         |        -0.186  |   -0.4634      |     0      |
| ('Bollinger', 'W')         |        -0.5032 |   -0.6728      |     0.3543 |
| ('BuyAndHold', 'D')        |         7.541  |   11.8778      |     0      |
| ('BuyAndHold', 'M')        |         3.3932 |    2.55664e+09 |     0      |
| ('BuyAndHold', 'W')        |         7.541  |  226.648       |     0      |
| ('MACD', 'D')              |        -0.6129 |   -1.6347      |     0.2079 |
| ('MACD', 'M')              |         1.089  |    1.65151e+07 |     0.0667 |
| ('MACD', 'W')              |        -0.4932 |   -0.5466      |     0.3456 |

