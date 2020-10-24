import argparse
import krpc
import math
import pickle
import numpy as np
import time

from computers import *


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--correct-fraction", type=float, default=1.0, help="Fraction of correct flight computers (default 1.0).")
parser.add_argument("--flight-computers", type=int, default=3, help="Number of flight computers (default: 3).")
arguments, _ = parser.parse_known_args()


connection = krpc.connect(name="INFO8002")
vessel = connection.space_center.active_vessel
vessel.control.sas = True
vessel.control.rcs = True
vessel.auto_pilot.engage()


# Setup the data streams
stream_altitude = connection.add_stream(getattr, vessel.flight(), "mean_altitude")
stream_apoapsis = connection.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
stream_periapsis = connection.add_stream(getattr, vessel.orbit, "periapsis_altitude")
stream = vessel.resources_in_decouple_stage(stage=3, cumulative=False)
stream_srb_fuel = connection.add_stream(stream.amount, "SolidFuel")
stream = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
stream_s1_fuel = connection.add_stream(stream.amount, "LiquidFuel")
stream = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
stream_s2_fuel = connection.add_stream(stream.amount, "LiquidFuel")


def readout_state():
    state = {
        "altitude": float(stream_altitude()),
        "apoapsis": float(stream_apoapsis()),
        "periapsis": float(stream_periapsis()),
        "throttle": vessel.control.throttle,
        "fuel_srb": stream_srb_fuel(),
        "fuel_s1": stream_s1_fuel(),
        "fuel_s2": stream_s2_fuel()}

    return state


def execute_action(action):
    if "throttle" in action:
        vessel.control.throttle = action["throttle"]
    if "pitch" in action and "heading" in action:
        vessel.auto_pilot.target_pitch_and_heading(action["pitch"], action["heading"])
    if "stage" in action and action["stage"]:
        vessel.control.activate_next_stage()


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
    if action is None:
        raise ValueError
    action_decided = leader.decide_on_action(action)
    if action_decided:
        return action

    return None


# Initial configuration of the rocket
action = {"heading": 90, "pitch": 90, "throttle": 0.0, "next_stage": False}
execute_action(action)

# Countdown and lift-off.
for i in range(3, 0, -1):
    time.sleep(1)
    print("Launch in ", i, "...")
print("Lift-off!")

action = {"stage": True}
vessel.control.sas = True
vessel.control.rcs = True
execute_action(action)

states = []
actions = []

complete = False
while not complete:
    state = readout_state()
    leader = select_leader()
    state_decided = leader.decide_on_state(state)
    if not state_decided:
        continue
    states.append(state)
    action = leader.sample_next_action()
    if action is None:
        complete = True
    if action is not None and leader.decide_on_action(action):
        actions.append(action)
        execute_action(action)
    else:
        actions.append(None)

# Save the trajectory
pickle.dump(actions, open("actions.pickle", "wb"))
pickle.dump(states, open("states.pickle", "wb"))
