import os
import sys

from ECHO import *

stack = IntType("stack", 1, 3)
color = EnumType("color", ["red", "orange", "yellow", "black"])
agent = AgentType(['alice', 'bob'])

color_pair = StructType("colorxcolor", [color, color])
color_stack = StructType("colorxstack", [color, stack])
agent_color = StructType("agentxcolor", [agent, color])
agent_stack = StructType("agentxstack", [agent, stack])

on_block     = Fluent("on_block", color_pair)
on_stack     = Fluent("on_stack", color_stack)
top          = Fluent("top_block", color)
gripped      = Fluent("gripped", agent_color)
free_gripper = Fluent("free_gripper", agent)
free_stack   = Fluent("free_stack", stack)
owner        = Fluent("owner", agent_color)
free_table   = Fluent("free_table")
on_table     = Fluent("table", color)
in_front_of  = Fluent("in_front_of", agent_stack)

C1 = Variable("C1", color)
C2 = Variable("C2", color)
S  = Variable("S", stack)
A1 = Variable("a1", agent)
A2 = Variable("a2", agent)
R  = Variable("R", agent)

pick = IAction(name = "pick",
               params = [R, C1, C2],
               precondition = [top(C1), on_block(C1, C2), free_gripper(R), owner(R, C1)],
               effects = [-top(C1), -on_block(C1, C2), top(C2), -free_gripper(R), gripped(R, C1)])


pick_from_ground = IAction(name = "pick_from_ground",
                           params = [R, C1, S],
                           precondition = [in_front_of(R, S), top(C1), on_stack(C1, S), free_gripper(R), owner(R, C1)],
                           effects = [free_stack(S), -top(C1), -on_stack(C1, S), -free_gripper(R), gripped(R, C1)])

pick_from_table = IAction(name = "pick_from_table",
                          params = [R, C1],
                          precondition = [on_table(C1), -free_table(), free_gripper(R)],
                          effects = [-on_table(C1), free_table(), -free_gripper(R), gripped(R, C1), owner(R, C1)])

place = IAction(name = "place",
                params = [R, C1, C2],
                precondition = [top(C2), -free_gripper(R), gripped(R, C1), owner(R, C1), owner(R, C2)],
                effects = [top(C1), on_block(C1, C2), -top(C2), free_gripper(R), -gripped(R, C1)])

place_on_ground = IAction(name = "place_on_ground",
                params = [R, C1, S],
                precondition = [free_stack(S), -free_gripper(R), gripped(R, C1), owner(R, C1), in_front_of(R, S)],
                effects = [-free_stack(S), top(C1), free_gripper(R), -gripped(R, C1)])

place_on_table = IAction(name = "place_on_table",
                         params = [R, C1],
                         precondition = [free_table(), -free_gripper(R), gripped(R, C1), owner(R, C1)],
                         effects = [-free_table(), -owner(R, C1), on_table(C1), free_gripper(R), -gripped(R, C1)])

p = ClassicalPlanningProblem()
#add types:
p.add_type(agent)
p.add_type(stack)
p.add_type(color)
p.add_type(color_pair)
p.add_type(color_stack)
p.add_type(agent_color)
p.add_type(agent_stack)
#add fluents:
p.add_fluent(on_block)
p.add_fluent(on_stack)
p.add_fluent(top)
p.add_fluent(gripped)
p.add_fluent(free_gripper)
p.add_fluent(free_stack)
p.add_fluent(owner)
p.add_fluent(free_table)
p.add_fluent(on_table)
p.add_fluent(in_front_of)
#add variables:
p.add_variable(C1)
p.add_variable(C2)
p.add_variable(S)
p.add_variable(R)
#add action:
p.add_action(pick)
p.add_action(pick_from_ground)

p.add_action(place)
p.add_action(place_on_ground)

p.add_action(pick_from_table)
p.add_action(place_on_table)
#add initial values:

p.add_initial_values(on_stack('red', 1))
p.add_initial_values(on_block('black', 'red'))
p.add_initial_values(top('black'))
p.add_initial_values(on_stack('orange', 2))
p.add_initial_values(top('orange'))
p.add_initial_values(free_gripper('bob'))
p.add_initial_values(free_gripper('alice'))
p.add_initial_values(free_stack(3))
p.add_initial_values(owner('bob', 'red'))
p.add_initial_values(owner('bob', 'black'))
p.add_initial_values(owner('bob', 'orange'))
p.add_initial_values(in_front_of('bob', 1))
p.add_initial_values(in_front_of('bob', 2))
p.add_initial_values(in_front_of('alice', 3))
p.add_initial_values(free_table())


pick_from_stack_place_on_table = MEAction('pspt',
                                          params = [A1, C1],
                                          precondition = [owner(A1, C1), free_table(), B([A1], free_table())],
                                          effects=[-owner(A1, C1), on_table(C1), -free_table()],
                                          full_obs=[A1])

pick_from_table_place_on_stack = MEAction('ptps',
                                          params = [A1, C1],
                                          precondition = [-owner(A1, C1), -free_table(),# -B([A1], free_table()),
                                                          on_table(C1)],
                                          effects=[owner(A1, C1), -on_table(C1), free_table()],
                                          full_obs=[A1])

e = MEPlanningProblem()
#add types:
e.add_type(agent)
e.add_type(color)
e.add_type(agent_color)
#add fluents:
e.add_fluent(owner)
e.add_fluent(free_table)
e.add_fluent(on_table)
#add variables:
e.add_variable(C1)
e.add_variable(A1)
e.add_variable(A2)
#add action:
e.add_action(pick_from_stack_place_on_table)
e.add_action(pick_from_table_place_on_stack)
#add initial values:
e.add_initial_values(owner('bob', 'red'))
e.add_initial_values(owner('bob', 'orange'))
e.add_initial_values(owner('bob', 'black'))
e.add_initial_values(free_table())
e.add_initial_values(B(['bob', 'alice'], owner('bob', 'red')))
e.add_initial_values(B(['bob', 'alice'], owner('bob', 'orange')))
e.add_initial_values(B(['bob', 'alice'], owner('bob', 'black')))
e.add_initial_values(B(['bob', 'alice'], free_table()))
#add goals:
e.add_goals(free_table(), owner('alice', 'black'))


echo_problem = ECHOPlanningProblem(p, e)


echo_plan = solve_echo(echo_problem)
for action in echo_plan:
    print(action)
    for sub_action in action[1]:
        print("\t\t" + str(sub_action))
