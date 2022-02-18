# Q-learning algorithm

An agent searches for the shortest path in a maze using Q-learning algorithm

Q-learning is a type of algorithm in which a certain agent moves in given environment (performs available actions). As a result, agent changes a state (a state can be for example a square on a board). For performing specific acion in specific state, agent is given an adequate reward. Agent's ultimate goal is to maximize received reward.

## Implementation

- **environment.py** - in this module class Environment is implemented. Environment generates a maze in which agent is moving and also provides feedback about actions performed by agent
- **main.py** - in this module function qlearn() is implemented. Function qlearn() is the principal part of the project. The function saves detailed info about algorithm performance in a json file. The module also contains an example execution of the algorithm.
- **testing.py** - module contains a scheme to perform automatic testing in respect to given parameters.
- **plotter.py** - module is responsible for creating a plots using matplotlib library. To create a plot a json file with data has to be provided.

## Repository also contains:

- **pictures** - folder contains plots generated while doing a study about the implementation
- **WSI_lab6_sprawozdanie** - document (only in Polish) contains more detailed description of project and report about examination how quality of algorithm performance with respect to different parameters. 

