"""Optimization algorithms for finding minima and maxima."""

import math
import random
from typing import Callable, List, Tuple, Optional, Any

__all__ = [
    'gradient_descent',
    'gradient_descent_momentum',
    'gradient_descent_adam',
    'stochastic_gradient_descent',
    'hill_climbing',
    'simulated_annealing',
    'genetic_algorithm',
    'grid_search',
    'random_search',
    'coordinate_descent',
    'nelder_mead',
    'golden_section_search',
    'bisection_method',
    'newton_method',
    'secant_method',
    'line_search',
    'backtracking_line_search',
    'particle_swarm',
    'differential_evolution',
    'basin_hopping',
    'minimize_scalar',
    'minimize_multivariate',
    'constraint_penalty',
    'lagrange_multiplier',
]

def gradient_descent(f: Callable, grad_f: Callable, x0: List[float], 
                     learning_rate: float = 0.01, max_iter: int = 1000, 
                     tol: float = 1e-6) -> Tuple[List[float], float]:
    """Minimize function using gradient descent.
    
    Args:
        f: Objective function
        grad_f: Gradient function
        x0: Initial point
        learning_rate: Learning rate
        max_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> grad_f = lambda x: [2*x[0], 2*x[1]]
        >>> x_opt, f_opt = gradient_descent(f, grad_f, [5.0, 5.0])
        >>> abs(f_opt) < 0.01
        True
    """
    x = x0.copy()
    
    for _ in range(max_iter):
        grad = grad_f(x)
        x_new = [x[i] - learning_rate * grad[i] for i in range(len(x))]
        
        # Check convergence
        if sum((x_new[i] - x[i])**2 for i in range(len(x))) < tol**2:
            break
        
        x = x_new
    
    return x, f(x)

def gradient_descent_momentum(f: Callable, grad_f: Callable, x0: List[float],
                               learning_rate: float = 0.01, momentum: float = 0.9,
                               max_iter: int = 1000, tol: float = 1e-6) -> Tuple[List[float], float]:
    """Gradient descent with momentum.
    
    Args:
        f: Objective function
        grad_f: Gradient function
        x0: Initial point
        learning_rate: Learning rate
        momentum: Momentum factor (0 to 1)
        max_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> grad_f = lambda x: [2*x[0], 2*x[1]]
        >>> x_opt, _ = gradient_descent_momentum(f, grad_f, [5.0, 5.0])
        >>> abs(x_opt[0]) < 0.1 and abs(x_opt[1]) < 0.1
        True
    """
    x = x0.copy()
    velocity = [0.0] * len(x)
    
    for _ in range(max_iter):
        grad = grad_f(x)
        velocity = [momentum * velocity[i] - learning_rate * grad[i] for i in range(len(x))]
        x_new = [x[i] + velocity[i] for i in range(len(x))]
        
        if sum((x_new[i] - x[i])**2 for i in range(len(x))) < tol**2:
            break
        
        x = x_new
    
    return x, f(x)

def gradient_descent_adam(f: Callable, grad_f: Callable, x0: List[float],
                          learning_rate: float = 0.001, beta1: float = 0.9,
                          beta2: float = 0.999, epsilon: float = 1e-8,
                          max_iter: int = 1000, tol: float = 1e-6) -> Tuple[List[float], float]:
    """Adam optimization algorithm.
    
    Args:
        f: Objective function
        grad_f: Gradient function
        x0: Initial point
        learning_rate: Learning rate
        beta1: First moment decay
        beta2: Second moment decay
        epsilon: Small constant for numerical stability
        max_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> grad_f = lambda x: [2*x[0], 2*x[1]]
        >>> x_opt, _ = gradient_descent_adam(f, grad_f, [5.0, 5.0])
        >>> abs(x_opt[0]) < 0.1 and abs(x_opt[1]) < 0.1
        True
    """
    x = x0.copy()
    m = [0.0] * len(x)  # First moment
    v = [0.0] * len(x)  # Second moment
    
    for t in range(1, max_iter + 1):
        grad = grad_f(x)
        
        # Update biased moments
        m = [beta1 * m[i] + (1 - beta1) * grad[i] for i in range(len(x))]
        v = [beta2 * v[i] + (1 - beta2) * grad[i]**2 for i in range(len(x))]
        
        # Bias correction
        m_hat = [m[i] / (1 - beta1**t) for i in range(len(x))]
        v_hat = [v[i] / (1 - beta2**t) for i in range(len(x))]
        
        # Update parameters
        x_new = [x[i] - learning_rate * m_hat[i] / (math.sqrt(v_hat[i]) + epsilon) 
                 for i in range(len(x))]
        
        if sum((x_new[i] - x[i])**2 for i in range(len(x))) < tol**2:
            break
        
        x = x_new
    
    return x, f(x)

def stochastic_gradient_descent(f: Callable, grad_f: Callable, x0: List[float],
                                learning_rate: float = 0.01, max_iter: int = 1000) -> Tuple[List[float], float]:
    """Stochastic gradient descent (simulated with noise).
    
    Args:
        f: Objective function
        grad_f: Gradient function
        x0: Initial point
        learning_rate: Learning rate
        max_iter: Maximum iterations
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> grad_f = lambda x: [2*x[0], 2*x[1]]
        >>> x_opt, _ = stochastic_gradient_descent(f, grad_f, [5.0, 5.0])
        >>> abs(x_opt[0]) < 1.0 and abs(x_opt[1]) < 1.0
        True
    """
    x = x0.copy()
    
    for _ in range(max_iter):
        grad = grad_f(x)
        # Add noise to simulate stochastic updates
        noise = [random.gauss(0, 0.1) for _ in range(len(x))]
        x = [x[i] - learning_rate * (grad[i] + noise[i]) for i in range(len(x))]
    
    return x, f(x)

def hill_climbing(f: Callable, x0: List[float], step_size: float = 0.1,
                  max_iter: int = 1000, maximize: bool = False) -> Tuple[List[float], float]:
    """Hill climbing optimization.
    
    Args:
        f: Objective function
        x0: Initial point
        step_size: Step size for exploration
        max_iter: Maximum iterations
        maximize: If True, maximize instead of minimize
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: -(x[0]**2 + x[1]**2)
        >>> x_opt, f_opt = hill_climbing(f, [5.0, 5.0], maximize=True)
        >>> f_opt > -1.0
        True
    """
    x = x0.copy()
    f_x = f(x)
    
    for _ in range(max_iter):
        improved = False
        
        # Try all neighbors
        for i in range(len(x)):
            for delta in [step_size, -step_size]:
                x_new = x.copy()
                x_new[i] += delta
                f_new = f(x_new)
                
                if (maximize and f_new > f_x) or (not maximize and f_new < f_x):
                    x = x_new
                    f_x = f_new
                    improved = True
                    break
            
            if improved:
                break
        
        if not improved:
            break
    
    return x, f_x

def simulated_annealing(f: Callable, x0: List[float], bounds: List[Tuple[float, float]],
                        T0: float = 100.0, cooling_rate: float = 0.95,
                        max_iter: int = 1000) -> Tuple[List[float], float]:
    """Simulated annealing optimization.
    
    Args:
        f: Objective function
        x0: Initial point
        bounds: List of (min, max) for each dimension
        T0: Initial temperature
        cooling_rate: Temperature cooling rate
        max_iter: Maximum iterations
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = simulated_annealing(f, [5.0, 5.0], [(-10, 10), (-10, 10)])
        >>> f_opt < 1.0
        True
    """
    x = x0.copy()
    f_x = f(x)
    best_x = x.copy()
    best_f = f_x
    T = T0
    
    for _ in range(max_iter):
        # Generate neighbor
        x_new = []
        for i in range(len(x)):
            x_new.append(random.uniform(bounds[i][0], bounds[i][1]))
        
        f_new = f(x_new)
        delta = f_new - f_x
        
        # Accept or reject
        if delta < 0 or random.random() < math.exp(-delta / T):
            x = x_new
            f_x = f_new
            
            if f_x < best_f:
                best_x = x.copy()
                best_f = f_x
        
        T *= cooling_rate
    
    return best_x, best_f

def genetic_algorithm(f: Callable, bounds: List[Tuple[float, float]],
                      pop_size: int = 50, n_generations: int = 100,
                      mutation_rate: float = 0.1, crossover_rate: float = 0.8) -> Tuple[List[float], float]:
    """Genetic algorithm optimization.
    
    Args:
        f: Objective function (minimize)
        bounds: List of (min, max) for each dimension
        pop_size: Population size
        n_generations: Number of generations
        mutation_rate: Mutation probability
        crossover_rate: Crossover probability
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = genetic_algorithm(f, [(-10, 10), (-10, 10)], n_generations=50)
        >>> f_opt < 5.0
        True
    """
    n_dims = len(bounds)
    
    # Initialize population
    population = []
    for _ in range(pop_size):
        individual = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(n_dims)]
        population.append(individual)
    
    for _ in range(n_generations):
        # Evaluate fitness
        fitness = [f(ind) for ind in population]
        
        # Selection (tournament)
        new_population = []
        for _ in range(pop_size):
            i1, i2 = random.sample(range(pop_size), 2)
            winner = population[i1] if fitness[i1] < fitness[i2] else population[i2]
            new_population.append(winner.copy())
        
        # Crossover
        for i in range(0, pop_size - 1, 2):
            if random.random() < crossover_rate:
                point = random.randint(1, n_dims - 1)
                new_population[i][:point], new_population[i+1][:point] = \
                    new_population[i+1][:point], new_population[i][:point]
        
        # Mutation
        for individual in new_population:
            if random.random() < mutation_rate:
                idx = random.randint(0, n_dims - 1)
                individual[idx] = random.uniform(bounds[idx][0], bounds[idx][1])
        
        population = new_population
    
    # Return best
    fitness = [f(ind) for ind in population]
    best_idx = fitness.index(min(fitness))
    return population[best_idx], fitness[best_idx]

def grid_search(f: Callable, param_grid: List[List[float]]) -> Tuple[List[float], float]:
    """Grid search over parameter space.
    
    Args:
        f: Objective function
        param_grid: List of parameter values for each dimension
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: (x[0] - 2)**2 + (x[1] - 3)**2
        >>> grid = [[1, 2, 3, 4], [2, 3, 4, 5]]
        >>> x_opt, f_opt = grid_search(f, grid)
        >>> x_opt == [2, 3]
        True
    """
    def generate_combinations(grid, current=[]):
        if not grid:
            return [current]
        
        result = []
        for value in grid[0]:
            result.extend(generate_combinations(grid[1:], current + [value]))
        return result
    
    combinations = generate_combinations(param_grid)
    best_x = combinations[0]
    best_f = f(best_x)
    
    for x in combinations[1:]:
        f_x = f(x)
        if f_x < best_f:
            best_x = x
            best_f = f_x
    
    return best_x, best_f

def random_search(f: Callable, bounds: List[Tuple[float, float]],
                  n_iter: int = 100) -> Tuple[List[float], float]:
    """Random search optimization.
    
    Args:
        f: Objective function
        bounds: List of (min, max) for each dimension
        n_iter: Number of iterations
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = random_search(f, [(-10, 10), (-10, 10)], n_iter=100)
        >>> f_opt < 10.0
        True
    """
    best_x = None
    best_f = float('inf')
    
    for _ in range(n_iter):
        x = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
        f_x = f(x)
        
        if f_x < best_f:
            best_x = x
            best_f = f_x
    
    return best_x, best_f

def coordinate_descent(f: Callable, x0: List[float], step_size: float = 0.1,
                       max_iter: int = 1000, tol: float = 1e-6) -> Tuple[List[float], float]:
    """Coordinate descent optimization.
    
    Args:
        f: Objective function
        x0: Initial point
        step_size: Step size
        max_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = coordinate_descent(f, [5.0, 5.0])
        >>> f_opt < 0.1
        True
    """
    x = x0.copy()
    
    for _ in range(max_iter):
        x_old = x.copy()
        
        # Optimize each coordinate
        for i in range(len(x)):
            best_val = x[i]
            best_f = f(x)
            
            # Try steps in both directions
            for delta in [step_size, -step_size, step_size * 0.1, -step_size * 0.1]:
                x[i] = x_old[i] + delta
                f_new = f(x)
                if f_new < best_f:
                    best_val = x[i]
                    best_f = f_new
            
            x[i] = best_val
        
        # Check convergence
        if sum((x[i] - x_old[i])**2 for i in range(len(x))) < tol**2:
            break
    
    return x, f(x)

def nelder_mead(f: Callable, x0: List[float], max_iter: int = 1000,
                tol: float = 1e-6) -> Tuple[List[float], float]:
    """Nelder-Mead simplex algorithm.
    
    Args:
        f: Objective function
        x0: Initial point
        max_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = nelder_mead(f, [5.0, 5.0])
        >>> f_opt < 0.1
        True
    """
    n = len(x0)
    
    # Initialize simplex
    simplex = [x0.copy()]
    for i in range(n):
        x = x0.copy()
        x[i] += 1.0
        simplex.append(x)
    
    alpha, gamma, rho, sigma = 1.0, 2.0, 0.5, 0.5
    
    for _ in range(max_iter):
        # Order simplex by function value
        simplex.sort(key=lambda x: f(x))
        
        # Check convergence
        f_std = math.sqrt(sum((f(simplex[i]) - f(simplex[0]))**2 for i in range(n+1)) / (n+1))
        if f_std < tol:
            break
        
        # Centroid of best n points
        centroid = [sum(simplex[i][j] for i in range(n)) / n for j in range(n)]
        
        # Reflection
        x_r = [centroid[j] + alpha * (centroid[j] - simplex[-1][j]) for j in range(n)]
        f_r = f(x_r)
        
        if f(simplex[0]) <= f_r < f(simplex[-2]):
            simplex[-1] = x_r
        elif f_r < f(simplex[0]):
            # Expansion
            x_e = [centroid[j] + gamma * (x_r[j] - centroid[j]) for j in range(n)]
            simplex[-1] = x_e if f(x_e) < f_r else x_r
        else:
            # Contraction
            x_c = [centroid[j] + rho * (simplex[-1][j] - centroid[j]) for j in range(n)]
            if f(x_c) < f(simplex[-1]):
                simplex[-1] = x_c
            else:
                # Shrink
                for i in range(1, n+1):
                    simplex[i] = [simplex[0][j] + sigma * (simplex[i][j] - simplex[0][j]) 
                                 for j in range(n)]
    
    simplex.sort(key=lambda x: f(x))
    return simplex[0], f(simplex[0])

def golden_section_search(f: Callable, a: float, b: float,
                          tol: float = 1e-5) -> Tuple[float, float]:
    """Golden section search for 1D optimization.
    
    Args:
        f: Objective function (1D)
        a: Lower bound
        b: Upper bound
        tol: Convergence tolerance
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: (x - 2)**2
        >>> x_opt, f_opt = golden_section_search(f, 0, 5)
        >>> abs(x_opt - 2.0) < 0.01
        True
    """
    phi = (1 + math.sqrt(5)) / 2
    resphi = 2 - phi
    
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1 = f(x1)
    f2 = f(x2)
    
    while abs(b - a) > tol:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = f(x2)
    
    return (a + b) / 2, f((a + b) / 2)

def bisection_method(f: Callable, a: float, b: float,
                     tol: float = 1e-5) -> float:
    """Bisection method for root finding.
    
    Args:
        f: Function
        a: Lower bound
        b: Upper bound
        tol: Tolerance
        
    Returns:
        Root of function
        
    Example:
        >>> f = lambda x: x**2 - 4
        >>> root = bisection_method(f, 0, 3)
        >>> abs(root - 2.0) < 0.01
        True
    """
    if f(a) * f(b) > 0:
        raise ValueError("Function must have opposite signs at bounds")
    
    while abs(b - a) > tol:
        c = (a + b) / 2
        if f(c) == 0:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2

def newton_method(f: Callable, df: Callable, x0: float,
                  max_iter: int = 100, tol: float = 1e-6) -> float:
    """Newton's method for root finding.
    
    Args:
        f: Function
        df: Derivative of function
        x0: Initial guess
        max_iter: Maximum iterations
        tol: Tolerance
        
    Returns:
        Root of function
        
    Example:
        >>> f = lambda x: x**2 - 4
        >>> df = lambda x: 2*x
        >>> root = newton_method(f, df, 1.0)
        >>> abs(root - 2.0) < 0.01
        True
    """
    x = x0
    
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            break
        
        dfx = df(x)
        if abs(dfx) < 1e-10:
            break
        
        x = x - fx / dfx
    
    return x

def secant_method(f: Callable, x0: float, x1: float,
                  max_iter: int = 100, tol: float = 1e-6) -> float:
    """Secant method for root finding.
    
    Args:
        f: Function
        x0: First initial guess
        x1: Second initial guess
        max_iter: Maximum iterations
        tol: Tolerance
        
    Returns:
        Root of function
        
    Example:
        >>> f = lambda x: x**2 - 4
        >>> root = secant_method(f, 1.0, 3.0)
        >>> abs(root - 2.0) < 0.01
        True
    """
    for _ in range(max_iter):
        f0 = f(x0)
        f1 = f(x1)
        
        if abs(f1) < tol:
            return x1
        
        if abs(f1 - f0) < 1e-10:
            break
        
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
    
    return x1

def line_search(f: Callable, x: List[float], direction: List[float],
                alpha_max: float = 1.0) -> float:
    """Line search to find step size.
    
    Args:
        f: Objective function
        x: Current point
        direction: Search direction
        alpha_max: Maximum step size
        
    Returns:
        Optimal step size
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> alpha = line_search(f, [5.0, 5.0], [-1.0, -1.0])
        >>> 0 < alpha <= 1.0
        True
    """
    alpha = alpha_max
    c = 0.5
    
    f_0 = f(x)
    
    for _ in range(20):
        x_new = [x[i] + alpha * direction[i] for i in range(len(x))]
        if f(x_new) < f_0:
            return alpha
        alpha *= c
    
    return alpha

def backtracking_line_search(f: Callable, grad_f: Callable, x: List[float],
                             direction: List[float], alpha_init: float = 1.0,
                             rho: float = 0.5, c: float = 1e-4) -> float:
    """Backtracking line search (Armijo rule).
    
    Args:
        f: Objective function
        grad_f: Gradient function
        x: Current point
        direction: Search direction
        alpha_init: Initial step size
        rho: Reduction factor
        c: Armijo constant
        
    Returns:
        Step size satisfying Armijo condition
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> grad_f = lambda x: [2*x[0], 2*x[1]]
        >>> alpha = backtracking_line_search(f, grad_f, [5.0, 5.0], [-1.0, -1.0])
        >>> alpha > 0
        True
    """
    alpha = alpha_init
    grad = grad_f(x)
    f_x = f(x)
    
    # Directional derivative
    dir_deriv = sum(grad[i] * direction[i] for i in range(len(x)))
    
    for _ in range(50):
        x_new = [x[i] + alpha * direction[i] for i in range(len(x))]
        if f(x_new) <= f_x + c * alpha * dir_deriv:
            return alpha
        alpha *= rho
    
    return alpha

def particle_swarm(f: Callable, bounds: List[Tuple[float, float]],
                   n_particles: int = 30, max_iter: int = 100,
                   w: float = 0.7, c1: float = 1.5, c2: float = 1.5) -> Tuple[List[float], float]:
    """Particle swarm optimization.
    
    Args:
        f: Objective function
        bounds: List of (min, max) for each dimension
        n_particles: Number of particles
        max_iter: Maximum iterations
        w: Inertia weight
        c1: Cognitive parameter
        c2: Social parameter
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = particle_swarm(f, [(-10, 10), (-10, 10)], max_iter=50)
        >>> f_opt < 1.0
        True
    """
    n_dims = len(bounds)
    
    # Initialize particles
    particles = []
    velocities = []
    for _ in range(n_particles):
        pos = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(n_dims)]
        vel = [random.uniform(-1, 1) for _ in range(n_dims)]
        particles.append(pos)
        velocities.append(vel)
    
    # Initialize personal and global bests
    personal_best = particles.copy()
    personal_best_values = [f(p) for p in personal_best]
    global_best = personal_best[personal_best_values.index(min(personal_best_values))].copy()
    global_best_value = min(personal_best_values)
    
    for _ in range(max_iter):
        for i in range(n_particles):
            # Update velocity
            r1, r2 = random.random(), random.random()
            for d in range(n_dims):
                velocities[i][d] = (w * velocities[i][d] +
                                   c1 * r1 * (personal_best[i][d] - particles[i][d]) +
                                   c2 * r2 * (global_best[d] - particles[i][d]))
            
            # Update position
            for d in range(n_dims):
                particles[i][d] += velocities[i][d]
                particles[i][d] = max(bounds[d][0], min(bounds[d][1], particles[i][d]))
            
            # Update personal best
            f_val = f(particles[i])
            if f_val < personal_best_values[i]:
                personal_best[i] = particles[i].copy()
                personal_best_values[i] = f_val
                
                # Update global best
                if f_val < global_best_value:
                    global_best = particles[i].copy()
                    global_best_value = f_val
    
    return global_best, global_best_value

def differential_evolution(f: Callable, bounds: List[Tuple[float, float]],
                           pop_size: int = 50, max_iter: int = 100,
                           F: float = 0.8, CR: float = 0.9) -> Tuple[List[float], float]:
    """Differential evolution algorithm.
    
    Args:
        f: Objective function
        bounds: List of (min, max) for each dimension
        pop_size: Population size
        max_iter: Maximum iterations
        F: Differential weight
        CR: Crossover probability
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = differential_evolution(f, [(-10, 10), (-10, 10)], max_iter=50)
        >>> f_opt < 1.0
        True
    """
    n_dims = len(bounds)
    
    # Initialize population
    population = []
    for _ in range(pop_size):
        individual = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(n_dims)]
        population.append(individual)
    
    for _ in range(max_iter):
        new_population = []
        
        for i in range(pop_size):
            # Mutation
            indices = [j for j in range(pop_size) if j != i]
            a, b, c = random.sample(indices, 3)
            mutant = [population[a][d] + F * (population[b][d] - population[c][d]) 
                     for d in range(n_dims)]
            
            # Bound checking
            mutant = [max(bounds[d][0], min(bounds[d][1], mutant[d])) for d in range(n_dims)]
            
            # Crossover
            trial = []
            for d in range(n_dims):
                if random.random() < CR or d == random.randint(0, n_dims - 1):
                    trial.append(mutant[d])
                else:
                    trial.append(population[i][d])
            
            # Selection
            if f(trial) < f(population[i]):
                new_population.append(trial)
            else:
                new_population.append(population[i])
        
        population = new_population
    
    # Return best
    fitness = [f(ind) for ind in population]
    best_idx = fitness.index(min(fitness))
    return population[best_idx], fitness[best_idx]

def basin_hopping(f: Callable, x0: List[float], bounds: List[Tuple[float, float]],
                  n_iter: int = 100, step_size: float = 0.5) -> Tuple[List[float], float]:
    """Basin hopping global optimization.
    
    Args:
        f: Objective function
        x0: Initial point
        bounds: List of (min, max) for each dimension
        n_iter: Number of iterations
        step_size: Step size for perturbation
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = basin_hopping(f, [5.0, 5.0], [(-10, 10), (-10, 10)])
        >>> f_opt < 1.0
        True
    """
    x = x0.copy()
    f_x = f(x)
    best_x = x.copy()
    best_f = f_x
    
    for _ in range(n_iter):
        # Perturb
        x_new = [x[i] + random.uniform(-step_size, step_size) for i in range(len(x))]
        
        # Bound checking
        x_new = [max(bounds[i][0], min(bounds[i][1], x_new[i])) for i in range(len(x))]
        
        # Local minimization (simple hill climbing)
        for _ in range(10):
            improved = False
            for i in range(len(x_new)):
                for delta in [0.1, -0.1]:
                    x_try = x_new.copy()
                    x_try[i] += delta
                    if all(bounds[j][0] <= x_try[j] <= bounds[j][1] for j in range(len(x_try))):
                        if f(x_try) < f(x_new):
                            x_new = x_try
                            improved = True
                            break
                if improved:
                    break
            if not improved:
                break
        
        f_new = f(x_new)
        
        # Accept
        x = x_new
        f_x = f_new
        
        if f_x < best_f:
            best_x = x.copy()
            best_f = f_x
    
    return best_x, best_f

def minimize_scalar(f: Callable, bounds: Tuple[float, float],
                    method: str = 'golden') -> Tuple[float, float]:
    """Minimize scalar function.
    
    Args:
        f: Objective function (1D)
        bounds: (min, max) bounds
        method: 'golden' or 'bisection'
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: (x - 3)**2
        >>> x_opt, f_opt = minimize_scalar(f, (0, 10))
        >>> abs(x_opt - 3.0) < 0.1
        True
    """
    if method == 'golden':
        return golden_section_search(f, bounds[0], bounds[1])
    else:
        # Use grid search as fallback
        n_points = 100
        step = (bounds[1] - bounds[0]) / n_points
        best_x = bounds[0]
        best_f = f(best_x)
        
        for i in range(n_points + 1):
            x = bounds[0] + i * step
            f_x = f(x)
            if f_x < best_f:
                best_x = x
                best_f = f_x
        
        return best_x, best_f

def minimize_multivariate(f: Callable, x0: List[float],
                          method: str = 'nelder-mead') -> Tuple[List[float], float]:
    """Minimize multivariate function.
    
    Args:
        f: Objective function
        x0: Initial point
        method: 'nelder-mead', 'gradient-descent', or 'coordinate-descent'
        
    Returns:
        (optimal_point, optimal_value)
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> x_opt, f_opt = minimize_multivariate(f, [5.0, 5.0])
        >>> f_opt < 1.0
        True
    """
    if method == 'nelder-mead':
        return nelder_mead(f, x0)
    elif method == 'coordinate-descent':
        return coordinate_descent(f, x0)
    else:
        return nelder_mead(f, x0)

def constraint_penalty(f: Callable, constraints: List[Callable],
                       penalty_factor: float = 1000.0) -> Callable:
    """Create penalty function for constraints.
    
    Args:
        f: Objective function
        constraints: List of constraint functions (should be >= 0 when satisfied)
        penalty_factor: Penalty multiplier
        
    Returns:
        Penalized objective function
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> c = [lambda x: x[0] + x[1] - 1]  # x0 + x1 >= 1
        >>> f_pen = constraint_penalty(f, c)
        >>> f_pen([0.5, 0.5])
        1.25
    """
    def penalized(x):
        value = f(x)
        for constraint in constraints:
            violation = constraint(x)
            if violation < 0:
                value += penalty_factor * violation**2
        return value
    
    return penalized

def lagrange_multiplier(f: Callable, g: Callable, x0: List[float],
                        lambda0: float = 1.0) -> List[float]:
    """Simple Lagrange multiplier method (numerical approximation).
    
    Args:
        f: Objective function
        g: Equality constraint (g(x) = 0)
        x0: Initial point
        lambda0: Initial multiplier
        
    Returns:
        Optimal point
        
    Example:
        >>> f = lambda x: x[0]**2 + x[1]**2
        >>> g = lambda x: x[0] + x[1] - 2
        >>> x_opt = lagrange_multiplier(f, g, [1.0, 1.0])
        >>> len(x_opt) == 2
        True
    """
    # Create augmented Lagrangian
    def L(x, lam):
        return f(x) + lam * g(x)
    
    # Simple iterative approach
    x = x0.copy()
    lam = lambda0
    
    for _ in range(100):
        # Minimize L with respect to x
        x, _ = nelder_mead(lambda x: L(x, lam), x)
        
        # Update multiplier
        lam = lam + 0.1 * g(x)
        
        # Check if constraint is satisfied
        if abs(g(x)) < 1e-4:
            break
    
    return x
