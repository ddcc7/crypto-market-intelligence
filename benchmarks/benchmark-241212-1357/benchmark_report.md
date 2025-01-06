# Crypto Trading Strategy Benchmark Report

Generated on: 2024-12-12 13:57:54

## Overall Strategy Performance

| strategy   |   ('total_return', 'mean') |   ('sharpe_ratio', 'mean') |   ('win_rate', 'mean') |   ('num_trades', 'sum') |   ('execution_time', 'mean') |   ('execution_time', 'sum') |
|:-----------|---------------------------:|---------------------------:|-----------------------:|------------------------:|-----------------------------:|----------------------------:|
| Bollinger  |                8.40022e+40 |                2.95647e+39 |                 0.3408 |                    1919 |                       0.0087 |                      0.1304 |
| BuyAndHold |                6.3401      |                8.44556e+08 |                 0      |                      15 |                       0.002  |                      0.0304 |
| MACD       |               -0.006       |                5.44096e+06 |                 0.2067 |                     526 |                       0.0096 |                      0.1446 |

## Performance by Cryptocurrency

### BTC-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1.0387 |   -0.0474      |     0.4564 |
| ('Bollinger', 'M')  |        -0.4301 |   -0.7926      |     0      |
| ('Bollinger', 'W')  |        -1      |   -0.0883      |     0.4375 |
| ('BuyAndHold', 'D') |         5.0632 |   12.4306      |     0      |
| ('BuyAndHold', 'M') |         3.3562 |    4.25182e+06 |     0      |
| ('BuyAndHold', 'W') |         5.0632 |   75.8453      |     0      |
| ('MACD', 'D')       |        -0.5967 |   -1.9636      |     0.2083 |
| ('MACD', 'M')       |         0      |    0           |     0      |
| ('MACD', 'W')       |        -0.4134 |   -1.0366      |     0.4091 |

### ETH-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1      |        -0.0495 |     0.4358 |
| ('Bollinger', 'M')  |        -0.0654 |        -2.4178 |     0      |
| ('Bollinger', 'W')  |        -0.9965 |        -0.1079 |     0.4286 |
| ('BuyAndHold', 'D') |         2.2874 |         4.8572 |     0      |
| ('BuyAndHold', 'M') |         1.4885 |      8201.43   |     0      |
| ('BuyAndHold', 'W') |         2.2874 |        14.3877 |     0      |
| ('MACD', 'D')       |        -0.5641 |        -1.6846 |     0.1948 |
| ('MACD', 'M')       |        -0.473  |        -0.6382 |     0      |
| ('MACD', 'W')       |        -0.3445 |        -0.6791 |     0.45   |

### XRP-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1.0019 |   -0.1122      |     0.5075 |
| ('Bollinger', 'M')  |        -0.2519 |   -1.1495      |     0      |
| ('Bollinger', 'W')  |        -0.9987 |   -0.1884      |     0.5667 |
| ('BuyAndHold', 'D') |         6.1843 |    8.3459      |     0      |
| ('BuyAndHold', 'M') |         4.9888 |    3.38834e+07 |     0      |
| ('BuyAndHold', 'W') |         6.1843 |   58.7722      |     0      |
| ('MACD', 'D')       |        -0.7492 |   -1.3865      |     0.0769 |
| ('MACD', 'M')       |         0.2038 |    2.7171      |     0.3333 |
| ('MACD', 'W')       |        -0.9653 |   -0.5874      |     0.2353 |

### SOL-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |    1.26003e+42 |    4.4347e+40  |     0.4548 |
| ('Bollinger', 'M')  |    0.0269      |    3.7908      |     0.5    |
| ('Bollinger', 'W')  |    1.51601e+06 |    6.9604e+13  |     0.3947 |
| ('BuyAndHold', 'D') |   22.1763      |   29.1878      |     0      |
| ('BuyAndHold', 'M') |    8.6587      |    1.26302e+10 |     0      |
| ('BuyAndHold', 'W') |   22.1763      |  969.164       |     0      |
| ('MACD', 'D')       |   -0.656       |   -1.3968      |     0.3039 |
| ('MACD', 'M')       |    5.006       |    8.16142e+07 |     0      |
| ('MACD', 'W')       |   -0.8181      |   -0.6992      |     0.3478 |

### BNB-USD

|                     |   total_return |   sharpe_ratio |   win_rate |
|:--------------------|---------------:|---------------:|-----------:|
| ('Bollinger', 'D')  |        -1      |        -0.0702 |     0.4722 |
| ('Bollinger', 'M')  |        -0.3162 |        -1.2763 |     0      |
| ('Bollinger', 'W')  |        -1      |        -0.0978 |     0.4583 |
| ('BuyAndHold', 'D') |         1.9431 |         4.488  |     0      |
| ('BuyAndHold', 'M') |         1.3002 |      3556.94   |     0      |
| ('BuyAndHold', 'W') |         1.9431 |        11.8573 |     0      |
| ('MACD', 'D')       |        -0.497  |        -1.7385 |     0.2553 |
| ('MACD', 'M')       |         0.703  |       149.698  |     0      |
| ('MACD', 'W')       |         0.0752 |         0.269  |     0.2857 |

## Best Performing Strategy-Timeframe Combinations

### By total_return
| strategy   | symbol   | timeframe   |   total_return |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    1.26003e+42 |
| Bollinger  | SOL-USD  | W           |    1.51601e+06 |
| BuyAndHold | SOL-USD  | D           |   22.1763      |
| BuyAndHold | SOL-USD  | W           |   22.1763      |
| BuyAndHold | SOL-USD  | M           |    8.65866     |

### By sharpe_ratio
| strategy   | symbol   | timeframe   |   sharpe_ratio |
|:-----------|:---------|:------------|---------------:|
| Bollinger  | SOL-USD  | D           |    4.4347e+40  |
| Bollinger  | SOL-USD  | W           |    6.9604e+13  |
| BuyAndHold | SOL-USD  | M           |    1.26302e+10 |
| MACD       | SOL-USD  | M           |    8.16142e+07 |
| BuyAndHold | XRP-USD  | M           |    3.38834e+07 |

### By win_rate
| strategy   | symbol   | timeframe   |   win_rate |
|:-----------|:---------|:------------|-----------:|
| Bollinger  | XRP-USD  | W           |   0.566667 |
| Bollinger  | XRP-USD  | D           |   0.507508 |
| Bollinger  | SOL-USD  | M           |   0.5      |
| Bollinger  | BNB-USD  | D           |   0.472222 |
| Bollinger  | BNB-USD  | W           |   0.458333 |

