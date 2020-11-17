#!/usr/bin/env python
# coding=utf-8
import numpy as np

"""
1: Procedure Policy_Iteration(S,A,P,R)
2:           Inputs
3:                     S is the set of all states
4:                     A is the set of all actions
5:                     P is state transition function specifying P(s'|s,a)
6:                     R is a reward function R(s,a,s')
7:           Output
8:                     optimal policy π
9:           Local
10:                     action array π[S]
11:                     Boolean variable noChange
12:                     real array V[S]
13:           set π arbitrarily
14:           repeat
15:                     noChange ←true
16:                     Solve V[s] = ∑s'∈S P(s'|s,π[s])(R(s,a,s')+γV[s'])
17:                     for each s∈S do
18:                               Let QBest=V[s]
19:                               for each a ∈A do
20:                                         Let Qsa=∑s'∈S P(s'|s,a)(R(s,a,s')+γV[s'])
21:                                         if (Qsa > QBest) then
22:                                                   π[s]←a
23:                                                   QBest ←Qsa
24:                                                   noChange ←false
25:           until noChange
26:           return π
"""
# Note: Assuming only actions and state-state probs in the file

def parse_initialization(file):
    gamma, n_states, n_actions = -1, 0, 0
    for line in file:
        if line.startswith("discount"):
            gamma = float(line.split("discount:")[1])
        elif line.startswith("states"):
            n_states = int(line.split("states:")[1])
        elif line.startswith("actions"):
            n_actions = int(line.split("actions:")[1])
        # Break in the next linebreak
        elif line.startswith("\n"):
            break
        else:
            print("[-]: Please define discount factor, #states and #actions first. Exiting..")
            exit()

    if gamma < 0 or not n_states or not n_actions:
        print("[-]: Discount factor, #states or #actions was not specified. Exiting..")
        exit()

    assert gamma >= 0
    assert n_states
    assert n_actions
    return gamma, n_states, n_actions, file

def parse_policy(file):
    try:
        for line in file:
            policy = list(map(int, line.split(" ")))
    except:
        print("[-]: Error reading policy. It must be input as int values: %d %d %d ...")
        exit()

    assert policy
    return policy

def parse_P_R(s_num, mat, file):
    for a_count, line in enumerate(file):
        if line.startswith("\n"):
            break
        mat[a_count, s_num] = list(map(float, line.split(" ")))

# NOTE: States must be specified by number
def parse_POMDP_solve_file(filepath):
    file = open(filepath, "r")

    gamma, n_states, n_actions, file = parse_initialization(file)

    P = np.zeros((n_states, n_actions, n_states))  # transition probability
    R = np.zeros((n_states, n_actions, n_states))

    for line in file:
        if line.startswith("T:"):
            state_num = int(line.split(":")[1])
            parse_P_R(state_num, P, file)
        elif line.startswith("R:"):
            state_num = int(line.split(":")[1])
            parse_P_R(state_num, R, file)
        elif line.startswith("P:"):
            policy = parse_policy(file)

    return P, R, policy, gamma

POMDP_filepath = "multiple_user_data/POMDP-solve-format-example"
P, R, policy, gamma = parse_POMDP_solve_file(POMDP_filepath)

n_states = R.shape[0]
n_actions = R.shape[1]
states = list(range(n_states))
actions = list(range(n_actions))

# initialize value arbitrarily
V = np.zeros(n_states)

print("Initial policy", policy)

is_value_changed = True
iterations = 0
while is_value_changed:
    is_value_changed = False
    iterations += 1
    # run value iteration for each state
    for s in range(n_states):
        V[s] = sum([P[s,policy[s],s1] * (R[s,policy[s],s1] + gamma*V[s1]) for s1 in range(n_states)])
        # print "Run for state", s

    for s in range(n_states):
        q_best = V[s]
        # print "State", s, "q_best", q_best
        for a in range(n_actions):
            q_sa = sum([P[s, a, s1] * (R[s, a, s1] + gamma * V[s1]) for s1 in range(n_states)])
            if q_sa > q_best:
                print("State", s, ": q_sa", q_sa, "q_best", q_best)
                policy[s] = a
                q_best = q_sa
                is_value_changed = True

    print("Iterations:", iterations)
    # print "Policy now", policy

print("Final policy")
print(policy)
print(V)