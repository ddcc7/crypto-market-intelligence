# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 13:46:17

## Overall Strategy Performance

| strategy   |   ('total_return', 'mean') |   ('sharpe_ratio', 'mean') |   ('win_rate', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:-----------|---------------------------:|---------------------------:|-----------------------:|------------------------:|-----------------------------:|----------------------------:|
| Bollinger  |                5.48888e+40 |                1.932e+39   |                 0.3409 |                    1918 |                       0.0092 |                      0.1375 |
| BuyAndHold |                6.3215      |                8.2707e+08  |                 0      |                      15 |                       0.0016 |                      0.0236 |
| MACD       |               -0.0072      |                5.32877e+06 |                 0.2067 |                     526 |                       0.0114 |                      0.1715 |

## Performance by Cryptocurrency

### BTC-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1.0376 |   -0.0474      |     0.4564 |
| ('Bollinger', 'M')  |        -0.4307 |   -0.7923      |     0      |
| ('Bollinger', 'W')  |        -1      |   -0.0883      |     0.4375 |
| ('BuyAndHold', 'D') |         5.0655 |   12.4365      |     0      |
| ('BuyAndHold', 'M') |         3.3579 |    4.27019e+06 |     0      |
| ('BuyAndHold', 'W') |         5.0655 |   75.921       |     0      |
| ('MACD', 'D')       |        -0.5969 |   -1.9641      |     0.2083 |
| ('MACD', 'M')       |         0      |    0           |     0      |
| ('MACD', 'W')       |        -0.4134 |   -1.0366      |     0.4091 |

### ETH-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1      |        -0.0495 |     0.4371 |
| ('Bollinger', 'M')  |        -0.0614 |        -2.4631 |     0      |
| ('Bollinger', 'W')  |        -0.9964 |        -0.1078 |     0.4286 |
| ('BuyAndHold', 'D') |         2.275  |         4.8317 |     0      |
| ('BuyAndHold', 'M') |         1.4791 |      7869.54   |     0      |
| ('BuyAndHold', 'W') |         2.275  |        14.2439 |     0      |
| ('MACD', 'D')       |        -0.5623 |        -1.6799 |     0.1948 |
| ('MACD', 'M')       |        -0.473  |        -0.6382 |     0      |
| ('MACD', 'W')       |        -0.3445 |        -0.6791 |     0.45   |

### XRP-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1.0019 |   -0.1122      |     0.5075 |
| ('Bollinger', 'M')  |        -0.2445 |   -1.1783      |     0      |
| ('Bollinger', 'W')  |        -0.9987 |   -0.1883      |     0.5667 |
| ('BuyAndHold', 'D') |         6.1422 |    8.2892      |     0      |
| ('BuyAndHold', 'M') |         4.9537 |    3.17686e+07 |     0      |
| ('BuyAndHold', 'W') |         6.1422 |   57.9009      |     0      |
| ('MACD', 'D')       |        -0.7477 |   -1.3838      |     0.0769 |
| ('MACD', 'M')       |         0.1967 |    2.5299      |     0.3333 |
| ('MACD', 'W')       |        -0.9653 |   -0.5874      |     0.2353 |

### SOL-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |    8.23332e+41 |    2.898e+40   |     0.4548 |
| ('Bollinger', 'M')  |    0.0287      |    3.8265      |     0.5    |
| ('Bollinger', 'W')  |    1.5607e+06  |    7.47739e+13 |     0.3947 |
| ('BuyAndHold', 'D') |   22.1326      |   29.1307      |     0      |
| ('BuyAndHold', 'M') |    8.6405      |    1.237e+10   |     0      |
| ('BuyAndHold', 'W') |   22.1326      |  964.607       |     0      |
| ('MACD', 'D')       |   -0.6554      |   -1.3954      |     0.3039 |
| ('MACD', 'M')       |    4.9947      |    7.99315e+07 |     0      |
| ('MACD', 'W')       |   -0.8181      |   -0.6992      |     0.3478 |

### BNB-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1      |        -0.0702 |     0.4722 |
| ('Bollinger', 'M')  |        -0.3102 |        -1.3062 |     0      |
| ('Bollinger', 'W')  |        -1      |        -0.0977 |     0.4583 |
| ('BuyAndHold', 'D') |         1.9336 |         4.4663 |     0      |
| ('BuyAndHold', 'M') |         1.2929 |      3434.57   |     0      |
| ('BuyAndHold', 'W') |         1.9336 |        11.7529 |     0      |
| ('MACD', 'D')       |        -0.4953 |        -1.7329 |     0.2553 |
| ('MACD', 'M')       |         0.6975 |       144.564  |     0      |
| ('MACD', 'W')       |         0.0752 |         0.269  |     0.2857 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    8.23332e+41 |
| Bollinger  | SOL-USD  | W           |    1.5607e+06  |
| BuyAndHold | SOL-USD  | D           |   22.1326      |
| BuyAndHold | SOL-USD  | W           |   22.1326      |
| BuyAndHold | SOL-USD  | M           |    8.64046     |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |   sharpe_ratio |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    2.898e+40   |
| Bollinger  | SOL-USD  | W           |    7.47739e+13 |
| BuyAndHold | SOL-USD  | M           |    1.237e+10   |
| MACD       | SOL-USD  | M           |    7.99315e+07 |
| BuyAndHold | XRP-USD  | M           |    3.17686e+07 |

### By win_rate
| strategy   | symbol   | timeframe   |   win_rate |
|:-----------|:---------|:------------|-----------:|
| Bollinger  | XRP-USD  | W           |   0.566667 |
| Bollinger  | XRP-USD  | D           |   0.507508 |
| Bollinger  | SOL-USD  | M           |   0.5      |
| Bollinger  | BNB-USD  | D           |   0.472222 |
| Bollinger  | BNB-USD  | W           |   0.458333 |

