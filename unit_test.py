##
#%%

import unittest
from main import *
import os
import sys

dir_test_name = "tests"
dir_test_path = os.path.join(os.path.abspath(os.getcwd()),dir_test_name)



class TestEnvironment(unittest.TestCase):
    pass

    
class TestDynamic(TestEnvironment):
    flat_lands = [[0, 0], [6999, 0]]
    initial_state = [2500, 2500, 0, 0, 500, 0, 0]

    def setUp(self) -> None:
        self.test_env = EnvMarsLander(
            TestDynamic.flat_lands,
            TestDynamic.initial_state
        )
        self.test_env.reset()

    def test_fall(self):

        action_null = Action(0, 0)
        true_lander = Lander()
        test_file_path = os.path.join(dir_test_path,"test_fall.test")
        with open(test_file_path, 'r') as test_file:
            for line in test_file.readlines():
                state = list(map(
                    int,
                    line.split(";")
                ))

                true_lander.update(*state)
                
                self.assertEqual(
                    self.test_env.lander,
                    true_lander
                    )
                self.test_env.step(action_null)


    def test_up(self):

        action_null = Action(0, 1)
        true_lander = Lander()
        test_file_path = os.path.join(dir_test_path, "test_up.test")
        with open(test_file_path, 'r') as test_file:
            for line in test_file.readlines():
                state = list(map(
                    int,
                    line.split(";")
                ))

                true_lander.update(*state)
 
                self.assertEqual(
                    self.test_env.lander,
                    true_lander
                    )
                    
                self.test_env.step(action_null)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# %%
