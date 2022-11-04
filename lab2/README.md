
# Lab 2 - set covering with evolutionary algorithms

Test with various evolutionary algorithms on the set covering problem.
After a while I realized that my code favors a lot an explorative approach rather than an exploitative one.
This is mostly due to the tweak or mutation function, which incorporates a "drop" feature, where a solution gets dropped and rebuilt from scratch adding random lists from the pool, instead of mutated.
At the present time I have a persistend error on the last algorithm, mostly due to messy implementation of the new crossover and offspring generation functions, but they are mostly there on a conceptual level, they just need some debugging that I'll work on next week.

These are the results of each type of algorithm implemented:

## 1+1 EA algorithm

    SIGMA = 1
    STEPS = 1000

    N = 5, best solution: w=5 (bloat=0%)
    N = 10, best solution: w=10 (bloat=0%)
    N = 20, best solution: w=24 (bloat=20%)
    N = 100, best solution: w=211 (bloat=111%)
    N = 500, best solution: w=1663 (bloat=233%)
    N = 1000, best solution: w=4367 (bloat=337%)

## 1 + λ Evolution algorithm

    SIGMA = 1
    STEPS = 500
    OFFSPRING_SIZE = 40

    N = 5, best solution: w=5 (bloat=0%)
    N = 10, best solution: w=10 (bloat=0%)
    N = 20, best solution: w=24 (bloat=20%)
    N = 100, best solution: w=208 (bloat=108%)
    N = 500, best solution: w=1464 (bloat=193%)
    N = 1000, best solution: w=3705 (bloat=270%)

## 1, λ Evolution algorithm

    SIGMA = 2
    STEPS = 500
    OFFSPRING_SIZE = 40

    N = 5, best solution: w=5 (bloat=0%)
    N = 10, best solution: w=10 (bloat=0%)
    N = 20, best solution: w=24 (bloat=20%)
    N = 100, best solution: w=185 (bloat=85%)
    N = 500, best solution: w=1589 (bloat=218%)
    N = 1000, best solution: w=3613 (bloat=261%)

## 1, λ Adaptive algorithm

    SIGMA = 1
    STEPS = 500
    OFFSPRING_SIZE = 40
    SELF_ADAPTATION_EVERY = 100
    SELF_ADAPTATION_FACTOR = 0.5

    N = 5, best solution: w=5 (bloat=0%)
    N = 10, best solution: w=10 (bloat=0%)
    N = 20, best solution: w=24 (bloat=20%)
    N = 100, best solution: w=208 (bloat=108%)
    N = 500, best solution: w=1466 (bloat=193%)
    N = 1000, best solution: w=3806 (bloat=281%)

## Mu, Rho / Lambda Evolution Strategy

    MISSING