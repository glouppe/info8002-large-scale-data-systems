import argparse
import math
import pickle
import numpy as np
import time

from computers import *

# Load the pickle files
actions = pickle.load(open("actions.pickle", "rb"))
states = pickle.load(open("states.pickle", "rb"))
timestep = 0

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--correct-fraction", type=float, default=1.0, help="Fraction of correct flight computers (default 1.0).")
parser.add_argument("--flight-computers", type=int, default=3, help="Number of flight computers (default: 3).")
arguments, _ = parser.parse_known_args()


def readout_state():
    return states[timestep]


def execute_action(action):
    print(action)
    print(actions[timestep])
    for k in action.keys():
        assert(action[k] == actions[timestep][k])


def allocate_flight_computers(arguments):
    flight_computers = []
    n_fc = arguments.flight_computers
    n_correct_fc = math.ceil(arguments.correct_fraction * n_fc)
    n_incorrect_fc = n_fc - n_correct_fc
    state = readout_state()
    for _ in range(n_correct_fc):
        flight_computers.append(FlightComputer(state))
    for _ in range(n_incorrect_fc):
        flight_computers.append(allocate_random_flight_computer(state))
    # Add the peers for the consensus protocol
    for fc in flight_computers:
        for peer in flight_computers:
            if fc != peer:
                fc.add_peer(peer)

    return flight_computers

# Connect with Kerbal Space Program
flight_computers = allocate_flight_computers(arguments)


def select_leader():
    leader_index = np.random.randint(0, len(flight_computers))

    return flight_computers[leader_index]


def next_action(state):
    leader = select_leader()
    state_decided = leader.decide_on_state(state)
    if not state_decided:
        return None
    action = leader.sample_next_action()
    action_decided = leader.decide_on_action(action)
    if action_decided:
        return action

    return None

complete = False
try:
    while not complete:
        timestep += 1
        state = readout_state()
        leader = select_leader()
        state_decided = leader.decide_on_state(state)
        if not state_decided:
            continue
        action = leader.sample_next_action()
        if action is None:
            complete = True
            continue
        if leader.decide_on_action(action):
            execute_action(action)
        else:
            timestep -= 1
except Exception as e:
    print(e)

if complete:
    print("Success!")
else:
    print("Fail!")
