# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 21:29:09

## Overall Strategy Performance

| strategy          |   ('total_return', 'mean') |   ('total_return', 'std') |   ('sharpe_ratio', 'mean') |   ('sharpe_ratio', 'std') |   ('win_rate', 'mean') |   ('win_rate', 'std') |   ('profit_factor', 'mean') |   ('profit_factor', 'std') |   ('recovery_factor', 'mean') |   ('recovery_factor', 'std') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:------------------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|-----------------------:|----------------------:|----------------------------:|---------------------------:|------------------------------:|-----------------------------:|------------------------:|-----------------------------:|----------------------------:|
| AdaptiveBollinger |                     0.0026 |                    0.0217 |                0.0542      |               1.1123      |                 0.0939 |                0.1462 |                    667.104  |                   487.311  |                      667.097  |                     487.323  |                     343 |                       2.1244 |                     31.8661 |
| AdaptiveMACD      |                     0.0532 |                    0.1338 |                0.4694      |               1.2217      |                 0.1523 |                0.2233 |                    667.074  |                   487.353  |                      667.352  |                     486.948  |                    1920 |                       2.1458 |                     32.1871 |
| Bollinger         |                    -0.3502 |                    0.3017 |               -0.625       |               1.4642      |                 0.2643 |                0.2001 |                     67.2548 |                   258.036  |                       66.0153 |                     258.379  |                     439 |                       0.516  |                      7.7406 |
| BuyAndHold        |                     6.0208 |                    6.7477 |                7.0983e+08  |               2.74812e+09 |                 0      |                0      |                      2.1284 |                     0.8884 |                       16.2841 |                      15.7291 |                      15 |                       0.0029 |                      0.0439 |
| MACD              |                    -0.0143 |                    1.4295 |                4.58444e+06 |               1.77554e+07 |                 0.2087 |                0.1557 |                     67.7265 |                   257.908  |                       67.1219 |                     258.098  |                     526 |                       0.0088 |                      0.1324 |
| Optimized         |                    -0.2614 |                    0.3078 |               -1.063       |               0.9183      |                 0.2839 |                0.193  |                      0.5707 |                     0.4628 |                       -0.6281 |                       0.5357 |                    2730 |                       0.4797 |                      7.1952 |

## Performance by Cryptocurrency

### BTC-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0265 |    -1.535      |     0.3288 |          0.5987 |
| ('AdaptiveBollinger', 'M') |         0      |     0          |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |     0          |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.1698 |     2.2183     |     0.4841 |          1.2651 |
| ('AdaptiveMACD', 'M')      |         0      |     0          |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |     0          |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.2432 |    -0.7099     |     0.4051 |          0.9749 |
| ('Bollinger', 'M')         |        -0.3939 |    -0.8054     |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5108 |    -1.0097     |     0.3636 |          0.683  |
| ('BuyAndHold', 'D')        |         4.9896 |    12.2461     |     0      |          1.3782 |
| ('BuyAndHold', 'M')        |         3.3034 |     3.7161e+06 |     0      |          4.2352 |
| ('BuyAndHold', 'W')        |         4.9896 |    73.5119     |     0      |          2.2939 |
| ('MACD', 'D')              |        -0.5919 |    -1.9466     |     0.2083 |          0.8019 |
| ('MACD', 'M')              |         0      |     0          |     0      |       1000      |
| ('MACD', 'W')              |        -0.4134 |    -1.0366     |     0.4091 |          0.6779 |
| ('Optimized', 'D')         |        -0.6219 |    -1.9764     |     0.4783 |          0.8387 |
| ('Optimized', 'M')         |        -0.1107 |    -2.4382     |     0      |          0      |
| ('Optimized', 'W')         |        -0.5367 |    -1.2936     |     0.4096 |          0.5634 |

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
| ('Bollinger', 'M')         |        -0.0445 |        -2.6666 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.1057 |        -0.2427 |     0.4444 |          1.0431 |
| ('BuyAndHold', 'D')        |         2.2228 |         4.7228 |     0      |          1.2238 |
| ('BuyAndHold', 'M')        |         1.4396 |      6599.08   |     0      |          2.6148 |
| ('BuyAndHold', 'W')        |         2.2228 |        13.6443 |     0      |          1.639  |
| ('MACD', 'D')              |        -0.555  |        -1.6594 |     0.1948 |          0.8321 |
| ('MACD', 'M')              |        -0.473  |        -0.6382 |     0      |          0      |
| ('MACD', 'W')              |        -0.3445 |        -0.6791 |     0.45   |          0.8664 |
| ('Optimized', 'D')         |         0.1547 |         0.4268 |     0.5015 |          1.0628 |
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
| ('Bollinger', 'D')         |        -0.6611 |        -0.9511 |     0.4366 |          0.9346 |
| ('Bollinger', 'M')         |        -0.2127 |        -1.3167 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.3541 |        -0.4698 |     0.2667 |          1.0743 |
| ('BuyAndHold', 'D')        |         5.9598 |         8.042  |     0      |          1.3456 |
| ('BuyAndHold', 'M')        |         2.0393 |     44088.4    |     0      |          2.4092 |
| ('BuyAndHold', 'W')        |         5.9598 |        54.216  |     0      |          2.0722 |
| ('MACD', 'D')              |        -0.7412 |        -1.3714 |     0.0962 |          0.8506 |
| ('MACD', 'M')              |         0.1661 |         1.8281 |     0.3333 |          1.4535 |
| ('MACD', 'W')              |        -0.9653 |        -0.5874 |     0.2353 |          0.24   |
| ('Optimized', 'D')         |         0.0152 |         0.229  |     0.3333 |          1.197  |
| ('Optimized', 'M')         |        -0.1702 |        -1.5452 |     0      |          0      |
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
| ('Bollinger', 'D')         |        -0.8855 |   -1.4457      |     0.4648 |          0.8257 |
| ('Bollinger', 'M')         |         0.0419 |    4.0938      |     0      |       1000      |
| ('Bollinger', 'W')         |        -0.9037 |   -0.5595      |     0.3333 |          0.5978 |
| ('BuyAndHold', 'D')        |        21.8197 |   28.7195      |     0      |          1.3739 |
| ('BuyAndHold', 'M')        |         8.5101 |    1.06437e+10 |     0      |          3.5837 |
| ('BuyAndHold', 'W')        |        21.8197 |  932.305       |     0      |          2.1915 |
| ('MACD', 'D')              |        -0.6506 |   -1.3854      |     0.3039 |          0.8774 |
| ('MACD', 'M')              |         4.9136 |    6.87665e+07 |     0      |          4.1642 |
| ('MACD', 'W')              |        -0.8181 |   -0.6992      |     0.3478 |          0.5758 |
| ('Optimized', 'D')         |        -0.6758 |   -1.4437      |     0.4495 |          0.8814 |
| ('Optimized', 'M')         |        -0.0522 |   -1.4774      |     0.25   |          0.4041 |
| ('Optimized', 'W')         |        -0.8362 |   -0.6951      |     0.3425 |          0.5604 |

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
| ('Bollinger', 'M')         |        -0.2156 |        -1.8321 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5905 |        -1.0095 |     0.3636 |          0.6394 |
| ('BuyAndHold', 'D')        |         1.889  |         4.3629 |     0      |          1.2197 |
| ('BuyAndHold', 'M')        |         1.258  |      2907.25   |     0      |          2.6773 |
| ('BuyAndHold', 'W')        |         1.889  |        11.2654 |     0      |          1.6678 |
| ('MACD', 'D')              |        -0.4876 |        -1.7054 |     0.266  |          0.8407 |
| ('MACD', 'M')              |         0.6718 |       122.415  |     0      |          2.5456 |
| ('MACD', 'W')              |         0.0752 |         0.269  |     0.2857 |          1.1714 |
| ('Optimized', 'D')         |        -0.4284 |        -1.2973 |     0.4749 |          0.9209 |
| ('Optimized', 'M')         |        -0.1198 |        -2.0889 |     0      |          0      |
| ('Optimized', 'W')         |        -0.2743 |        -0.7774 |     0.3293 |          0.8425 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| BuyAndHold | SOL-USD  | D           |       21.8197  |
| BuyAndHold | SOL-USD  | W           |       21.8197  |
| BuyAndHold | SOL-USD  | M           |        8.51007 |
| BuyAndHold | XRP-USD  | D           |        5.95982 |
| BuyAndHold | XRP-USD  | W           |        5.95982 |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |    sharpe_ratio |
|:-----------|:---------|:------------|----------------:|
| BuyAndHold | SOL-USD  | M           |     1.06437e+10 |
| MACD       | SOL-USD  | M           |     6.87665e+07 |
| BuyAndHold | BTC-USD  | M           |     3.7161e+06  |
| BuyAndHold | XRP-USD  | M           | 44088.4         |
| BuyAndHold | ETH-USD  | M           |  6599.08        |

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
| AdaptiveBollinger | BTC-USD  | W           |            1000 |
| AdaptiveMACD      | BTC-USD  | W           |            1000 |
| MACD              | BTC-USD  | M           |            1000 |
| AdaptiveMACD      | BTC-USD  | M           |            1000 |
| AdaptiveBollinger | BTC-USD  | M           |            1000 |

## Strategy Analysis

### Risk-Adjusted Returns
| strategy          |   sharpe_ratio |   max_drawdown |   recovery_factor |
|:------------------|---------------:|---------------:|------------------:|
| AdaptiveBollinger |    0.0542      |        -0.007  |          667.097  |
| AdaptiveMACD      |    0.4694      |        -0.0254 |          667.352  |
| Bollinger         |   -0.625       |        -0.5242 |           66.0153 |
| BuyAndHold        |    7.0983e+08  |        -0.3674 |           16.2841 |
| MACD              |    4.58444e+06 |        -0.5059 |           67.1219 |
| Optimized         |   -1.063       |        -0.3951 |           -0.6281 |

### Trading Efficiency
| strategy          |   ('win_rate', 'mean') |   ('profit_factor', 'mean') |   ('num_trades', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |
|:------------------|-----------------------:|----------------------------:|-------------------------:|------------------------:|-----------------------------:|
| AdaptiveBollinger |                 0.0939 |                    667.104  |                  22.8667 |                     343 |                       2.1244 |
| AdaptiveMACD      |                 0.1523 |                    667.074  |                 128      |                    1920 |                       2.1458 |
| Bollinger         |                 0.2643 |                     67.2548 |                  29.2667 |                     439 |                       0.516  |
| BuyAndHold        |                 0      |                      2.1284 |                   1      |                      15 |                       0.0029 |
| MACD              |                 0.2087 |                     67.7265 |                  35.0667 |                     526 |                       0.0088 |
| Optimized         |                 0.2839 |                      0.5707 |                 182      |                    2730 |                       0.4797 |

### Performance by Timeframe
|                            |   total_return |   sharpe_ratio |   win_rate |
|:---------------------------|---------------:|---------------:|-----------:|
| ('AdaptiveBollinger', 'D') |         0.0079 |    0.1626      |     0.2818 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |
| ('AdaptiveMACD', 'D')      |         0.1595 |    1.4083      |     0.4568 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |
| ('Bollinger', 'D')         |        -0.3927 |   -0.7114      |     0.4384 |
| ('Bollinger', 'M')         |        -0.165  |   -0.5054      |     0      |
| ('Bollinger', 'W')         |        -0.4929 |   -0.6582      |     0.3543 |
| ('BuyAndHold', 'D')        |         7.3762 |   11.6187      |     0      |
| ('BuyAndHold', 'M')        |         3.3101 |    2.12949e+09 |     0      |
| ('BuyAndHold', 'W')        |         7.3762 |  216.988       |     0      |
| ('MACD', 'D')              |        -0.6052 |   -1.6137      |     0.2138 |
| ('MACD', 'M')              |         1.0557 |    1.37533e+07 |     0.0667 |
| ('MACD', 'W')              |        -0.4932 |   -0.5466      |     0.3456 |
| ('Optimized', 'D')         |        -0.3112 |   -0.8123      |     0.4475 |
| ('Optimized', 'M')         |        -0.1629 |   -1.6675      |     0.1    |
| ('Optimized', 'W')         |        -0.31   |   -0.7092      |     0.3041 |

