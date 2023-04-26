# Route Optimization with Continuous Data Collection of an Uncertain Road System:

The purpose of this project is to create a package delivery algorithm that can continuously prioritize tasks, schedule tasks, and collect data about a graph with uncertain edge weights. The delivery of large single trip packages to retail or average consumers involves significant planning to schedule deliveries and maximize profit. However, this is not an easy task for a delivery company that is new to an area and has no knowledge of the road system. The team solves this problem by first creating a road map of an area assigning random traversal times between each point and guaranteeing the road system is connected. Second, the team creates a route finding algorithm that balances discovery with exploitation of available data to learn and choose more optimal delivery routes. Third, the team builds a scheduler that continuously updates the delivery plan based on priority to maximize profit. Finally, the team compares the results of their algorithm to a monte carlo route planner to determine the algorithm’s effectiveness.

## Uncertainty Algorthims Implemented: 

1. Pure Randomness
   - Our Monte Carlo utilizes particle swarm optimization to run a 100 simulations to predict the best route to the delivery, after the simulations are ran the best path is utilized as the actual delivery route
  
2. Explore and Exploit 
   - Our U.S.G.S. utilizes an Epsilon Greedy algorithm to allow the delievery to have a random chance of taking a suboptimal path to furhter explore the enviroment
  
3. Sorting and Ordering 
   - Our U.S.G.S. utilizes a prioritization algorithm 
  
4. Scheduling 
   - Our U.S.G.S. utilizes a predictive priority algorithm

## Uncertainty Algorthims attempted: 
We were unable to fully implement the Ant Colony algorithm with our visual interface given the time constraint, however we did get these algorithms working but are unable to visualize them: 

1. Bayes Rule
   - Our Ant Colony utilizes a modified Baysian update to select which pheremone values to follow

2. Scheduling 
   - Our Ant Colony algorithm utilizes a predictive priority algorithm

## Running the Monte Carlo Simulation:


## Running the Updating Semi-Greedy Scheduler Simulation:


## Running the Ant Colony Simulation:


## Results:

### Monte Carlo Simulation:
!(./Figures/GreedyVsMonteCarlo.png)

### Updating Semi-Greedy Scheduler:
!(./Figures/USGS.gif)

### Ant Colony Simulation: