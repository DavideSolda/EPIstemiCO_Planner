import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.join(current_dir, "..", "..", "model"))
from shortcuts import *

sys.path.insert(1, os.path.join(current_dir, "..", "..", "engines", 'answer_set_planning'))
import asp_engine

sys.path.insert(1, os.path.join(current_dir, "..", "..", "engines", 'epicla_planning'))
import epicla_engine

import time
from mae_blocks_world import *

if __name__ == '__main__':


    #alpha
    alpha = [B(["alice"], (on_table("red")))]

    #beta
    beta = [B(["alice"], owner("alice", "red"))]

    #gamma
    #gamma = [B(["alice"], owner("alice", "red")), B(["alice"], on_table("orange"))]

    #delta
    #delta = [B(["alice, bob"], owner("alice", "red")), B(["alice, bob"], owner("alice", "orange"))]

    #one color
    color = EnumType("color", ["red"])

    #classical
    initially = [on_stack('red', 1), free_stack(2), free_stack(3),
                 free_stack(4), free_stack(5), free_stack(6),
                 top('red'),
                 free_gripper('bob'), free_gripper('alice'),
                 owner('bob', 'red'),
                 in_front_of('bob', 1), in_front_of('bob', 2), in_front_of('bob', 3),
                 in_front_of('alice', 4), in_front_of('alice', 5), in_front_of('alice', 6),
                 free_table()]

    #epistemic
    epistemic_initially = [owner('bob', 'red'), free_table(), B(["bob", "alice"], free_table())]

    one_color_time = []
    for goal in [alpha, beta]:
        t = time.time()
        run(color, initially, epistemic_initially, goal)
        one_color_time.append(time.time()-t)

    print(one_color_time)
    quit()
    #two colors


    #three colors
    color = EnumType("color", ["red", "orange", "yellow"])

    initially = [on_stack('red', 1), on_stack('orange', 2), free_stack(3),
                 free_stack(4), free_stack(5), free_stack(6),
                 on_block('black', 'red'),
                 top('black'), top('orange'),
                 free_gripper('bob'), free_gripper('alice'),
                 owner('bob', 'red'), owner('bob', 'black'), owner('bob', 'orange'),
                 in_front_of('bob', 1), in_front_of('bob', 2), in_front_of('alice', 3),
                 free_table()]

    #four colors
    color = EnumType("color", ["red", "orange", "yellow", "black"])

    initially = [on_stack('red', 1), on_stack('orange', 2), free_stack(3),
                 free_stack(4), free_stack(5), free_stack(6),
                 on_stack('red', 1), on_stack('orange', 2), free_stack(3),
                 on_block('black', 'red'),
                 top('black'), top('orange'),
                 free_gripper('bob'), free_gripper('alice'),
                 owner('bob', 'red'), owner('bob', 'black'), owner('bob', 'orange'),
                 in_front_of('bob', 1), in_front_of('bob', 2), in_front_of('alice', 3),
                 free_table()]
    
    four_color_time = []

    for goal in goals:
        t = time.time()
        run(color, initially, goal)
        four_color_time.append(time.time()-t)
