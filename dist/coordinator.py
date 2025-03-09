import cvxpy as cp
import numpy as np
from dist.intersected import intersected_optimization, parsing_vehicle_data
from dist.platooning import platooning_optimization
from dist.simulator import *

#(number_of_lane, number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, parameters)

# Consensus ADMM parameters
MAX_ITER = 1000
RHO = 1.0
TOLERANCE = 1e-4

# Function to check convergence
def check_convergence(x_local_combined, z_new, z_prev):
    """Convergence check based on primal and dual residuals."""
    # Compute primal residuals
    primal_residual = np.linalg.norm(x_local_combined - z_new)
    
    # Compute dual residuals using the change in consensus variables
    dual_residual = RHO * np.linalg.norm(z_new - z_prev)

    # Check convergence
    
    return (primal_residual < TOLERANCE) and (dual_residual < TOLERANCE)


def admm_algorithm(intersected_information,platooning_information, map_to_lane, map_to_vehicle_num):
    print("Berkay")
    print(intersected_information)
    print("Saydam")
    # Unpack intersected information
    (
        number_of_lane_intersected, 
        number_of_vehicle_intersected, 
        v_intersected, 
        x_intersected, 
        xr_cons_intersected, 
        x_pos_intersected, 
        parameters_intersected, 
        intersected_list
    ) = intersected_information

    # Unpack platooning information
    (
        number_of_lane_platooning, 
        number_of_vehicle_platooning, 
        v_platooning, 
        x_platooning, 
        xr_cons_platooning, 
        x_pos_platooning, 
        parameters_platooning, 
        platooning_list
    ) = platooning_information

    # Initialization
    n_lanes = 4 #constant TO DO: CHECK
    z = np.zeros(n_lanes+1) # Consensus variable TO DO: can be improved to give average x0 values !!!CHECK FASTER CONVERGE WITH X0

    # New
    #z_intersected = np.zeros(number_of_lane_intersected)
    #z_platooning = np.zeros(number_of_vehicle_platooning)

    u = np.zeros(n_lanes+1) # Dual variable (Lagrange multipliers)
    x_local_combined = np.zeros(n_lanes+1)
    distances_dict = {}
    xr_dict = {}

    for iteration in range(MAX_ITER):
        index = 0
        # Temporary arrays to store local solutions
        x_intersected_local = np.zeros(number_of_vehicle_intersected)
        x_platooning_local = np.zeros(number_of_vehicle_platooning)

        # Store previous values of consensus variables for dual residual calculation
        z_prev = np.copy(z)

        #TO DO: Do we need to reset idx ? If not we need to hold idx after intersected list to not overwright the values in platooning 
        # Step 1: Local optimization for intersected group (each vehicle)# Perform local optimization for intersected vehicles, we are sending whole intersected cars because they depent on each others.
        if number_of_vehicle_intersected != 0:
            x_intersected_local = intersected_optimization(
                number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, parameters_intersected, z[index], u[index], distances_dict, xr_dict
            )

            x_local_combined[index] = np.average(x_intersected_local)
        
        if x_local_combined[index] == 0:
            print("ERROR: Infeasible")
            break
        # Step 2: Local optimization for platooning group (each vehicle)

        for lane_number in range(1, number_of_lane_platooning + 1):

            index += 1

            # Collect vehicle indices for the current lane
            vehicles_in_lane = [
                vehicle_id for vehicle_id in platooning_list if map_to_lane[vehicle_id] == lane_number
            ]

            # Check if there are any vehicles in this lane
            if not vehicles_in_lane:
                continue  # Skip if no vehicles are found in the current lane

            # Extract data for all vehicles in this lane
            v_lane = {}
            x_lane = {}
            xr_lane = {}
            x_pos_lane = {}

            # Populate the lane-specific data structures
            for vehicle_id in enumerate(vehicles_in_lane):
                vehicle_index = map_to_vehicle_num[vehicle_id[1]]

                # Fill lane-specific data dictionaries
                v_lane[(lane_number, vehicle_index)] = v_platooning.get((lane_number, vehicle_index), 0)
                x_lane[(lane_number, vehicle_index)] = x_platooning.get((lane_number, vehicle_index), 0)
                xr_lane[(lane_number, vehicle_index)] = xr_cons_platooning.get((lane_number, vehicle_index), 0)
                x_pos_lane[(lane_number, vehicle_index)] = x_pos_platooning.get((lane_number, vehicle_index), 0)
            # Perform optimization for all vehicles in the current lane
            if len(vehicles_in_lane) != 0:
                print(vehicles_in_lane)
                print(xr_lane[(lane_number, vehicle_index)])
                print(lane_number)
                print(vehicle_index)
                # TO DO: WE ARE HERE!!! When we check the lane by lane there is a problem like: We want to optimize (3,1) but there is Xcons value for (1,1) as well 
                print("lane_number",lane_number)
                print("len(vehicles_in_lane)",len(vehicles_in_lane))
                print("vehicles_in_lane",vehicles_in_lane)
                print("v_lane",v_lane)
                print("x_lane",x_lane)
                print("xr_lane",xr_lane)
                print("x_pos_lane",x_pos_lane)
                print("parameters_platooning",parameters_platooning)
                x_platooning_local = platooning_optimization(
                    lane_number, 
                    len(vehicles_in_lane), 
                    v_lane, 
                    x_lane, 
                    xr_lane, 
                    parameters_platooning, 
                    z[index], 
                    u[index], 
                    distances_dict,
                    xr_dict
                )

                # Update the results for each vehicle in this lane
                x_local_combined[index] = np.average(x_platooning_local)
                
        # Step 3: Consensus step (The division by 2 ensures the consensus is the average of the primal and dual updates.)
        #TO DO: we are not sure, they are solving together but their u's and z's different so it can be N but they are consensused in each other during solving, therefore we are having 5 z and u values 
        z = (x_local_combined + u / RHO) / (n_lanes+1) #TO DO: we can need to have summation to sum whole values of array CHECK!!!!standard practice typically divides by 2, balancing primal and dual variables equally.!!!

        # Step 4: Update dual variables
        u = u + RHO * (x_local_combined - z)

        # Step 5: Convergence check
        if check_convergence(x_local_combined, z, z_prev):

            print(f"Convergence reached after {iteration} iterations.")
            break

    return x_intersected_local, x_platooning_local

def prepare_data(intersected_list, lane_number, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, map_to_lane, map_to_vehicle_num):
    
    # Extract data for all vehicles in the intersection
    v_inter = {}
    x_inter = {}
    xr_inter = {}
    x_pos_inter = {}

    # Collect vehicle indices for the intersection
    vehicles_in_inter = [vehicle_id for vehicle_id in intersected_list]

    # Check if there are any vehicles in the intersection
    if not vehicles_in_inter:
        print("No car in intersection: " + str(lane_number))
        return v_inter, x_inter, xr_inter, x_pos_inter# Skip if no vehicles are found in the intersection

    # Populate the vehicle-specific data structures
    for vehicle_id in enumerate(vehicles_in_inter):
        vehicle_index = map_to_vehicle_num[vehicle_id[1]]
        lane_number = map_to_lane[vehicle_id[1]] #TO DO:test this!!!

        # Fill vehicle-specific data dictionaries
        v_inter[(lane_number, vehicle_index)] = v_intersected.get((lane_number, vehicle_index), 0)
        x_inter[(lane_number, vehicle_index)] = x_intersected.get((lane_number, vehicle_index), 0)
        xr_inter[(lane_number, vehicle_index)] = xr_cons_intersected.get((lane_number, vehicle_index), 0)
        x_pos_inter[(lane_number, vehicle_index)] = x_pos_intersected.get((lane_number, vehicle_index), 0)
    
    return v_inter, x_inter, xr_inter, x_pos_inter

def prepare_data_platooning(platooning_list,lane_number, v_platooning, x_platooning, xr_cons_platooning, x_pos_platooning, map_to_lane, map_to_vehicle_num):

    # Extract data for all vehicles in this lane
    v_lane = {}
    x_lane = {}
    xr_lane = {}
    x_pos_lane = {}

    # Collect vehicle indices for the current lane
    vehicles_in_lane = [vehicle_id for vehicle_id in platooning_list if map_to_lane[vehicle_id] == lane_number]

    # Check if there are any vehicles in this lane
    if not vehicles_in_lane:
        print("No car in lane: " + str(lane_number))
        return v_lane, x_lane, xr_lane, x_pos_lane # Skip if no vehicles are found in the current lane

    # Populate the lane-specific data structures
    for vehicle_id in enumerate(vehicles_in_lane):
        vehicle_index = map_to_vehicle_num[vehicle_id[1]]

        # Fill lane-specific data dictionaries
        v_lane[(lane_number, vehicle_index)] = v_platooning.get((lane_number, vehicle_index), 0)
        x_lane[(lane_number, vehicle_index)] = x_platooning.get((lane_number, vehicle_index), 0)
        xr_lane[(lane_number, vehicle_index)] = xr_cons_platooning.get((lane_number, vehicle_index), 0)
        x_pos_lane[(lane_number, vehicle_index)] = x_pos_platooning.get((lane_number, vehicle_index), 0)

    return v_lane, x_lane, xr_lane, x_pos_lane

#TO DO: 1,5 is not correct, we can not have car in lane 4, therefore it can be rearranged again from the beginning

def update_consensus(z, u, x):

    z_updated = np.copy(z)

    for lane_number in range(0, 5):
        if lane_number==0: #for intersection
            for idx in range(1,5): #each lane in the intersection
                if idx==1:
                    z_updated[lane_number][idx] = x[lane_number][idx] + u[lane_number][idx] / RHO
                else:
                    z_updated[lane_number][idx] = max(x[lane_number][idx] + u[lane_number][idx] / RHO, z_updated[0][1])
        else: #for platooning
            for idx in range(1,len(z[lane_number])):
                z_updated[lane_number][idx] = np.average(z_updated[lane_number])
    return z_updated

def update_dual(z, u, x):

    u_updated = np.copy(u)

    for lane_number in range(0, 5):
        for idx in range(1,len(u[lane_number])):
            u_updated[lane_number][idx] = u[lane_number][idx] + RHO * x[lane_number][idx] - z[lane_number][idx]

    return u_updated

def consensus_admm_algorithm(intersected_information,platooning_information, map_to_lane, map_to_vehicle_num):

    # Unpack intersected information
    (
        number_of_lane_intersected, 
        number_of_vehicle_intersected, 
        v_intersected, 
        x_intersected, 
        xr_cons_intersected, 
        x_pos_intersected, 
        parameters_intersected, 
        intersected_list
    ) = intersected_information

    # Unpack platooning information
    (
        number_of_lane_platooning, 
        number_of_vehicle_platooning, 
        v_platooning, 
        x_platooning, 
        xr_cons_platooning, 
        x_pos_platooning, 
        parameters_platooning, 
        platooning_list
    ) = platooning_information

    # Initialization
    n_lanes = 4 #constant TO DO: CHECK
    lane_number = 0
    number_of_vehicle = 0

    #0 = intersected; 1,2,3,4 = platooning lanes
    z = np.zeros((1+n_lanes, number_of_vehicle_intersected + number_of_vehicle_platooning))
    u = np.zeros((1+n_lanes, number_of_vehicle_intersected + number_of_vehicle_platooning))
    x = np.zeros((1+n_lanes, number_of_vehicle_intersected + number_of_vehicle_platooning))
    result = np.zeros((1+n_lanes, number_of_vehicle_intersected + number_of_vehicle_platooning))

    distances_dict = {}
    xr_dict = {}

    for iteration in range(MAX_ITER):
        # Temporary arrays to store local solutions
        # x_intersected_local = np.zeros(number_of_vehicle_intersected)
        # x_platooning_local = np.zeros(number_of_vehicle_platooning)

        # Store previous values of consensus variables for dual residual calculation
        #TO DO: we should store average values for platooning 
        z_prev = np.copy(z)
    
        v_inter, x_inter, xr_inter, x_pos_inter = prepare_data(intersected_list, lane_number, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, map_to_lane, map_to_vehicle_num)

        #TO DO: Do we need to reset idx ? If not we need to hold idx after intersected list to not overwright the values in platooning 
        # Step 1: Local optimization for intersected group (each vehicle)# Perform local optimization for intersected vehicles, we are sending whole intersected cars because they depent on each others.
        for idx in range(1, number_of_vehicle_intersected + 1):
            #TO DO: Adding one constraint for z; returning z,u and x_local values and also a value to map x_local values; change optimization for one car; optimization will be called for a thread
            #TO DO: x_local >= z + u xlocal = (Xl^t+1 - Fl)=zl (X^t+1 -Fm)=zm -> Clarify it
            number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle = parsing_vehicle_data(number_of_lane_intersected, number_of_vehicle, v_inter, x_inter, xr_inter, x_pos_inter, idx)
            result[lane_number][idx], x[lane_number][idx] = intersected_optimization(number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle, parameters_intersected, z[lane_number][idx], u[lane_number][idx], distances_dict, xr_dict, idx)

            if result[lane_number][idx] == 0:
                print("ERROR: Infeasible")
            print(result[lane_number][idx], x[lane_number][idx])
        new_arr = x[:number_of_vehicle_intersected] #TO DO: rearrange the arrays with unnecessary zeros
        lane_number =+ 1
        # Step 2: Local optimization for platooning group (each vehicle)
        
        for lane_number in range(1, number_of_lane_platooning + 1): #1,2,3,4
    
            v_lane, x_lane, xr_lane, x_pos_lane = prepare_data_platooning(platooning_list,lane_number, v_platooning, x_platooning, xr_cons_platooning, x_pos_platooning, map_to_lane, map_to_vehicle_num)

            # Perform optimization for all vehicles in the current lane
            for idx in reversed(range(2,len(xr_lane)+1)): #Starts from 2 for ignore the first car
                number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle = parsing_vehicle_data(lane_number, number_of_vehicle, v_lane, x_lane, xr_lane, x_pos_lane, idx)
                result[lane_number][idx], x[lane_number][idx] = platooning_optimization(lane_number, number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, parameters_platooning, z[lane_number][idx], u[lane_number][idx], distances_dict, xr_dict, idx)
            
                if result[lane_number][idx] == 0:
                    print("ERROR: Infeasible")
            print(result[lane_number][idx], x[lane_number][idx])
        # Step 3: Consensus step

        z_new = update_consensus(z, u, x)

        # Step 4: Update dual variables

        u_new = update_dual(z, u, x)

        # Step 5: Convergence check

        if check_convergence(x, z_new, z_prev):

            print(f"Convergence reached after {iteration} iterations.")
            break

    return result