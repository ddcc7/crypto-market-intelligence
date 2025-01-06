# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 15:44:58

## Overall Strategy Performance

| strategy          |   ('total_return', 'mean') |   ('total_return', 'std') |   ('sharpe_ratio', 'mean') |   ('sharpe_ratio', 'std') |   ('win_rate', 'mean') |   ('win_rate', 'std') |   ('profit_factor', 'mean') |   ('profit_factor', 'std') |   ('recovery_factor', 'mean') |   ('recovery_factor', 'std') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:------------------|---------------------------:|--------------------------:|---------------------------:|--------------------------:|-----------------------:|----------------------:|----------------------------:|---------------------------:|------------------------------:|-----------------------------:|------------------------:|-----------------------------:|----------------------------:|
| AdaptiveBollinger |                     0.0026 |                    0.0217 |                0.0542      |               1.1123      |                 0.0939 |                0.1462 |                    667.104  |                   487.311  |                      667.097  |                     487.323  |                     343 |                       1.6854 |                     25.2808 |
| AdaptiveMACD      |                     0.0531 |                    0.1338 |                0.4689      |               1.221       |                 0.1521 |                0.2231 |                    667.074  |                   487.353  |                      667.352  |                     486.949  |                    1920 |                       1.6641 |                     24.9622 |
| Bollinger         |                    -0.3601 |                    0.2974 |               -0.6204      |               1.3664      |                 0.2639 |                0.1998 |                     67.2516 |                   258.037  |                       66.0085 |                     258.381  |                     440 |                       0.4402 |                      6.6026 |
| BuyAndHold        |                     6.1363 |                    6.8396 |                8.29519e+08 |               3.21147e+09 |                 0      |                0      |                      2.144  |                     0.8993 |                       16.5995 |                      15.9407 |                      15 |                       0.0017 |                      0.0258 |
| MACD              |                    -0.0077 |                    1.4521 |                5.35821e+06 |               2.07522e+07 |                 0.206  |                0.1565 |                     67.7342 |                   257.906  |                       67.1457 |                     258.093  |                     526 |                       0.0076 |                      0.1145 |
| Optimized         |                    -0.2669 |                    0.3057 |               -1.081       |               0.9228      |                 0.2837 |                0.1928 |                      0.5606 |                     0.4669 |                       -0.6411 |                       0.5316 |                    2730 |                       0.363  |                      5.4446 |

## Performance by Cryptocurrency

### BTC-USD

|                            |   total_return |   sharpe_ratio |   win_rate |   profit_factor |
|:---------------------------|---------------:|---------------:|-----------:|----------------:|
| ('AdaptiveBollinger', 'D') |        -0.0265 |   -1.535       |     0.3288 |          0.5987 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |       1000      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'D')      |         0.1693 |    2.2112      |     0.4821 |          1.2643 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |       1000      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |       1000      |
| ('Bollinger', 'D')         |        -0.2551 |   -0.745       |     0.4051 |          0.9714 |
| ('Bollinger', 'M')         |        -0.4044 |   -0.8037      |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5185 |   -1.0185      |     0.3636 |          0.6742 |
| ('BuyAndHold', 'D')        |         5.0869 |   12.4894      |     0      |          1.3823 |
| ('BuyAndHold', 'M')        |         3.3733 |    4.43875e+06 |     0      |          4.2667 |
| ('BuyAndHold', 'W')        |         5.0869 |   76.6027      |     0      |          2.3173 |
| ('MACD', 'D')              |        -0.5983 |   -1.9688      |     0.1979 |          0.7977 |
| ('MACD', 'M')              |         0      |    0           |     0      |       1000      |
| ('MACD', 'W')              |        -0.4134 |   -1.0366      |     0.4091 |          0.6779 |
| ('Optimized', 'D')         |        -0.6266 |   -1.9923      |     0.4769 |          0.8362 |
| ('Optimized', 'M')         |        -0.1229 |   -2.4546      |     0      |          0      |
| ('Optimized', 'W')         |        -0.5425 |   -1.3019      |     0.4096 |          0.5551 |

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
| ('Bollinger', 'M')         |        -0.0677 |        -2.3926 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.1243 |        -0.2817 |     0.4444 |          1.0319 |
| ('BuyAndHold', 'D')        |         2.2944 |         4.8716 |     0      |          1.2272 |
| ('BuyAndHold', 'M')        |         1.4938 |      8394.88   |     0      |          2.6466 |
| ('BuyAndHold', 'W')        |         2.2944 |        14.4693 |     0      |          1.6543 |
| ('MACD', 'D')              |        -0.565  |        -1.6872 |     0.1948 |          0.8273 |
| ('MACD', 'M')              |        -0.473  |        -0.6382 |     0      |          0      |
| ('MACD', 'W')              |        -0.3445 |        -0.6791 |     0.45   |          0.8664 |
| ('Optimized', 'D')         |         0.1338 |         0.3688 |     0.5015 |          1.0591 |
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
| ('Bollinger', 'D')         |        -0.6685 |        -0.962  |     0.4366 |          0.9315 |
| ('Bollinger', 'M')         |        -0.2404 |        -1.195  |     0      |          0      |
| ('Bollinger', 'W')         |        -0.3662 |        -0.4819 |     0.2667 |          1.0623 |
| ('BuyAndHold', 'D')        |         6.1184 |         8.2572 |     0      |          1.3493 |
| ('BuyAndHold', 'M')        |         2.1086 |     56294.3    |     0      |          2.4309 |
| ('BuyAndHold', 'W')        |         6.1184 |        57.4126 |     0      |          2.0891 |
| ('MACD', 'D')              |        -0.7469 |        -1.3822 |     0.0769 |          0.8454 |
| ('MACD', 'M')              |         0.1927 |         2.4287 |     0.3333 |          1.4856 |
| ('MACD', 'W')              |        -0.9653 |        -0.5874 |     0.2353 |          0.24   |
| ('Optimized', 'D')         |         0.0152 |         0.229  |     0.3333 |          1.197  |
| ('Optimized', 'M')         |        -0.1923 |        -1.4197 |     0      |          0      |
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
| ('Bollinger', 'D')         |        -0.8839 |   -1.4428      |     0.4648 |          0.8273 |
| ('Bollinger', 'M')         |         0.0282 |    3.817       |     0      |       1000      |
| ('Bollinger', 'W')         |        -0.905  |   -0.5598      |     0.3333 |          0.5941 |
| ('BuyAndHold', 'D')        |        22.1441 |   29.1458      |     0      |          1.3752 |
| ('BuyAndHold', 'M')        |         8.6453 |    1.24383e+10 |     0      |          3.623  |
| ('BuyAndHold', 'W')        |        22.1441 |  965.81        |     0      |          2.2    |
| ('MACD', 'D')              |        -0.6555 |   -1.3958      |     0.3039 |          0.8754 |
| ('MACD', 'M')              |         4.9977 |    8.0373e+07  |     0      |          4.2374 |
| ('MACD', 'W')              |        -0.8181 |   -0.6992      |     0.3478 |          0.5758 |
| ('Optimized', 'D')         |        -0.6758 |   -1.4437      |     0.4495 |          0.8814 |
| ('Optimized', 'M')         |        -0.0622 |   -1.7557      |     0.25   |          0.2726 |
| ('Optimized', 'W')         |        -0.8379 |   -0.6957      |     0.3425 |          0.5567 |

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
| ('Bollinger', 'M')         |        -0.227  |        -1.7753 |     0      |          0      |
| ('Bollinger', 'W')         |        -0.5951 |        -1.015  |     0.3636 |          0.6334 |
| ('BuyAndHold', 'D')        |         1.9251 |         4.4467 |     0      |          1.2221 |
| ('BuyAndHold', 'M')        |         1.2862 |      3327.54   |     0      |          2.6982 |
| ('BuyAndHold', 'W')        |         1.9251 |        11.659  |     0      |          1.6779 |
| ('MACD', 'D')              |        -0.4938 |        -1.7277 |     0.2553 |          0.8373 |
| ('MACD', 'M')              |         0.6926 |       140.072  |     0      |          2.5749 |
| ('MACD', 'W')              |         0.0752 |         0.269  |     0.2857 |          1.1714 |
| ('Optimized', 'D')         |        -0.4341 |        -1.3144 |     0.4732 |          0.919  |
| ('Optimized', 'M')         |        -0.1198 |        -2.0889 |     0      |          0      |
| ('Optimized', 'W')         |        -0.2743 |        -0.7774 |     0.3293 |          0.8425 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| BuyAndHold | SOL-USD  | W           |       22.1441  |
| BuyAndHold | SOL-USD  | D           |       22.1441  |
| BuyAndHold | SOL-USD  | M           |        8.64527 |
| BuyAndHold | XRP-USD  | D           |        6.11837 |
| BuyAndHold | XRP-USD  | W           |        6.11837 |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |    sharpe_ratio |
|:-----------|:---------|:------------|----------------:|
| BuyAndHold | SOL-USD  | M           |     1.24383e+10 |
| MACD       | SOL-USD  | M           |     8.0373e+07  |
| BuyAndHold | BTC-USD  | M           |     4.43875e+06 |
| BuyAndHold | XRP-USD  | M           | 56294.3         |
| BuyAndHold | ETH-USD  | M           |  8394.88        |

### By win_rate
| strategy     | symbol   | timeframe   |   win_rate |
|:-------------|:---------|:------------|-----------:|
| Optimized    | ETH-USD  | D           |   0.501471 |
| AdaptiveMACD | BTC-USD  | D           |   0.482143 |
| Optimized    | BTC-USD  | D           |   0.476879 |
| AdaptiveMACD | XRP-USD  | D           |   0.474227 |
| Optimized    | BNB-USD  | D           |   0.473244 |

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
| AdaptiveMACD      |    0.4689      |        -0.0254 |          667.352  |
| Bollinger         |   -0.6204      |        -0.529  |           66.0085 |
| BuyAndHold        |    8.29519e+08 |        -0.3674 |           16.5995 |
| MACD              |    5.35821e+06 |        -0.5067 |           67.1457 |
| Optimized         |   -1.081       |        -0.3974 |           -0.6411 |

### Trading Efficiency
| strategy          |   ('win_rate', 'mean') |   ('profit_factor', 'mean') |   ('num_trades', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |
|:------------------|-----------------------:|----------------------------:|-------------------------:|------------------------:|-----------------------------:|
| AdaptiveBollinger |                 0.0939 |                    667.104  |                  22.8667 |                     343 |                       1.6854 |
| AdaptiveMACD      |                 0.1521 |                    667.074  |                 128      |                    1920 |                       1.6641 |
| Bollinger         |                 0.2639 |                     67.2516 |                  29.3333 |                     440 |                       0.4402 |
| BuyAndHold        |                 0      |                      2.144  |                   1      |                      15 |                       0.0017 |
| MACD              |                 0.206  |                     67.7342 |                  35.0667 |                     526 |                       0.0076 |
| Optimized         |                 0.2837 |                      0.5606 |                 182      |                    2730 |                       0.363  |

### Performance by Timeframe
|                            |   total_return |   sharpe_ratio |   win_rate |
|:---------------------------|---------------:|---------------:|-----------:|
| ('AdaptiveBollinger', 'D') |         0.0079 |    0.1626      |     0.2818 |
| ('AdaptiveBollinger', 'M') |         0      |    0           |     0      |
| ('AdaptiveBollinger', 'W') |         0      |    0           |     0      |
| ('AdaptiveMACD', 'D')      |         0.1594 |    1.4068      |     0.4564 |
| ('AdaptiveMACD', 'M')      |         0      |    0           |     0      |
| ('AdaptiveMACD', 'W')      |         0      |    0           |     0      |
| ('Bollinger', 'D')         |        -0.3963 |   -0.72        |     0.4373 |
| ('Bollinger', 'M')         |        -0.1823 |   -0.4699      |     0      |
| ('Bollinger', 'W')         |        -0.5018 |   -0.6714      |     0.3543 |
| ('BuyAndHold', 'D')        |         7.5138 |   11.8421      |     0      |
| ('BuyAndHold', 'M')        |         3.3814 |    2.48856e+09 |     0      |
| ('BuyAndHold', 'W')        |         7.5138 |  225.191       |     0      |
| ('MACD', 'D')              |        -0.6119 |   -1.6324      |     0.2058 |
| ('MACD', 'M')              |         1.082  |    1.60746e+07 |     0.0667 |
| ('MACD', 'W')              |        -0.4932 |   -0.5466      |     0.3456 |
| ('Optimized', 'D')         |        -0.3175 |   -0.8305      |     0.4469 |
| ('Optimized', 'M')         |        -0.1718 |   -1.7014      |     0.1    |
| ('Optimized', 'W')         |        -0.3115 |   -0.711       |     0.3041 |

