# Implementation of the El Farol Problem described in "Complexity and the economy"
# by Brian Arthur.
# This is my first python program, thus inconsistencies and slowness are expected

import random
import numpy as np
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt
from dataclasses import dataclass, field

# Number of agents
n_agents = 100
# Number of strategies that each agent holds
n_strats = 7
# Total number of weeks to simulate
total_weeks = 200
# How many weeks have passed so far
passed = 0
# Array with attendance
attendance = np.zeros(total_weeks, dtype=int)

# List with strategies
names = ["mean", "week", "mirr_mean_fifty", "mirr_sixty",
         "mirr_fifty", "median", "mirr_mean_sixty"]


# Set a random attendance on the first day to start
def first_day():
    attendance[0] = random.randint(0, n_agents)
    global passed
    passed += 1


# Return the mean of past n weeks attendance
def mean(n):
    if n >= passed:
        return np.mean(attendance[0:passed])
    else:
        return np.mean(attendance[passed - n:passed])


# Returns the attendance of n weeks past
def week(n):
    if n >= passed:
        return attendance[0]
    else:
        return attendance[passed - n]


# Returns the mean of past n weeks attendance mirrored around 50
def mirr_mean_fifty(n):
    if n >= passed:
        return abs(50 - np.mean(attendance[0:passed]))
    else:
        return abs(50 - np.mean(attendance[passed - n:passed]))


# Returns the mean of past n weeks attendance mirrored around 60
def mirr_mean_sixty(n):
    if n >= passed:
        return abs(60 - np.mean(attendance[0:passed]))
    else:
        return abs(60 - np.mean(attendance[passed - n:passed]))


# Returns the past n week attendance mirrored around 50
def mirr_fifty(n):
    if n >= passed:
        return abs(50 - attendance[0])
    else:
        return abs(50 - attendance[passed - n])


# Returns the past n week attendance mirrored around 60
def mirr_sixty(n):
    if n >= passed:
        return abs(60 - attendance[0])
    else:
        return abs(60 - attendance[passed - n])


# Returns the median
def median(n):
    if n >= passed:
        return int(np.median(attendance[0:passed]))
    else:
        return int(np.median(attendance[passed - n:passed]))


# Class of strategies
@dataclass(order=True)
class Strategy:
    # Strategy function name
    _function: chr
    # Strategy number used in the computation
    _n: int
    # Value assumed by strategy on the particular week
    value: int = 0
    # Number of successes of strategy
    success: int = 0


# Class of agents
@dataclass(order=True)
class Agent:
    # Unique ID
    _id: int
    # List of agents' strategies
    strat_list: list[int] = field(default_factory=list)


# Function to generate a complete list of strategies
def strat_generator(total):
    list_strats = []
    for name in range(len(names)):
        for j in range(int(total / len(names)) + 1):
            list_strats.append(Strategy(_function=names[name], _n=j + 1))
    return list_strats


# Generates list with all agents, each one with a random set of strats
def agent_generator(agents, number_strats, list_strategies):
    agent_list = []
    for agent in range(agents):
        agent_list.append(Agent(agent, strat_list=random.choices(list_strategies, k=number_strats)))
    return agent_list


# Function to compute the current prediction of each strat
def strat_pred(list_strats):
    # For each strategy, computes its value
    for strat in range(len(list_strats)):
        func = list_strats[strat]._function
        number = list_strats[strat]._n
        list_strats[strat].value = globals()[func](number)


# Simulates the week's attendance
def sim_el_farol(list_agents, current, strats):
    strat_pred(strats)
    # Calculates attendance
    for agent in list_agents:
        agent.strat_list.sort(key=lambda ag: ag.success, reverse=True)
        if agent.strat_list[0].value < 60:
            attendance[current] += 1
    # Add successes to correct predictions
    for strat in range(len(strats)):
        if strats[strat].value >= 60 and attendance[current] >= 60:
            strats[strat].success += 1
        elif strats[strat].value < 60 and attendance[current] < 60:
            strats[strat].success += 1
    # Updates number of passed weeks
    global passed
    passed += 1


def main():
    # Reset values of global variables
    global passed
    passed = 0
    global attendance
    attendance = np.zeros(total_weeks, dtype=int)
    first_day()
    strategies = strat_generator(len(names) * 9)
    list_agents = agent_generator(n_agents, n_strats, strategies)
    for i in range(total_weeks - 1):
        sim_el_farol(list_agents, passed, strategies)


def on_click(event):
    print(attendance)
    if event.button is MouseButton.LEFT:
        main()
        ax = plt.gca()
        x = np.arange(0, total_weeks, 1)
        plt.cla()
        ax.plot(x, list(attendance))
        plt.draw()


if __name__ == '__main__':
    main()
    # Plot and wait for mouse click
    x = np.arange(0, total_weeks, 1)
    fig, ax = plt.subplots()
    ax.plot(x, list(attendance))
    # If the left mouse button is clicked update the graph with a new simulation
    cid = fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()
