#include <cmath>
#include <bits.stdc++.h>

using namespace std;
using std::map;
using std::string;
using chromosome = str;
using point = int[2];

const int POPULATION_SIZE = 100;
const int CHROMOSOME_SIZE = 100;

const float GRADED_RETAIN_PERCENT = 0.1;
const float MUTATION_PROBABILITY = 0.01;

const int VERTICAL_SIZE = 7000;
const int HORIZONTAL_SIZE = 3000;

const float GRAVITY = -3.711;

chromosome population[POPULATION_SIZE];
chromosome new_population[POPULATION_SIZE];

bool ccw(point a, point b, point c){
    return ((c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]));
}  
