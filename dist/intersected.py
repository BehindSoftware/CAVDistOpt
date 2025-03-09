import cvxpy as cp
import numpy as np

#number_of_vehicle to understand there is car in the next lane(right one)
#v_input for vehicle's current velocity (the car and right one)
#x_input for vehicle's current distance travelled (the car and right one)
#xr_cons for vehicle's destination (the car and right one)
#x_pos to understand passed vehicle's intersection (the car and right one)
#parameters for optimization
#z is consensus variable
#u is dual update variable
#distances_dict is X^t+1 value for platooning cars
#xr_dict is xr_cons value for platooning cars
#car_index is index for vehicle -> number_of_lane


def intersected_optimization(number_of_vehicle, v_input, x_input, xr_cons, x_pos, parameters, z, u, distances_dict, xr_dict, car_index):
    
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

    #constraints
    constraints = []
    local_v = 0
    distance = []

    if(number_of_vehicle==0):
        print("There is no vehicle")
        distance.append(0)
        return distance[0], local_v
    else:
        #decision variables (scan each lane and define variable for having car) #can be filtered like platooning, we can define variables for just need of them
        v = {(i, 1): cp.Variable(nonneg=True) for i in range(car_index, car_index + number_of_vehicle) if xr_cons[(i, 1)] != 0} #car_index is that car, car_index+1+1 one for next car one for range typo
        x = {(i, 1): cp.Variable(nonneg=True) for i in range(car_index, car_index + number_of_vehicle) if xr_cons[(i, 1)] != 0}
        a = {(i, 1): cp.Variable() for i in range(car_index, car_index + number_of_vehicle) if xr_cons[(i, 1)] != 0}
    
    #test

    # print("v:",v)
    # print("x:",x)
    # print("a:",a)

    # print("v_input: ",v_input)
    # print("x_input: ",x_input)
    print("xr_cons: ",xr_cons)
    # print("x_pos  : ",x_pos)

    # x constraints
    for (i, j), value in xr_cons.items():
        if value != 0 and i==car_index:
            constraints.append(x[i, 1] == 0.5 * a[i, 1] * t**2 + v_input[(i, 1)] * t + x_input[(i, 1)])

    # v constraints
    for (i, j), value in xr_cons.items():
        if value != 0 and i==car_index:
            constraints.append(v[i, 1] == a[i, 1] * t + v_input[(i, 1)])

    # Lane crossing constraints
    if(number_of_vehicle==2):
        #for i in range(car_index, car_index + 1): #+1 because just one constraint for two cars
            #if xr_cons[(i, 1)] != 0 and xr_cons[(i+1, 1)] != 0:
        if(x_pos[car_index,1]<F and x_pos[car_index+1,1]<F): #Checks this is the first intersection for cars, if not m.F will be increased because of usage distance travelled X^t+1
            if x_pos[(car_index, 1)] >= F - epsilon_prime and x_pos[(car_index+1, 1)] >= F - epsilon_prime:
                check_for_will_pass_inters = x_pos[car_index,1]+v_input[car_index,1]-F
                check_for_will_pass_inters_lane2 = x_pos[car_index+1,1]+v_input[car_index+1,1]-7-F
                if(check_for_will_pass_inters<0 and check_for_will_pass_inters_lane2<0): #This checks for absolute between F and X^t+1
                    constraints.append((F-x[car_index,1])+(F-x[car_index+1,1])>=(lv+D))
                    constraints.append((F-x[car_index,1])>=(z+u))
                    #TO DO: Think about this, how local_v can be calculated, x is not value
                    #local_v = F-x[car_index,1]
                elif(check_for_will_pass_inters>0 and check_for_will_pass_inters_lane2<0):
                    constraints.append((x[car_index,1]-F)+(F-x[car_index+1,1])>=(lv+D))
                    constraints.append((x[car_index,1]-F)>=(z+u))
                    #local_v = x[car_index,1]-F
                elif(check_for_will_pass_inters<0 and check_for_will_pass_inters_lane2>0):
                    constraints.append((F-x[car_index,1])+(x[car_index+1,1]-F)>=(lv+D))
                    constraints.append((F-x[car_index,1])>=(z+u))
                    #local_v = F-x[car_index,1]
                else:
                    constraints.append((x[car_index,1]-F)+(x[car_index+1,1]-F)>=(lv+D))
                    constraints.append((x[car_index,1]-F)>=(z+u))
                    #local_v = x[car_index,1]-F
        elif(x_input[car_index,1]>F and x_input[car_index+1,1]<F):
            constraints.append ((2*F-x[car_index,1])+(F-x[car_index+1,1])>=(lv+D))
        elif(x_input[car_index,1]<F and x_input[car_index+1,1]>F):
            constraints.append ((F-x[car_index,1])+(2*F-x[car_index+1,1])>=(lv+D))
        elif(x_input[car_index,1]>F and x_input[car_index+1,1]>F):
            constraints.append ((2*F-x[car_index,1])+(2*F-x[car_index+1,1])>=(lv+D))
        elif(x_input[car_index,1]>2*F and x_input[car_index+1,1]>2*F):
            constraints.append ((3*F-x[car_index,1])+(3*F-x[car_index+1,1])>=(lv+D))
        else:
            pass

    # DECISION: The other car should not be limited
    # Velocity constraints: v should be between 0 and epsilon_prime
    if xr_cons[(car_index, 1)] != 0:
        constraints.append(v[car_index, 1] >= 0)  # v >= 0 (nonnegative)
        constraints.append(v[car_index, 1] <= epsilon_prime)  # v <= epsilon_prime

    # Acceleration constraints: a should be between alfa and alfa_prime
    if xr_cons[(car_index, 1)] != 0:
        constraints.append(a[car_index, 1] >= alfa)  # a >= alfa (minimum acceleration)
        constraints.append(a[car_index, 1] <= alfa_prime)  # a <= alfa_prime (maximum acceleration)

    #test
    # for i in range(0, len(constraints)):
    #     print(constraints[i])

    # Objective function
    objective = cp.Minimize(
    cp.sum([
        xr_cons[(i, 1)] - x[i, 1] + gamma * cp.abs(v[i, 1] - v_input[(i, 1)])
        for i in range(car_index, car_index + 1)
        if xr_cons[(i, 1)] != 0
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

    # Check the solution status
    if problem.status == cp.INFEASIBLE:
        print("Problem is infeasible.")
        #acceleration = {key: 0 for key in a} #Reset values
        #distance = {key: 0 for key in x} #Reset values
        distance.append(0) #Reset values
    elif problem.status == cp.UNBOUNDED:
        print("Problem is unbounded.")
        #acceleration = {key: 0 for key in a} #Reset values
        #distance = {key: 0 for key in x} #Reset values
        distance.append(0) #Reset values
    else:
        print("Solution found.")
        if (car_index, 1) in x and x[(car_index, 1)].value is not None:
            distance.append(x[(car_index, 1)].value) #X_local output
            distances_dict[(car_index, 1)] = x[(car_index, 1)].value #X value for platooning cars
            xr_dict[(car_index, 1)] = xr_cons[(car_index, 1)] #Xr value for platooning cars

    print(f"Distance (as list): {distance}")
    #TO DO: fill distances_list as dict for each car distances

    return distance[0], local_v

def parsing_vehicle_data(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, x_pos, idx):

    v_vehicle = {}
    x_vehicle = {}
    xrcons_vehicle = {}
    xpos_vehicle = {}

    if (idx, 1) in xr_cons and idx == number_of_lane: #Last lane
        v_vehicle = {
            (idx,1): v_input[(idx, 1)],
        }
        x_vehicle = {
            (idx,1): x_input.get((idx, 1), None),
        }
        xrcons_vehicle = {
            (idx,1): xr_cons.get((idx, 1), None),
        }
        xpos_vehicle = {
            (idx,1): x_pos.get((idx, 1), None),
        }
        number_of_vehicle = 1
    elif (idx, 1) in xr_cons and (idx + 1, 1) in xr_cons: #If there is car in next lane
        v_vehicle = {
            (idx,1): v_input[(idx, 1)],
            (idx+1,1): v_input[(idx + 1, 1)]
        }
        x_vehicle = {
            (idx,1): x_input.get((idx, 1), None),
            (idx+1,1): x_input.get((idx + 1, 1), None)
        }
        xrcons_vehicle = {
            (idx,1): xr_cons.get((idx, 1), None),
            (idx+1,1): xr_cons.get((idx + 1, 1), None)
        }
        xpos_vehicle = {
            (idx,1): x_pos.get((idx, 1), None),
            (idx+1,1): x_pos.get((idx + 1, 1), None)
        }
        number_of_vehicle = 2
    elif (idx, 1) in xr_cons:   #If there is no car in next lane
        v_vehicle = {
            (idx,1): v_input[(idx, 1)],
        }
        x_vehicle = {
            (idx,1): x_input.get((idx, 1), None),
        }
        xrcons_vehicle = {
            (idx,1): xr_cons.get((idx, 1), None),
        }
        xpos_vehicle = {
            (idx,1): x_pos.get((idx, 1), None),
        }
        number_of_vehicle = 1
    else:               #If the car does not exist in that lane
        number_of_vehicle = 0

    print(v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle)
    return number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle

def test_dist_opt():
    v_input = {(1, 1): 9.768100274959579, (2, 1): 1.8596483482979238, (3, 1): 11.0, (3, 2): 4.0, (4, 1): 11.77369166086428, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    x_input = {(1, 1): 13.995449316874145, (2, 1): 492, (3, 1): 480, (3, 2): 475, (4, 1): 18.80794448377565, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    xr_cons = {(1, 1): 984.27, (2, 1): 984.27, (3, 1): 984.27, (3, 2): 984.27, (4, 1): 984.27, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    x_pos = {(1, 1): 18.095449316874145, (2, 1): 492, (3, 1): 480, (3, 2): 475, (4, 1): 22.907944483775648, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0}
    number_of_lane = 4
    number_of_vehicle = 5
    #TO DO: z and u should be updated
    z = np.zeros((number_of_lane + 1, number_of_vehicle + 1))
    u = np.zeros((number_of_lane + 1, number_of_vehicle + 1))
    RHO = 1.0 
    parameters = [1, 80, -7, 7, 0.49, 1, 2.5, 4]
    distances_dict = {}
    xr_dict = {}

    # Extract unique indices that have (index,1) as a key
    indices = sorted(set(k[0] for k in xr_cons.keys() if k[1] == 1))
    print(indices)
    for idx in indices:
        number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle = parsing_vehicle_data(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, x_pos, idx)
        intersected_optimization(number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle, parameters, z[idx], u[idx], distances_dict, xr_dict, idx)
        
    print("Test finished")

#test_dist_opt()