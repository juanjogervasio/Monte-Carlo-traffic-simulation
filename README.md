# Monte Carlo simulations of a simple traffic model

The Nagel-Schreckenberg model is a probabilistic cellular automaton that replicates the traffic flow in a single-lane road. Its main implementation goes as follows:
* The road is divided into N positions and parameterized with periodic boundary conditions, so that the position next to the Nth cell is the first one in the lane.
* A number $k < N$ of cars are set in some $x_{i}$ positions, which can be occupied by only one car. Every car is assigned a velocity $V_{i} \leq V_{max}$ and is intended to move in the same direction as the others.
* The positions and velocities are updated following these rules:
  * Acceleration: $V_{i}(t+1) = V_{i}(t)+1$, unless $V_{i}(t) = V_{max}$ , in which case it remains the same.
  * Braking: if the updated velocity is greater than or equal to the distance $d_{i}(t)$ to the next car, then a collision will occur. If this is the case, the velocity is reduced back to $V_{i}(t)$.
  * Random braking: in a real scenario, a driver can stop accelerating due to a distraction, a mechanical problem, etc. To take this into account, a braking $V_{i}(t+1) \rightarrow V_{i}(t+1)-1$ is introduced with probaility $p$.
  * In the last step, the positions are updated to  $x_{i}(t+1) = x_{i}(t) + V_{i}(t+1)$

This process is repeated for a large number of iterations in order to reproduce the stationary state of the system. In this project, I made simulations varying the number of cars to obtain the corresponding fundamental diagram (traffic flow vs car density) and explore the results for different values of $V_{max}$ and $p$.

For further details, see the Jupyter notebook files [Work in progress].
