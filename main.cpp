#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <cmath>
#include <bits/stdc++.h>

using namespace std;
using std::map;
using std::string;

const int NUMBER_EVOLUTION = 1;
const int POPULATION_SIZE = 60;
const int CHROMOSOME_SIZE = 60;

const float GRADED_RETAIN_PERCENT = 0.2;
const float MUTATION_PROBABILITY = 0.01;

const int VERTICAL_SIZE = 7000;
const int HORIZONTAL_SIZE = 3000;

const int MAX_SPEED = 150;//Estimation, not the real max_speed
const int MAX_ROTATE = 90;

const int MAX_ROTATE_COMMAND = 15;

const float GRAVITY = -3.711;

float random_percent(){
    return (rand() % 10000)/10000;
}

float norm(float x, float y){
    return sqrt(pow(x, 2) + pow(y, 2));
}
class Action
{
    public :
        int rotate_;
        int power_;

        Action(const int& rotate, const int& power): rotate_(rotate), power_(power) {}
        
        Action(){
            rotate_ = rand() % 31 - 15;
            power_ = rand() % 3 - 1;
        }

        bool operator==(const Action& other){
            return (rotate_ == other.rotate_ && power_ == other.power_);
        }

        bool operator!=(const Action& other){
            return (rotate_ != other.rotate_ || power_ != other.power_);
        }

        Action crossover(const Action& other, const float& random){
            return Action(
                round( rotate_*random + other.rotate_*(1-random) ),
                round( power_*random + other.power_*(1-random) )
            );
        }   

        void mutation(){
            rotate_ = rand() % 31 - 15;
            power_ = rand() % 3 - 1;
        }

        void last_action(int rotate){
            if (abs(rotate) <= MAX_ROTATE_COMMAND){
                rotate_ = -rotate;
            }
        }
};

class Point
{
    public :
        int x_;
        int y_;

        Point(int x, int y): x_(x), y_(y) {}
        Point(){
            x_ = 0;
            y_ = 0;
        }

        bool operator==(Point other){
            return (x_ == other.x_ && y_ == other.y_);
        }

        float distance(const Point& other){
            return norm(x_ - other.x_, y_ - other.y_);
            }
};

class Segment
{
    public :
        static bool ccw(Point A, Point B, Point C){
            return ((C.y_ - A.y_) * (B.x_ - A.x_) > (B.y_ - A.y_) * (C.x_ - A.x_));
        }

        Point point_left_;
        Point point_right_;
        float length_;
        
        Segment(){
            point_left_ = Point();
            point_right_ = Point();
            length_ = 0;
        }

        Segment(Point point_left, Point point_right): point_left_(point_left), point_right_(point_right){
            length_ = point_left_.distance(point_right_);
        }

        bool operator==(Segment other){
            return (point_left_ == other.point_left_ && point_right_ == other.point_right_);
        }

    bool intersect(Segment other){
        bool cond_1 = Segment::ccw( point_left_, other.point_left_, other.point_right_) != Segment::ccw( point_right_, other.point_left_, other.point_right_);
        bool cond_2 =  Segment::ccw( point_left_,  point_right_, other.point_left_) != Segment::ccw( point_left_, point_right_, other.point_right_);
        return (cond_1 && cond_2);
    }        
};

class Shuttle
{
    public :
        int x_, y_, h_speed_, v_speed_, fuel_, rotate_, power_;    
        
        void update(int x, int y, int h_speed, int v_speed, int fuel, int rotate, int power){
            x_ = x; y_ = y ; h_speed_ = h_speed; v_speed_ = v_speed; fuel_ = fuel; rotate_ = rotate; power_ = power;
        }
};

class MarsEnvironment
{
    public :
        
        int x_, y_, h_speed_, v_speed_, fuel_, rotate_, power_;
        Segment landing_site_;
        vector<Point> lands_;
        vector<Segment> surface_;
        Shuttle shuttle_;
        Segment collision_site_;
        Segment trajectory_;
        float distance_max_;

        MarsEnvironment(int surface_n, vector<Point> lands): lands_(lands) {
            bool first = true;
            Point point_left;
            for (Point point_right : lands_){
                if (first){first = false;}
                else{
                    surface_.push_back(Segment(point_left, point_right));
                }
                point_left = point_right;
            }
            findLandingSite();
            findMaxDistance();
        }

        void reset(vector<int> initial_params){
            shuttle_.update(initial_params[0], initial_params[1], initial_params[2], initial_params[3], initial_params[4], initial_params[5], initial_params[6]);
        }

        bool step(Action action){
            int rotate = max(-15, min(15, action.rotate_ + shuttle_.rotate_));
            int power = max(0, min(4, action.power_ + shuttle_.power_));
            
            int h_accel = - round(sin(rotate)*power);
            int v_accel = round(GRAVITY + cos(rotate)*power);

            int h_speed = shuttle_.h_speed_ + h_accel;
            int v_speed = shuttle_.v_speed_ + v_accel;

            int x = shuttle_.x_ + h_speed;
            int y = shuttle_.y_ + v_speed;

            int fuel = shuttle_.fuel_ - power;

            trajectory_ = Segment(Point(shuttle_.x_, shuttle_.y_), Point(x, y) );

            if (exitZone(x, y) || collision() || fuel == 0){
                return false;
            }
            shuttle_.update(x, y, h_speed, v_speed, fuel, rotate, power);
            return true;
        }
        
        bool exitZone(int x, int y){
            bool space_x = (0 <= x && x < VERTICAL_SIZE);
            bool space_y = (0 <= y && y < HORIZONTAL_SIZE);
            return (!space_x || !space_y);
        }

        int getScoreLanding(){
            if (landingOnSite()){
                return 200;
            }
            return round(50*(1 - distance()/distance_max_));
        }

        int getScoreSpeed(){
            int score;
            if (landingOnSite()){
                score = min(0, 40 - abs(shuttle_.v_speed_));
                score+= min(0, 20 - abs(shuttle_.h_speed_));
            }
            else{
                score = round(50*(1 - norm(shuttle_.v_speed_, shuttle_.h_speed_)));
            }
            return score;
        }

        int getScoreRotate(){
            return round(20*(1 - abs(shuttle_.rotate_)/MAX_ROTATE));
        }

        int getScore(){
            if (exitZone(shuttle_.x_, shuttle_.y_)){
                return 0;
            }
            int score = getScoreLanding() + getScoreSpeed();
            if (landingOnSite()){
                return max(100, min(200, score)) + getScoreRotate();
            }
            else{
                return max(0, min(100, score));
            }
        }

        bool successfulLanding(){
            bool correct_speed = (abs(shuttle_.v_speed_) <= 40 && abs(shuttle_.h_speed_) <= 20);
            bool correct_angle = abs(shuttle_.rotate_) == 0;
            return (correct_speed && correct_angle && landingOnSite());
        }

    private :

        void findMaxDistance(){
            float distance = 0.;
            float distance_left;
            for (Segment site : surface_){
                if (site == landing_site_){
                    distance_left = distance;
                    distance = 0;
                }
                else{
                    distance += site.length_;
                }
            distance_max_ = max(distance_left, distance);
            }
        }

        float distance(){
            //Give the distance by following eachs sites to the landing site
            Point point_from, point_to, point_end, point_temp;
            Point point_shuttle = Point(shuttle_.x_, shuttle_.y_);
            bool run = false;
            float distance_collision;
            for (Point point : lands_){
                if (!run){
                    if (point == collision_site_.point_left_){
                        point_from = point;
                        point_to = collision_site_.point_right_;
                        point_end = landing_site_.point_left_;
                        distance_collision = point_shuttle.distance(collision_site_.point_right_);
                        run = true;
                    }
                    else if (point == landing_site_.point_right_){
                        point_from = landing_site_.point_left_;
                        point_to = point;
                        point_end = collision_site_.point_left_;
                        distance_collision = collision_site_.point_left_.distance(point_shuttle);
                        run = true;
                    }
                }
                else{
                    point_temp = point_to;
                    point_to = point;
                    point_from = point_temp;
                    distance_collision += point_from.distance(point_to);
                    if (point_to == point_end){
                        break;
                    }
                }
            }
            return distance_collision;
        }
        
        bool collision(){
            for (Segment &site : surface_){
                if (trajectory_.intersect(site)){
                    collision_site_ = site;
                    return true;
                }
            }
            return false;
        }

        bool landingOnSite(){
            return (collision_site_ == landing_site_);
        }

        bool findLandingSite(){
            for (Segment &segment : surface_){
                if (segment.point_left_.y_ == segment.point_right_.y_){
                    landing_site_ = segment;
                    return true;
                }
            }
            return false;
        }      
};



class Chromosome
{
    public :
        
        static bool compare_score(const Chromosome& c_a, const Chromosome& c_b){
            return (c_a.score_ < c_b.score_);
        }

        vector<Action> genes_;
        float score_;

        Chromosome(){
            for (int i = 0; i<CHROMOSOME_SIZE; i++){
                genes_[i] = Action();
            }
            score_ = 0;
        }

        Chromosome(vector<Action> genes): genes_(genes){
            score_ = 0;
        }

        bool operator==(const Chromosome& other){
            for (int i=0; i<CHROMOSOME_SIZE; i++){
                if (genes_[i] != other.genes_[i]){
                    return false;
                }
            }
            return true;
        }
        void mutation(const float& random){
            for (Action &gene : genes_){
                if (random_percent() > random){
                    gene.mutation();
                }
            }
        }

        Chromosome crossover(const Chromosome& other, float random){
            vector<Action> new_genes;
            for (int i = 0; i<CHROMOSOME_SIZE; i++){
                new_genes.push_back(genes_[i].crossover(other.genes_[i], random));
            }
            return Chromosome(new_genes);
        }

        bool use(MarsEnvironment environment){
            for (Action &action : genes_){
                if (environment.step(action)){
                    if (!environment.exitZone(environment.shuttle_.x_, environment.shuttle_.y_)){
                        action.last_action(environment.shuttle_.rotate_);
                    }
                    score_ = environment.getScore();
                    break;
                }
            }
            

            if (score_ > 100 && environment.successfulLanding()){
                return true;
            }
            else{
                return false;
            }

        }
};

class Population
{
    public :
        vector<Chromosome> population_;
        float total_score_;

        Population(){
            for (int i = 0; i<POPULATION_SIZE; i++){
                population_[i] = Chromosome();
            }
            total_score_ = 0;
        }

        Population(std::vector<Chromosome> population): population_(population){
            total_score_ = 0;
        }

        void selection(){
            for (Chromosome &chromosome : population_){
                chromosome.score_ /= total_score_;
            }
            float cumulative_score = 0.;
            sort(population_.begin(), population_.end(), Chromosome::compare_score);
            vector<Chromosome> elit_population = population_;

            for (Chromosome &chromosome : population_){
                cumulative_score += chromosome.score_;
                chromosome.score_ += cumulative_score;
            }

            vector<Chromosome> new_population;
            Chromosome parent;
            bool paired = false;
            while (new_population.size() < POPULATION_SIZE){
                float random = random_percent();
                int i = 0;
                while (population_[i].score_ < random){
                    i++;
                }
                if (!paired){
                    parent = population_[i];
                    paired = true;
                }
                else {
                    float random = random_percent();
                    Chromosome child0 = parent.crossover(population_[i], random);
                    Chromosome child1 = population_[i].crossover(parent, random);
                    child0.mutation(MUTATION_PROBABILITY);
                    child1.mutation(MUTATION_PROBABILITY);
                    new_population.push_back(child0);
                    new_population.push_back(child1);
                    paired = false;
                }
            } 
            for (int i=0; i<POPULATION_SIZE*GRADED_RETAIN_PERCENT; i++){
                new_population[i] = elit_population[i];
            }
            population_ = new_population;
        }
};

const int INPUT_SIZE = 7;
vector<int> console_input(){
    vector<int> input;
    int input_var;
    for (int i = 0; i < INPUT_SIZE; i++){
        cin >> input_var;
        input.push_back(input_var);
    }
    cin.ignore();
}

void print(int rotate, int power){
    cout << rotate << " " << power << endl;
}

class EnvCodingame : public MarsEnvironment
{
    public :
        EnvCodingame(int surface_n, vector<Point> lands): MarsEnvironment(surface_n, lands){}

        void step(Action action){
            MarsEnvironment::step(action);
            print(rotate_, power_);
        }
};



int main(){
    int surface_n, land_x, land_y;
    vector<Point> lands;
    vector<int> initial_input;

    cin >> surface_n; cin.ignore();
    for (int i = 0; i < surface_n; i++){
        cin >> land_x >> land_y; cin.ignore();
        lands.push_back(Point(land_x,land_y));
    }
    initial_input = console_input();

    Population population = Population();
    MarsEnvironment env = MarsEnvironment(surface_n, lands);
    env.reset(initial_input);
    Chromosome the_one;
    
    for (int i = 0; i < NUMBER_EVOLUTION; i++){
        for (Chromosome chromosome : population.population_){
            if (chromosome.use(env)){
                the_one = chromosome;
                goto end;
            }
            env.reset(initial_input);
        }
        population.selection();
    }
    cout << "No solution found" << endl;
    return 0;
    
    end : 

    EnvCodingame env_use = EnvCodingame(surface_n, lands);
    env_use.reset(initial_input);
    int x, y, h_speed, v_speed, fuel, rotate, power;
    while (true){
        the_one.use(env_use);
        cin >> x >> y >> h_speed >> v_speed >> fuel >> rotate >> power; cin.ignore();
    }

}