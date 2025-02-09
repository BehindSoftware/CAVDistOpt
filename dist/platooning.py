import cvxpy as cp
import numpy as np

def platooning_optimization(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, x_pos, parameters, z, u, RHO, distances_dict, xr_dict):
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

    #decision variables -> #platooning is started from 2 to (number_of_vehicle+2) because 1 for range(started with 0) 1 for second car(not intersected), lane will be constant
    v = {(number_of_lane, j): cp.Variable(nonneg=True) for j in range(2, number_of_vehicle + 2) if xr_cons[(number_of_lane, j)] != 0} 
    x = {(number_of_lane, j): cp.Variable(nonneg=True) for j in range(2, number_of_vehicle + 2) if xr_cons[(number_of_lane, j)] != 0}
    a = {(number_of_lane, j): cp.Variable() for j in range(2, number_of_vehicle + 2) if xr_cons[(number_of_lane, j)] != 0}

    #constraints
    constraints = []

    #test

    # print("v:",v)
    # print("x:",x)
    # print("a:",a)

    # print("v_input: ",v_input)
    # print("x_input: ",x_input)
    # print("xr_cons: ",xr_cons)
    # print("x_pos  : ",x_pos)

    # x constraints
    for (number_of_lane, j), value in xr_cons.items():
        if value != 0:
            constraints.append(x[number_of_lane, j] == 0.5 * a[number_of_lane, j] * t**2 + v_input[(number_of_lane, j)] * t + x_input[(number_of_lane, j)])

    # v constraints
    for (number_of_lane, j), value in xr_cons.items():
        if value != 0:
            constraints.append(v[number_of_lane, j] == a[number_of_lane, j] * t + v_input[(number_of_lane, j)])

    # Safe distance constraints (we need to the first car values in here)
    if number_of_vehicle > 0: #if we have 1 car, we need to check with intersected
        for j in range(1, number_of_vehicle+1): #we need to think like intersected
            #if xr_cons[(number_of_lane, j)] != 0 and xr_cons[(number_of_lane, j + 1)] != 0:
            if xr_dict[(number_of_lane, 1)] != 0 and xr_cons[(number_of_lane, j + 1)] != 0:
                constraints += [distances_dict[(number_of_lane, 1)] - x[number_of_lane, j + 1] >= lv + D + R * v[number_of_lane, j + 1]]
                #constraints.append(x[i, j] - x[i, j + 1] >= lv + D + R * v[i, j + 1]) Test it

    # Velocity constraints: v should be between 0 and epsilon_prime
    for j in range(2, number_of_vehicle + 2):
        if xr_cons[(number_of_lane, j)] != 0:
            constraints.append(v[number_of_lane, j] >= 0)  # v >= 0 (nonnegative)
            constraints.append(v[number_of_lane, j] <= epsilon_prime)  # v <= epsilon_prime

    # Acceleration constraints: a should be between alfa and alfa_prime
    for j in range(2, number_of_vehicle + 2):
        if xr_cons[(number_of_lane, j)] != 0:
            constraints.append(a[number_of_lane, j] >= alfa)  # a >= alfa (minimum acceleration)
            constraints.append(a[number_of_lane, j] <= alfa_prime)  # a <= alfa_prime (maximum acceleration)

    #test
    # for i in range(0, len(constraints)):
    #     print(constraints[i])
    #TO DO: Do we need to split objective function ?
    # Objective function
    objective = cp.Minimize(
    cp.sum([
        xr_cons[(number_of_lane, j)] - x[number_of_lane, j] + gamma * cp.abs(v[number_of_lane, j] - v_input[(number_of_lane, j)])
        + (RHO / 2) * cp.sum_squares(x[(number_of_lane, j)] - z + u) #TO DO: check maybe u/rho 
        for j in range(2, number_of_vehicle + 2)
        if xr_cons[(number_of_lane, j)] != 0
    ])
    )

    #test
    print(f"Objective function: {objective}")

    # Problem
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI, reoptimize=True, presolve=False)

    #acceleration = {key: a[key].value for key in a}
    #distance = {key: x[key].value for key in x}
    # Convert results to a list
    distance = []
    # Check the solution status
    if problem.status == cp.INFEASIBLE:
        print("Problem is infeasible.")
        #acceleration = {key: 0 for key in a} #Reset values
        #distance = {key: 0 for key in x} #Reset values
        distance = [0] * (number_of_lane * number_of_vehicle) #Reset values
    elif problem.status == cp.UNBOUNDED:
        print("Problem is unbounded.")
        #acceleration = {key: 0 for key in a} #Reset values
        #distance = {key: 0 for key in x} #Reset values
        distance = [0] * (number_of_lane * number_of_vehicle) #Reset values
    else:
        print("Solution found.")
        for j in range(2, number_of_vehicle + 2):
            if (number_of_lane, j) in x and x[(number_of_lane, j)].value is not None:
                distance.append(x[(number_of_lane, j)].value)

    print(f"Distance (as list): {distance}")
    #TO DO: fill distances_list as dict for each car distances

    return distance

def test_dist_opt():
    v_input = {(1, 1): 9.768100274959579, (2, 1): 1.8596483482979238, (3, 1): 11.0, (3, 2): 4.0, (4, 1): 11.77369166086428, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    x_input = {(1, 1): 13.995449316874145, (2, 1): 492, (3, 1): 480, (3, 2): 475, (4, 1): 18.80794448377565, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    xr_cons = {(1, 1): 984.27, (2, 1): 984.27, (3, 1): 984.27, (3, 2): 984.27, (4, 1): 984.27, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    x_pos = {(1, 1): 18.095449316874145, (2, 1): 492, (3, 1): 480, (3, 2): 475, (4, 1): 22.907944483775648, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    number_of_lane = 4
    number_of_vehicle = 5
    z = np.zeros((number_of_lane + 1, number_of_vehicle + 1))
    u = np.zeros((number_of_lane + 1, number_of_vehicle + 1))
    RHO = 1.0 
    parameters = [1, 80, -7, 7, 0.49, 1, 2.5, 4]
    distances_dict = {}

    platooning_optimization(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, x_pos, parameters, z, u, RHO, distances_dict)
    print("Test finished")

#test_dist_opt()