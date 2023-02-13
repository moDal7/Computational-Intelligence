# Laboratory 3 - Nim Policy Search

Note: this laboratory was completed way after the deadline in the course. I finished it anyway for completeness and to prepare myself on the methods and techniques seen during the course.
I will state if and where any inspiration and ideas were taken from.

## Agent 0, Expert System

I tried to codify some common sense rules in order to create an agent who can consistently beat a random player.
The logic is to fully empty rows until there are only two rows remaining with elements in them, and at that point remove one element at the time from the longest.
When only one row remains and if possible, the agent takes the win.
It's a fairly basic strategy that mostly aims at not doing "losing" moves in critical moments in the game, but plays almost randomly in the rest of the game.

    INFO:root: Hard coded strategy vs. 'gabriele' -> 1.0
    INFO:root: Hard coded strategy vs. pure random -> 1.0

The agent consistently wins against the 'gabriele' strategy and the pure random strategy.

## Agent 1, Nim Sum or Optimal Strategy

This agent chooses moves solely based on the computation of Nim-Sum, and this guarantees that only the best possible moves are taken. If more moves are available, it randomly chooses a move among them. If by chance there is no move with positive nim sum, the agent implements the Hard Coded Agent behaviour.

    INFO:root: Optimal strategy w/ nim sum vs. Hard Coded -> 1.0
    INFO:root: Optimal strategy w/ nim sum vs. previous optimal strategy -> 1.0
    INFO:root: Previous optimal strategy vs. previous optimal strategy w/ nim sum -> 1.0

## Agent 2, Evolved Rules with Genome

This agent acts according to a genome selected through an Evolutionary Algorithm. The genome has 3 genes, each having 3 possible values. Each gene represents the policy in a different stage of the game, so early-game, mid-game, end-game.
Since the agent is naturally sub-optimal (we have already seen which is the behaviour of an optimal agent) the algorithm contemplates also sub-optimal or straight-up bad policy choices.

    INFO:root:Evolving strategy vs. pure random --> 0.86
    INFO:root:Evolving strategy vs. gabriele --> 1.0
    INFO:root:Evolving strategy vs. hard coded --> 1.0
    INFO:root:Evolving strategy vs. Nim sum --> 0.0

## Agent 3, Min-Max Agent

This agent implements the minmax algorithm to look for the best possible play. It is another optimal agent, but it suffers from higher computational times. The code was inspired by [this article](https://realpython.com/python-minimax-nim/) by Geir Arne on www.realpythton.com.
I also tested a version with lower level of depth and implemented alpha beta pruning. After these optimizations, for nim size=5, the algorithm takes approximately 1/5 of the time previously needed.

    INFO:root:min-max strategy vs. hard coded strategy --> 1.0

## Agent 4, Reinforcement Learning Agent

This agent proved quite tricky to setup, and I went through quite a lot of troubleshooting. I found some suggestions in the repo in [this article](https://towardsdatascience.com/practical-reinforcement-learning-02-getting-started-with-q-learning-582f63e4acd9), but unfortunately is not available anymore. I changed it a lot and performed some parameter tuning.
The parameters in this method where 3: alpha as the learning rate, or a general multiplier for the rewards; gamma, which is the multiplier of the maximum future q values among possible moves; and epsilon, which is an "exploitation vs. exploration" factor.
The model is only able to play with nim size=5 and as a starting player.
The learning procedure works as follows: from the first third of the training the opponent is the pure random strategy, then the opponent becomes the much more fearsom hard coded strategy.
The idea is to try and challenge the strategy more and more.

    INFO:root:q-learning strategy vs. pure random strategy --> 0.774
    INFO:root:q-learning strategy  vs. hard coded strategy --> 0.839
    INFO:root:q-learning strategy  vs. nim sum strategy strategy --> 0.0

Notably, the Q-Learning beats more often the hard-coded strategy than the pure random.
