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

    #decision variables
    v = {(i, j): cp.Variable(nonneg=True) for i in range(1, number_of_lane + 1) for j in range(1, number_of_vehicle + 1) if xr_cons[(i, j)] != 0}
    x = {(i, j): cp.Variable(nonneg=True) for i in range(1, number_of_lane + 1) for j in range(1, number_of_vehicle + 1) if xr_cons[(i, j)] != 0}
    a = {(i, j): cp.Variable() for i in range(1, number_of_lane + 1) for j in range(1, number_of_vehicle + 1) if xr_cons[(i, j)] != 0}

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
    for (i, j), value in xr_cons.items():
        if value != 0:
            constraints.append(x[i, j] == 0.5 * a[i, j] * t**2 + v_input[(i, j)] * t + x_input[(i, j)])

    # v constraints
    for (i, j), value in xr_cons.items():
        if value != 0:
            constraints.append(v[i, j] == a[i, j] * t + v_input[(i, j)])

    # Safe distance constraints
    if number_of_vehicle > 2:
        for i in range(1, number_of_lane + 1):
            for j in range(1, number_of_vehicle):
                if xr_cons[(i, j)] != 0 and xr_cons[(i, j + 1)] != 0:
                    constraints += [x[i, j] - x[i, j + 1] >= lv + D + R * v[i, j + 1]]
                    #constraints.append(x[i, j] - x[i, j + 1] >= lv + D + R * v[i, j + 1]) Test it

    # Lane crossing constraints
    for lane in range(2, 5):
        for i in range(1, number_of_lane + 1):
            for j in range(1, number_of_vehicle + 1):
                if xr_cons[(i, j)] != 0 and xr_cons[(lane, j)] != 0 and i < lane:
                    if(x_pos[i,j]<F and x_pos[lane,j]<F): #Checks this is the first intersection for cars, if not m.F will be increased because of usage distance travelled X^t+1
                        if x_pos[(i, j)] >= F - epsilon_prime and x_pos[(lane, j)] >= F - epsilon_prime:
                            check_for_will_pass_inters = x_pos[i,j]+v_input[i,j]-F
                            check_for_will_pass_inters_lane2 = x_pos[lane,j]+v_input[lane,j]-7-F
                            print(i,j,lane,j)
                            if(check_for_will_pass_inters<0 and check_for_will_pass_inters_lane2<0): #This checks for absolute between F and X^t+1
                                constraints.append((F-x[i,j])+(F-x[lane,j])>=(lv+D))
                            elif(check_for_will_pass_inters>0 and check_for_will_pass_inters_lane2<0):
                                constraints.append((x[i,j]-F)+(F-x[lane,j])>=(lv+D))
                            elif(check_for_will_pass_inters<0 and check_for_will_pass_inters_lane2>0):
                                constraints.append((F-x[i,j])+(x[lane,j]-F)>=(lv+D))
                            else:
                                constraints.append((x[i,j]-F)+(x[lane,j]-F)>=(lv+D))
                    elif(x_input[i,j]>F and x_input[lane,j]<F):
                        constraints.append ((2*F-x[i,j])+(F-x[lane,j])>=(lv+D))
                    elif(x_input[i,j]<F and x_input[lane,j]>F):
                        constraints.append ((F-x[i,j])+(2*F-x[lane,j])>=(lv+D))
                    elif(x_input[i,j]>F and x_input[lane,j]>F):
                        constraints.append ((2*F-x[i,j])+(2*F-x[lane,j])>=(lv+D))
                    elif(x_input[i,j]>2*F and x_input[lane,j]>2*F):
                        constraints.append ((3*F-x[i,j])+(3*F-x[lane,j])>=(lv+D))
                    else:
                        pass

    # Velocity constraints: v should be between 0 and epsilon_prime
    for i in range(1, number_of_lane + 1):
        for j in range(1, number_of_vehicle + 1):
            if xr_cons[(i, j)] != 0:
                constraints.append(v[i, j] >= 0)  # v >= 0 (nonnegative)
                constraints.append(v[i, j] <= epsilon_prime)  # v <= epsilon_prime

    # Acceleration constraints: a should be between alfa and alfa_prime
    for i in range(1, number_of_lane + 1):
        for j in range(1, number_of_vehicle + 1):
            if xr_cons[(i, j)] != 0:
                constraints.append(a[i, j] >= alfa)  # a >= alfa (minimum acceleration)
                constraints.append(a[i, j] <= alfa_prime)  # a <= alfa_prime (maximum acceleration)

    #test
    # for i in range(0, len(constraints)):
    #     print(constraints[i])

    # Objective function
    objective = cp.Minimize(cp.sum([xr_cons[(i, j)] - x[i, j] + gamma * cp.abs(v[i, j] - v_input[(i, j)]) for i in range(1, number_of_lane + 1) for j in range(1, number_of_vehicle + 1) if xr_cons[(i, j)] != 0]))

    #test
    print(f"Objective function: {objective}")

    # Problem
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI, reoptimize=True, presolve=False)


    acceleration = {key: a[key].value for key in a}
    # Check the solution status
    if problem.status == cp.INFEASIBLE:
        print("Problem is infeasible.")
        acceleration = {key: 0 for key in a} #Reset values
    elif problem.status == cp.UNBOUNDED:
        print("Problem is unbounded.")
        acceleration = {key: 0 for key in a} #Reset values
    else:
        print("Solution found.")

    print(f"Acceleration: {acceleration}")

    return acceleration

def test_dist_opt():
    v_input = {(1, 1): 9.768100274959579, (2, 1): 1.8596483482979238, (3, 1): 11.0, (3, 2): 4.0, (4, 1): 11.77369166086428, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    x_input = {(1, 1): 13.995449316874145, (2, 1): 492, (3, 1): 480, (3, 2): 475, (4, 1): 18.80794448377565, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    xr_cons = {(1, 1): 984.27, (2, 1): 984.27, (3, 1): 984.27, (3, 2): 984.27, (4, 1): 984.27, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    x_pos = {(1, 1): 18.095449316874145, (2, 1): 492, (3, 1): 480, (3, 2): 475, (4, 1): 22.907944483775648, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}

    parameters = [1, 80, -7, 7, 0.49, 1, 2.5, 4]

    get_optimized_acceleration(4, 5, v_input, x_input, xr_cons, x_pos, parameters)
    print("Test finished")

#test_dist_opt()