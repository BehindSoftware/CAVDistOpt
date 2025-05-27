def publish_vehicle_inf(vehicle_on_lane, map_to_lane, map_to_vehicle_num, step):

    #Vehicle <-> Sensors (Traci)
    v_platooning = {}
    x_platooning = {}
    xr_cons_platooning = {}
    x_pos_platoning = {}

    vehicle_index = map_to_vehicle_num[vehicle_on_lane]
    lane_number = map_to_lane[vehicle_on_lane]

    v_platooning[lane_number,vehicle_index] = traci.vehicle.getSpeed(vehicle_on_lane) #Take v0
    x_platooning[lane_number,vehicle_index] = traci.vehicle.getDistance(vehicle_on_lane) #odyometer for traveled distance
    xr_cons_platooning[lane_number,vehicle_index] = calculate_desired_route(vehicle_on_lane) #Take Xr
    x_pos_platoning[lane_number,vehicle_index] = traci.vehicle.getLanePosition(vehicle_on_lane)
    a_platoning[lane_number,vehicle_index] = traci.vehicle.getAcceleration(vehicle_on_lane)
    x, y = traci.vehicle.getPosition(vehicle_on_lane)

    message = DSRCMessage(version=1, msg_type=0, vehicle_id=vehicle_on_lane, x, y, v_current=v_platooning[lane_number,vehicle_index], acc=a_platoning[lane_number,vehicle_index], timestamp=step)

return message

def listen_vehicle_inf(message):

    #Take whole messages
    #Check your location and clarify you are intersected vehicle or platooning vehicle.
    #For intersected:
        #Check their x and y values, if it is in the same circle, take it.
    #For platooning:
        #Check their x and y values, if it is in the same lane, take it.

    #Check message type, if it is 0 (initial)
        #For intersected:
            # Calculate their time slot according to distance to intersection with x,y values / v_current and add time gap according to their distance to intersection and then assign to z values
        #For platooning:
            # Calculate the average of v_current in message and put it to z values
    
    #Init u as 0

return z, u

def listen_vehicle_inf_for_optimized(message):
    #Check message type, if it is 1 (optimized)
        #For intersected:
            # Calculate their time slot according to distance to intersection with x,y values / v_next and add time gap according to their distance to intersection and then assign to z values
        #For platooning:
            # Calculate the average of v_next in message and put it to z values
return z, u

def platooning_optimization(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, parameters, z, u, distances_dict, xr_dict, car_index, RHO):

    # x constraints
    for (number_of_lane, j), value in xr_cons.items():
        if value != 0 and j==car_index:
            constraints.append(x[number_of_lane, j] == 0.5 * a[number_of_lane, j] * t**2 + v_input[(number_of_lane, j)] * t + x_input[(number_of_lane, j)])

    # v constraints
    for (number_of_lane, j), value in xr_cons.items():
        if value != 0 and j==car_index:
            constraints.append(v[number_of_lane, j] == a[number_of_lane, j] * t + v_input[(number_of_lane, j)])

    # Velocity constraints: v should be between 0 and epsilon_prime
    if xr_cons[(number_of_lane, car_index)] != 0:
        constraints.append(v[number_of_lane, car_index] >= 0)  # v >= 0 (nonnegative)
        constraints.append(v[number_of_lane, car_index] <= epsilon_prime)  # v <= epsilon_prime

    # Acceleration constraints: a should be between alfa and alfa_prime
    if xr_cons[(number_of_lane, car_index)] != 0:
        constraints.append(a[number_of_lane, car_index] >= alfa)  # a >= alfa (minimum acceleration)
        constraints.append(a[number_of_lane, car_index] <= alfa_prime)  # a <= alfa_prime (maximum acceleration)

    # Objective function
    objective = cp.Minimize(
    cp.sum([
        xr_cons[(number_of_lane, j)] - x[number_of_lane, j] + gamma * cp.abs(v[number_of_lane, j] - v_input[(number_of_lane, j)])
        + (RHO / 2) * cp.square(v[number_of_lane, j] - z + u)
        for j in range(car_index, car_index + 1)
        if xr_cons[(number_of_lane, j)] != 0
    ])
    )

    # IF WE WANT TO DO HARD CONSTRAINT, IT MEANS IF ITERATION IS 3
    #Safe distance constraints (we need to the first car values in here)
        if number_of_vehicle > 1: #if we have 1 car, we need to check with intersected
            if car_index==1: #Means the car which need the first car information from intersected list
                if (number_of_lane,1) in xr_dict and xr_dict[(number_of_lane, 1)] is not None and (number_of_lane, 1) in xr_cons: #Check for whether there is front car in the intersection
                    if xr_dict[(number_of_lane, 1)] != 0 and xr_cons[(number_of_lane, 1)] != 0:
                        #TO DO: test this for sure about distances_dict
                        constraints += [distances_dict[(number_of_lane, 1)] - x[number_of_lane, 1] >= lv + D + R * v[number_of_lane, 1]]
                        local_v_flag = True
                    else:
                        pass
                        #Infeasible solution
                else: #The intersected cars in platooning list
                    constraints.append(x[number_of_lane, car_index - 1] - x[number_of_lane, car_index] >= lv + D + R * v[number_of_lane, car_index])
                    local_v_flag = True
            else: #other lane cars
                if xr_cons[(number_of_lane, car_index)] != 0 and xr_cons[(number_of_lane, car_index-1)] != 0:    
                    constraints.append(x[number_of_lane, car_index - 1] - x[number_of_lane, car_index] >= lv + D + R * v[number_of_lane, car_index])
                    local_v_flag = True
        else:
            local_v_flag = True

    #test
    print(f"Objective function: {objective}")

    # Problem
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.GUROBI, reoptimize=True, presolve=False)

    # Check the solution status
    if problem.status == cp.INFEASIBLE:
        print("Problem is infeasible.")
        return result, local_v
    elif problem.status == cp.UNBOUNDED:
        print("Problem is unbounded.")
        return result, local_v
    else:
        print("Solution found.")
        if (number_of_lane, car_index) in x and x[(number_of_lane, car_index)].value is not None:
            distance=x[(number_of_lane, car_index)].value
            result=a[(number_of_lane, car_index)].value

    if local_v_flag == True:
        local_v = v[(number_of_lane, car_index)].value

    return result, local_v


def main(step):
    publish_vehicle_inf(vehicle_on_lane, map_to_lane, map_to_vehicle_num, step) #Publish current values
    z, u =listen_vehicle_inf(message) #Listen the messages and parse as regional filtering then we will calculate initial z, u values (Normally we will do Geocasting DSRC to not take whole messages) 
    
    MAX_ITER = 4
    for iteration in range(MAX_ITER):
        z_prev = z
        #if intersected car:
            accelaration, local_v = intersected_optimization(number_of_vehicle, v_input, x_input, xr_cons, x_pos, parameters, z, u, distances_dict, xr_dict, car_index, RHO) #Calculate distancetointersection/v_next(local v.) and optimized accelaration
        #if platooning car:
            accelaration, local_v = platooning_optimization(number_of_lane, number_of_vehicle, v_input, x_input, xr_cons, parameters, z, u, distances_dict, xr_dict, car_index, RHO) #Calculate v_next(local v.) and optimized accelaration
        publish_vehicle_inf_for_optimized(vehicle_on_lane, step, local_v, accelaration)
        z_new, u_new = listen_vehicle_inf_for_optimized(message) #Listen the messages and parse as regional filtering then we will calculate updated z, u values (Normally we will do Geocasting DSRC to not take whole messages)
        
        if check_convergence(x, z_new, z_prev, length_of_lanes):
            print(f"Convergence reached after {iteration} iterations.")
            break
        
    calculated_speed = traci.vehicle.getSpeed(vehicle_on_lane)+accelaration*1 #t=1
    traci.vehicle.setSpeed(vehicle_on_lane,calculated_speed)


