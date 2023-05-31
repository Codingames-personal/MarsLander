# Operation of the algorithm


## Evolution

### Selection

#### Steps
* get score : diversity 
* sort the chromosomes by score
* extract the best chromosome
* create new chromosomes
* return best chromosome

### Mutation

#### Cumulativ wheel
* calculate the size
* calculate the total score
* create the cumulativ score list
* create couple of chromosome 

#### Steps
* takes a couple of chromosome with the wheel
* create two childs by crossover
* mutate the childs
* add the childs to the new population

### Population switch
#### Steps
* copy the new population on the old one
* empties the new population

### Final
#### Steps
* Evolution number increment
* return the best chromosome


