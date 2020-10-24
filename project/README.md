In this project you will have to implement a consensus algorithm to ensure the
redundancy of several flight computers responsible for controlling a rocket.
The flight computers will guide the vehicle to a circular
orbit at approximately 100km. While redundancy is an important aspect
to ensure the safety of the vehicle, it should be noted that not reaching
consensus in a timely manner has profound effects on the vehicles behavior in flight:
no control inputs are executed. Several important design considerations
should therefore be made to ensure the timely progression of the state machine.

## Setup

### Preparing the development environment

> **Recommended**. **This installs a Python 3 environment by default.**

```console
you@host:~ $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
you@host:~ $ sh Miniconda3-latest-Linux-x86_64.sh
```
Afterwards, create the environment from the `environment.yml` file:
```console
you@host:~ $ conda env create -f environment.yml
```
The Python environment can afterwards by activated:
```console
you@host:~ $ conda activate fbw
```
The framework is installed by executing:
```console
you@host:~ $ pip install -e .
```

### Running the program

#### Without Kerbal Space Program

We provide 2 pickle files in the `data` folder to test your implementation without requiring the use of Kerbal Space Program.
The idea is simple, for every given state, the rocket executes a corresponding control action with respect to the state machine of the flight computer.
If the action does not match as expected for a correct execution (given by `actions.pickle`),
then your consensus algorithm probably did not progress using the correct value.
This could be intentional though, depending on your choice of `--correct-fraction`.

```console
you@host:~ $ python starter-code/without-ksp.py --flight-computers 10 --correct-fraction 1.0
```

#### With Kerbal Space Program

> **Note**. **Do not forget to activate your Python environment!.**

The `.craft` file of the rocket architecture can be found in the `craft` folder.
Follow the steps described in [kRPC: Getting Started](https://krpc.github.io/krpc/getting-started.html) to install and configure the `kRPC` plugin.

After preparing the rocket on the KSP launchpad, test your code by running

```console
you@host:~ $ python starter-code/with-ksp.py --flight-computers 10 --correct-fraction 1.0
```

If you do not have Kerbal Space Program, but would like to test your code in simulation, feel free to drop me an e-mail at [joeri.hermans@doct.uliege.be](mailto:joeri.hermans@doct.uliege.be),
or simply if you would like to have feedback on your implementation of report.

## Deliverables

All deliverables have to be submitted on the Montefiore submission website. We permit groups of max 4 students. We expect the following deliverables:

1. An `implementation` with the necessary description to execute your project.
2. A report describing all aspects of your architecture (max 4 pages) and assumptions with respect to the problem which needs to be solved. A discussion on the convergence rate of your consensus algorithm with respect to the ``--correct-fraction`` should be included.
3. An `environment.yml` file containing your Python dependencies.

## Guidelines

The initial codebase in the `starter-code` folder could serve as an initial foundation.
The main execution scripts will also have to be changed. For instance, how you will select the leader tasked to propose a state and action in the current consensus epoch?
Other options are possible as well.
The `computers.py` file contains
the definition of the flight computers. These *can* be adjusted. However, the interface of the constructor and the
following methods (`sample_next_action`, `decide_on_state`, `decide_on_action`) should be respected.
Their actual definitions will most likely have to be altered though. Other methods and classes can be added.

In it's current form there is no networking code. We recommend to split up the flight computers in
several independent processes (this makes it easier to deal with timeouts etc). Interprocess-communication
can be handled in various ways, although a programming a REST API through, for instance, `flask`
is fairly natural to solve the consensus problem and the failure detection. Alternatives include `grpc`
or regular network programming through sockets. All options are allowed.

We recommend the following steps to complete this project successfully.

### Step 1. Basic (abstract) consensus mechanism and system setup

Implement the interaction of the rocket sensors (`readout_state`) will
interact with a `proposer` (flight computer) to propose a new state and action to the remaining flight computers.
The chosen proposer will subsequently have to call the `decide_on_state` and `decide_on_action` method (you can alter the code to combine them)
and initiate your consensus algorithm.

At this point of the project it is probably a good idea to implement a basic synchronous consensus algorithm with
corresponding failure detectors (which should be handled). What about slow (correct) flight computers? How do they fit in your architecture and your assumptions?

You can assume that a fixed number of flight computers (although they might have different control logic) start at the same time.
Note that the flight computers provide the functions `acceptable_state` and `acceptable_action`, which can be used to verify whether a proposal
is acceptable to the acceptor, i.e., is this proposed action consistent with the state machine of the flight computer?

### Step 2. Leader election

After you've setup your consensus abstraction, you can use the consensus module to solve leader-election.
We do not impose any restrictions on how the leader is chosen.
You should however motivate your implementation. The properties of consensus, i.e., agreement, validity and termination should be satisfied
and discussed in your report.
The rocket can subsequently use the assigned leader, or some other mechanism,
to propose a state and action to the flight computers.
An important consideration here is to handle the leader re-election whenever the leader fails.

## Reading material

 [In Search of an Understandable Consensus Algorithm](https://web.stanford.edu/~ouster/cgi-bin/papers/raft-atc14)
