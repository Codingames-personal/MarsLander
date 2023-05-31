import math
import sys

from sources.tools.point import Point
from sources.action import Action
from sources.lander import Lander
from sources.surface import Surface

x_scale = 7000
y_scale = 3000


class EnvMarsLander:
    """ Environment of the Mars lander puzzle of CodinGames"""
    GRAVITY = - 3.711 # gravity on Mars m.s-2
    x_scale = 7000
    y_scale = 3000

    def __init__(self, lands : list, initial_state : list):
        self.lands = lands
        self.initial_state = initial_state
        self.lander = Lander()
        self.previous_lander = Lander()
        lands_points = \
            list(map(lambda obs : Point(obs[0], obs[1]), self.lands)) 
        self.surface = Surface(lands_points)


    def __str__(self) -> str:
        #return "\n".join([score_info,coord_info,speed_info,rotate_info,fuel_info])
        return str(self.lander)

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other) -> bool:
        
        return  self.surface == other.surface and\
                self.initial_state == other.initial_state and \
                self.lander == other.lander

    def landing_distance(self):
        """ Calculate the distance by "walke" of the collision to the landing site"""
        if self.landing_on_site():
            return 0 
        if self.lander.fuel <=0:
            return 10000
        
        point_lander = Point(self.lander.x, self.lander.y)
        run = False
        distance = 0
        for point in self.surface:
            if not run :
                if point == self.surface.collision_line.point_a: # from left to the right 
                    point_from = point
                    point_to = self.surface.collision_line.point_b
                    point_final = self.surface.landing_site.point_a
                    distance = point_lander.distance(self.surface.collision_line.point_b)
                    run = True

                elif point == self.surface.landing_site.point_b: # from right to the left
                    point_from = self.surface.landing_site.point_a
                    point_to = point
                    point_final = self.surface.collision_line.point_a
                    distance = self.surface.collision_line.point_a.distance(point_lander)
                    run = True
                    
            else:
                point_from, point_to = point_to, point
                distance += point_from.distance(point_to)
                if point == point_final:
                    break
        return distance

 
    def reset(self):
        """Reset the lander"""
        self.lander.update(*self.initial_state)
        self.maximal_speed = 0

    def exit_zone(self) -> bool:
        return not (0 <= self.lander.x < 7000 and 0 <= self.lander.y < 3000)

    def landing_on_site(self) -> bool:
        
        return self.surface.collision_line == self.surface.landing_site

    def landing_angle(self) -> bool:
        return self.lander.rotate == 0

    def landing_vertical_speed(self) -> bool:
        return abs(self.lander.v_speed) <= 40

    def landing_horizontal_speed(self) -> bool:
        return abs(self.lander.h_speed) <= 20

    def successful_landing(self) -> bool:
        """For a landing to be successful, the ship must:
            - land on flat ground
            - land in a vertical position (tilt angle = 0°)
            - vertical speed must be limited ( ≤ 40m/s in absolute value)
            - horizontal speed must be limited ( ≤ 20m/s in absolute value)
        """
        return (\
            self.landing_on_site() and\
            self.landing_angle() and\
            self.landing_vertical_speed() and\
            self.landing_horizontal_speed()
            )


    def get_score_distance(self):
        if self.landing_on_site():
            return 200
        return round(100*(1 - abs(self.landing_distance())/self.surface.distance_maximum))

    def get_score_speed(self):
        if self.landing_on_site():
            score = max(0, 100*(1 - abs(self.lander.v_speed)/200))
            score += max(0, 80*(1 - abs(self.lander.h_speed)/200))
        else:
            abs_speed = math.sqrt(self.lander.v_speed**2 + self.lander.h_speed**2)
            score = max(0, round(20*(1 - abs_speed/150))) # 150 : max speed estimated
            score = 0
        return score

    def get_score_angle(self):
        return round(60*(1 - abs(self.lander.rotate)/90))

    def get_score_max_speed(self):
        return max(0, 40*(1 - self.maximal_speed/200))

    def get_score(self):
        if self.exit_zone():
            return 0
        if self.lander.fuel <= 0:
            return 0
        score = self.get_score_distance() + self.get_score_speed() + self.get_score_max_speed()
        if self.landing_on_site():
            self.score = max(200, score)
            if 320<=self.score:
                self.score += self.get_score_angle()
        else:
            self.score = max(0, min(200, score))
        return self.score        

    def next_dynamics_parameters(self, rotate, power):
        
        h_accel = - power * math.sin(rotate*math.pi/180) 
        v_accel = power * math.cos(rotate*math.pi/180) + self.GRAVITY   

        h_speed = self.lander.h_speed + h_accel
        v_speed = self.lander.v_speed + v_accel

        x = self.lander.x + self.lander.h_speed + h_accel/2
        y = self.lander.y + self.lander.v_speed + v_accel/2

        return x, y, h_speed, v_speed

    def step(self, action : Action) -> bool:
        """        
        -rotate is the desired rotation angle for Mars lander. 
        Please note that for each turn the actual value of the angle 
        is limited to the value of the previous turn +/- 15°.
        
        - power is the desired thrust power. 
        0 = off. 4 = maximum power. 
        Please note that for each turn the value of the actuaNl power 
        is limited to the value of the previous turn +/- 1.
        """
        
        rotate = max(-90, min(
            90,
            self.lander.rotate + action.rotate
        )) 

        power = max(0, min(
            4,
            self.lander.power + action.power
        ))
        
        fuel = self.lander.fuel - power
        if fuel <= 0 :
            power = self.lander.fuel
            fuel = 0

        x, y, h_speed, v_speed = self.next_dynamics_parameters(rotate, power)

        self.point_lander_before = Point(self.lander.x, self.lander.y)
        self.point_lander_now = Point(x, y)

        collision = self.surface.collision(
            self.point_lander_before,
            self.point_lander_now
        )

        if collision and 0 < abs(rotate) <= 15:
            last_action = Action(-self.lander.rotate, action.power)
            self.step(last_action)

        self.maximal_speed = max(self.maximal_speed, abs(h_speed)*1.5, abs(v_speed))
        self.lander.update(x, y, h_speed, v_speed, fuel, rotate, power)
        
        return collision or self.exit_zone()
    

    def normalize_obs(self):
        return [
            self.lander.x/x_scale,
            self.lander.y/y_scale,
            abs(self.lander.h_speed)/500,
            abs(self.lander.v_speed)/500,
            self.lander.fuel/2000,
            (90 + self.lander.rotate)/180,
            self.lander.power/4
        ]
    
    def coarse_mapping(self, division_number):
        x0, x1 = 0, x_scale
        y0, y1 = 0, y_scale

        coarse_coding = list()

        for _ in range(division_number):
            coarse_coding.append(0)
            xm = (x0 + x1)/2
            ym = (y0 + y1)/2
            if self.lander.x > xm :
                coarse_coding[-1] += 2
                x0 = xm
            else:
                x1 = xm
            
            if self.lander.y > ym:
                coarse_coding[-1] +=1
                y0 = ym
            else:
                y1 = ym

        return coarse_coding
            
    def coarse_obs(self, division_number):
        coarse_speed = [
            [self.lander.h_speed, self.lander.v_speed],
            [-Lander.h_speed_scale/2, -Lander.v_speed_scale/2],
            [Lander.h_speed_scale/2, Lander.v_speed_scale]
        ]
        coarse_action = [
            [self.lander.rotate, self.lander.power],
            [-Lander.rotate_scale/2, 0],
            [Lander.rotate_scale/2, Lander.power_scale]
        ]
        
        def obs_division(obs_list, obs_0_list, obs_1_list, division_number):
            
            def recu(division_number):
                if division_number == 0 :
                    return []
            
                coarse_number = 0
                for i,(obs, obs_0, obs_1) in enumerate(zip(obs_list, obs_0_list, obs_1_list)):
                    obs_m = (obs_0 + obs_1)/2
                    if obs > obs_m:
                        coarse_number +=1
                        obs_0_list[i] = obs_m
                    else:
                        obs_1_list[i] = obs_m

                coarse_number >>=1
                return [coarse_number] + recu(division_number-1)
                

            return recu(division_number)
    
        return [
            obs_division(*coarse_speed, division_number),
            obs_division(*coarse_action, division_number)
        ]


        