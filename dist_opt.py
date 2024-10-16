import cvxpy as cp
import numpy as np


def get_optimized_acceleration(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, x_pos, parameters):
    #Constants
    t = parameters[0]                           #time scale: t is the measurement frequency, it can be 1 second for now.
    epsilon_prime = parameters[1] * 1000 / 3600 #km/h to m/s conversion for desired velocity
    alfa = parameters[2]                        #m/sec2 
    alfa_prime = parameters[3]                  #m/sec2 
    gamma = parameters[4]                       #Gamma is Speed-Location Conversion Factor
    R = parameters[5]                           #CAV's reaction (s)
    D = parameters[6]                           #Safety Distance (m)
    lv = parameters[7]                          #Length of vehicle (m)
    F = 495

    #Inputs
    v0 = np.array(v_input).reshape((number_of_lane, number_of_vehicle))
    x0 = np.array(x_input).reshape((number_of_lane, number_of_vehicle))
    xr = np.array(xr_cons).reshape((number_of_lane, number_of_vehicle))
    x_p = np.array(x_pos).reshape((number_of_lane, number_of_vehicle))

    #decision variables
    v = cp.Variable((number_of_lane, number_of_vehicle), nonneg=True)
    x = cp.Variable((number_of_lane, number_of_vehicle), nonneg=True)
    a = cp.Variable((number_of_lane, number_of_vehicle))
    w = cp.Variable((number_of_lane, number_of_vehicle), nonneg=True)
    z = cp.Variable((number_of_lane, number_of_vehicle), nonneg=True)

    #constraints
    constraints = []

    # Abs constraints
    #TO DO: check abs before using constraint
    constraints += [w[i, j] >= v[i, j] - v0[i, j] for i in range(number_of_lane) for j in range(number_of_vehicle)]
    constraints += [w[i, j] >= -(v[i, j] - v0[i, j]) for i in range(number_of_lane) for j in range(number_of_vehicle)]

    # x constraints
    constraints += [x[i, j] == 0.5 * a[i, j] * t**2 + v0[i, j] * t + x0[i, j] for i in range(number_of_lane) for j in range(number_of_vehicle) if xr[i, j] != 0]

    # v constraints
    constraints += [v[i, j] == a[i, j] * t + v0[i, j] for i in range(number_of_lane) for j in range(number_of_vehicle) if xr[i, j] != 0]

    # Safe distance constraints
    if number_of_vehicle > 2:
        for i in range(number_of_lane):
            for j in range(number_of_vehicle - 1):
                if xr[i, j] != 0 and xr[i, j + 1] != 0:
                    constraints += [x[i, j] - x[i, j + 1] >= lv + D + R * v[i, j + 1]]

    # Lane crossing constraints
    for lane in range(2, 5):
        for i in range(number_of_lane):
            for j in range(number_of_vehicle):
                if xr[i, j] != 0 and xr[lane - 2, j] != 0 and i < lane - 2:
                    if x_p[i, j] >= F - epsilon_prime and x_p[lane - 2, j] >= F - epsilon_prime:
                        constraints += [cp.abs(F - x[i, j]) + cp.abs(F - x[lane - 2, j]) >= lv + D]

    # Objective function
    objective = cp.Minimize(cp.sum(cp.sum(xr - x + gamma * w)))

    # Problem
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI)


    acceleration = a.value
    print(acceleration)
    return acceleration

def set_parameters(parameters):
    #parameters
    t = 1
    max_speed = 80
    lower_acc = -7
    upper_acc = 7 #If you do this as 4, there is crash on our scenario test with too much accelaration
    speed_loc_fac = 0.49
    reaction_t = 1
    safety_distance = 2.5
    vehicle_length = 4

    parameters = [t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance, vehicle_length]
    #print(parameters)
    return parameters

# parameters = []
# parameters = set_parameters(parameters)

# Example inputs with correct size
v_input = [3.480213571712375, 3.8152709864545615, 0, 0, 0, 0, 0, 0]
x_input = [4.4126363327726725, 5.626537988381459, 0, 0, 0, 0, 0, 0]
xr_cons = [2951.88, 1955.94, 0, 0, 0, 0, 0, 0]
x_pos = [8.512636332772672, 9.726537988381459, 0, 0, 0, 0, 0, 0]

parameters = [1, 80, -7, 7, 0.49, 1, 2.5, 4]

get_optimized_acceleration(4, 2, v_input, x_input, xr_cons, x_pos, parameters)

