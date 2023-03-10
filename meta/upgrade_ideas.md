# Upgrade idea

## Rewards

### General
* The calcul is made at the end of the calcul of each chromosome
* Calcul the score of each chromosome when all of them have already their trajectory calculated


### Diversity
* By the minimal distance between a chromosome and all of the other
* Distance between each points of the chromosome and the last best one


### Trajectory
A reward based on the trajectory and not the landing.
* Maximal speed during the trajectory
* Maximal rotation during the trajectory

#### Cons
It go against weird but interesting trajectory.

## Variation of constants 
### mutation probability
Increase the mutation probability when the score do not increase. 
It will permits the creation of new weirds trajectory that can escape trajectory holes.

### graded retain percent
Increase the graded retain percent when the score do not increase.
It will permits to extend the number of trajectory to use for the creation of new ones and so try to destroy trajectory holes.

## Do not have uniform dispersion of action

It is difficult to have a trajectory that work with a big speed of fall. From this observation we can try to find a dispersion of action and especially for the thrust power that is not uniform. 
Because during a lot of time, we will have a high thrust power we can propose different dispersion of power command {-1, 0, 1} :
|-1 | 0| 1|
|:-:| :-:|:-:|
|0.33| 0.33| 0.33|
|0.3 |0.3 |0.4|
|0.2 |0.3 |0.5|
|0.1 |0.4 |0.5|

But by analyzing a successful chromosome on the reverse cave we have determine : 

| Experience   | graded -1 | graded 0 | graded 1 |
|---           | :-:       | :-:      | :-:      |
|reverse cave  |0.11       |0.7375    |0.1523    |
|cave          |0.1425     |0.71      |0.1475    |  
|not special   |0.275      |0.43      |0.295     |
|cave 2        |0.115      |0.7175    |0.1675    |
|reverse cave 2|0.0925     |0.76      |0.1475    |

=> 0.25 | 0.4 | 0.35

## Behavior initial incoding
Create no random chromosome with really basic trajectory.

## Create little behavior 
By creating a kind of micro action, the trajectory will me more smooth and easier to calculate. With less calcul by chromosome, we can augment significantly the range of the population.



