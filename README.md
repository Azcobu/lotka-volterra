## Lotka-Volterra
This simple simulation shows how complex behaviour can arise from a very simple set of initial rules. In this case, the sim models the predator-prey relationship and demonstrates the mutually inter-related population dynamics modelled by the [Lotka-Volterra equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations).

The sim in action:

![Screen](/img/lotvolt-screen.jpg?raw=true "Screen")

## Rules
Each site has three states: wolf, sheep or empty.

1. Pick a site (only stochastic updates allowed), and a neighbour.
2. If a wolf is adjacent to a sheep, the sheep gets eaten (becomes wolf with probability r). Otherwise the wolf dies with probability p.
3. If a sheep is adjacent to empty ground, it reproduces with probability q.
4. If empty ground is adjacent to anything, the thing moves into empty ground.

Other assumptions - there is an unlimited supply of grass for the sheep to eat, sheep only die from wolves, and wolves only eat sheep.

The sim is run for 5000 ticks, or until one species goes extinct, whichever comes first. A plot showing populations for the two species is then displayed:

![Plot](/img/lotvolt-graph.png?raw=true "Plot")

The complex mututal relationship between predator and prey numbers is clearly shown here, with every great population boom for one side or the other followed by an equal crash.

### Other variants
I also wrote a version where the sheep were also constrained by limited food. In this version, grass was not infinite, but disppeared when eaten, and only regrew over time. This forced the sheep to constantly migrate in search of food. However, this variant resulted in a sharply-reduced sheep population (as you would expect) and a wolf population that was so low the sim usually ended fairly quickly.
