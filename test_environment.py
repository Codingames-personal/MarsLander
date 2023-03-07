# TEST UNITAIRE MARS LANDER
##
#%%
from main import *
import os
import sys

dir_test_name = "tests"
dir_test_path = os.path.join(os.path.abspath(os.getcwd()),dir_test_name)



chromosome_null = Chromosome([Action(0,0)]*200)##

def test_environment(environment, test_file, number_step : int = 1000) -> bool:
    data_extractor = lambda line : [list(map(int, data.split(";"))) for data in line.split("\t")]
    
    
    for step,(action_data, true_sate) in zip(
        range(number_step),
        map(data_extractor, test_file.readlines())
        ):
        
        print(f"Step number : {step}")
        print(f"Action read : {action_data}")
        print(f"Current state : {true_sate}")
        action_played = Action(*action_data)
        done = environment.step(action_played)
        print(f"Current test environment : {environment}")
        print(f"Is it done : {done}")
        
        if not environment == true_sate: 
            return False
        if done:
            return True


test_input = [
    [[0, 1500],[1000, 2000], [2000, 500], [3500, 500], [5000, 1500], [6999, 1000]],
    [5000, 2500, -50, 0, 1000, 90, 0]
]
def unitary_test():
    flat_lands = [0, 0], [6999, 0]
    
    ## GO DOWN
    number_step = 20
    initial_state = [2000, 2000, 0, 0, 1000, 0, 0]
    test_env = EnvMarsLander(flat_lands, initial_state)
    true_env = EnvMarsLander(flat_lands, initial_state)
    test_env.reset()
    test_file_path = os.path.join(dir_test_path,"test_fall.test")

    print("Test go up : begin")
    with open(test_file_path, 'r') as test_file:
        if test_environment(test_env, test_file):
            print("Success")
        else:
            print("Failed")
    print("Test go up : end")


def main():
    
    for index, test_file_path in enumerate(os.listdir(dir_test_path)):
        print(f"\t Test {index} :", end = '')
        lands = test_file.readline().split(";")
        initial_state = test_file.readline().split(";")
        environment = EnvMarsLander(lands, initial_state)
        with open(test_file_path, 'r') as test_file:
            if test_environment(environment, test_file):
                print(f"success")
            else:
                print(f"failed")



# %%
