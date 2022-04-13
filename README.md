# Lotka-Volterra
This simple simulation shows how complex behaviour can arise from a very simple set of initial rules. In this case, the sim models the predator-prey relationship and demonstrates the mutually inter-related population dynamics modelled by the [Lotka-Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations).

The rules are as follows:
Each site has three states: wolf, sheep or empty.

1. Pick a site (only stochastic updates allowed), and a neighbour.
2. If a wolf is adjacent to a sheep, the sheep gets eaten (becomes wolf with probability r). Otherwise the wolf dies with probability p.
3. If a sheep is adjacent to empty ground, it reproduces with probability q.
4. If empty ground is adjacent to anything, the thing moves into empty ground.

Other assumptions - there is an unlimited supply of grass for the sheep to eat, sheep only die from wolves, and wolves only eat sheep.

The sim is run for 5000 ticks, or until one species goes extinct, whichever comes first. A plot showing populations for the two species is then displayed:

