# Upgrade idea

## Rewards

### Distribution of rewards calculation time
Currently, the calculation of the score of each chromosome is done after the calculation of each of their trajectory but if we recalculate this score at the end of the generation, we can determine new criteria of scores which are done by comparing all chromosomes.


### Diversity
* By the minimal distance between a chromosome and all of the others
* Distance between each point of the chromosome and the last best one


### Trajectory
A reward based on the trajectory and not the landing.
* Maximal speed during the trajectory
* Maximal rotation during the trajectory

#### Cons
It go against weird but interesting trajectory.

## Variation of constants 
### mutation probability
Increase the mutation probability when the score does not increase. 
It will permits the creation of new weird trajectories that can escape trajectory holes.

### graded retain percent
Increase the graded retain percent when the score does not increase.
It will permits to extend the number of trajectories to use for the creation of new ones and so try to destroy trajectory holes.

## Do not have uniform dispersion of action

It is difficult to have a trajectory that work with a big speed of fall. From this observation we can try to find a dispersion of action and especially for the thrust power that is not uniform. 
Because during a lot of time, we will have a high thrust power we can propose different dispersions of power command :
|-1 | 0| 1|
|:-:| :-:|:-:|
|0.33| 0.33| 0.33|
|0.3 |0.3 |0.4|
|0.2 |0.3 |0.5|
|0.1 |0.4 |0.5|

But by analyzing a successful chromosome on different surface we have determine : 

| Surface      | graded -1 | graded 0 | graded 1 |
|---           | :-:       | :-:      | :-:      |
|reverse cave  |0.11       |0.7375    |0.1523    |
|cave          |0.1425     |0.71      |0.1475    |  
|not special   |0.275      |0.43      |0.295     |
|cave 2        |0.115      |0.7175    |0.1675    |
|reverse cave 2|0.0925     |0.76      |0.1475    |


## Behavior initial incoding
Create no random chromosome with really basic trajectory.

## Create little behavior 
By creating a kind of micro action, the trajectory will me more smooth and easier to calculate. With fewer calculations per chromosome, we significantly increase the range of the population.


## Fast trajectory by taking middlemen step
The idea is to not choose directly a successful trajectory but taking one of the best at a determined step.
I have two ideas to choose those new initial points : 
* With a uniform distribution : at each n steps, a new initial point will be chosen at a certain points on the trajectory of the actual best one.
* When a new trajectory offers a much better score than the other one, we directly choose it to take the new intial step.

## If I don't have any idea 
Reinforcement sutton bartol
Coarse Conding

We also have to choose where to take the new initial point. I also have to ideas for that :
* Choosing a fix lengh of trajectory that is kept
* Choose a point when the trajectory separates from the other

### Pro
I think that it really can decrease the calculation cost and, above all, distribute the calculation of the trajectory during its execution.

### Cons 
It really may leads to a not successful trajectory. For exemple if the last initial point leads to a fast vertical speed just before the landing, it may be impossible to slow down the shuttle enough. By increasing the score of the trajectory (maximal speed and other scores that I have to think about) it will be possible to minimize the possibility of having an initial point that cannot lead to a successful trajectory.
