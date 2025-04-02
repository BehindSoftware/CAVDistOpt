import cvxpy as cp
import numpy as np
from dist.intersected import intersected_optimization, parsing_vehicle_data
from dist.platooning import platooning_optimization, parsing_vehicle_data_platooning
from dist.simulator import *

WEIGHTED_AVERAGE_CONSENSUS_ACTIVE = False

# Consensus ADMM parameters
MAX_ITER = 10
RHO = 1.0
TOLERANCE = 1.5 #Determine according to sensitivity 

# Function to check convergence
def check_convergence(x, z_new, z_prev, length_of_lanes):
    """Convergence check based on primal and dual residuals."""
    # Initialize residuals
    primal_residual_sum = 0
    dual_residual_sum = 0

    #TO DO CHECK: Below loop takes substration of whole lane vehicles

    # Compute residuals for each lane
    for lane_number in range(len(length_of_lanes)):
        # Compute primal residuals for the current lane
        primal_residual_sum += np.linalg.norm(x[lane_number] - z_new[lane_number])

        # Compute dual residuals for the current lane using the change in consensus variables
        dual_residual_sum += np.linalg.norm(z_new[lane_number] - z_prev[lane_number])

    # Compute overall residuals
    primal_residual = primal_residual_sum
    dual_residual = RHO * dual_residual_sum

    # Check convergence
    return (primal_residual < TOLERANCE) and (dual_residual < TOLERANCE)

def prepare_data(intersected_list, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, map_to_lane, map_to_vehicle_num, number_of_vehicle):
    
    # Extract data for all vehicles in the intersection
    v_inter = {}
    x_inter = {}
    xr_inter = {}
    x_pos_inter = {}

    # Collect vehicle indices for the intersection
    vehicles_in_inter = [vehicle_id for vehicle_id in intersected_list]

    # Check if there are any vehicles in the intersection
    if not vehicles_in_inter:
        print("prepare_data: No car in intersection for whole lanes")
        return v_inter, x_inter, xr_inter, x_pos_inter, number_of_vehicle# Skip if no vehicles are found in the intersection

    # Populate the vehicle-specific data structures
    for vehicle_id in enumerate(vehicles_in_inter):
        vehicle_index = map_to_vehicle_num[vehicle_id[1]]
        lane_number = map_to_lane[vehicle_id[1]]

        # Fill vehicle-specific data dictionaries
        v_inter[(lane_number, vehicle_index)] = v_intersected.get((lane_number, vehicle_index), 0)
        x_inter[(lane_number, vehicle_index)] = x_intersected.get((lane_number, vehicle_index), 0)
        xr_inter[(lane_number, vehicle_index)] = xr_cons_intersected.get((lane_number, vehicle_index), 0)
        x_pos_inter[(lane_number, vehicle_index)] = x_pos_intersected.get((lane_number, vehicle_index), 0)
        number_of_vehicle += 1
    
    return v_inter, x_inter, xr_inter, x_pos_inter, number_of_vehicle

def prepare_data_platooning(platooning_list,lane_number, v_platooning, x_platooning, xr_cons_platooning, x_pos_platooning, map_to_lane, map_to_vehicle_num, number_of_vehicle):

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
        return v_lane, x_lane, xr_lane, x_pos_lane, number_of_vehicle # Skip if no vehicles are found in the current lane

    # Populate the lane-specific data structures
    for vehicle_id in enumerate(vehicles_in_lane):
        vehicle_index = map_to_vehicle_num[vehicle_id[1]]

        # Fill lane-specific data dictionaries
        v_lane[(lane_number, vehicle_index)] = v_platooning.get((lane_number, vehicle_index), 0)
        x_lane[(lane_number, vehicle_index)] = x_platooning.get((lane_number, vehicle_index), 0)
        xr_lane[(lane_number, vehicle_index)] = xr_cons_platooning.get((lane_number, vehicle_index), 0)
        x_pos_lane[(lane_number, vehicle_index)] = x_pos_platooning.get((lane_number, vehicle_index), 0)
        number_of_vehicle += 1

    print("prepare_data_platooning: ")
    print(v_lane, x_lane, xr_lane, x_pos_lane)
    return v_lane, x_lane, xr_lane, x_pos_lane, number_of_vehicle

def update_consensus(z, u, x, cars_in_lanes, length_of_lanes):

    #Create same structure with z
    z_updated = np.copy(z)

    for lane_number in range(0, 5): # it is constant lane 0= intersection, lane 1,2,3,4 lanes
        if lane_number==0: #for intersection
            first_flag = True
            consensus_idx = 0 #For intersection index 0 z[0], u[0], x[0]
            for idx in range(1,5): #each lane in the intersection lane 1,2,3,4
                if idx in cars_in_lanes and cars_in_lanes[idx] != -1:
                    if first_flag==True:
                        z_updated[lane_number][consensus_idx] = x[lane_number][consensus_idx] + u[lane_number][consensus_idx] / RHO
                        first_flag = False
                        pre_idx = consensus_idx
                    else:
                        z_updated[lane_number][consensus_idx] = max(x[lane_number][consensus_idx] + u[lane_number][consensus_idx] / RHO, z_updated[lane_number][pre_idx])
                        pre_idx = consensus_idx
                    consensus_idx+=1
        else: #for platooning
            if(WEIGHTED_AVERAGE_CONSENSUS_ACTIVE==True):
                #TO DO: NOT IMPLEMENTED need Weights and think structure
                weights = 0 
                for lane_number in range(1,len(z_updated)):
                    # Compute the weighted average of local variables
                    row_average = np.average(z_updated[lane_number], axis=0, weights=weights)
                    z_updated[lane_number] = np.full_like(z_updated[lane_number], row_average)
            else:
                # Calculate the average of each row and update the z values with these averages
                for lane_number in range(1,len(z_updated)):
                    row_average = np.mean(z_updated[lane_number])
                    z_updated[lane_number] = np.full_like(z_updated[lane_number], row_average)

    return z_updated

def update_dual(z, u, x):

    u_updated = np.copy(u)

    for lane_number in range(0, 5): # it is constant lane 0= intersection, lane 1,2,3,4 lanes
        for idx in range(0,len(u[lane_number])):
            u_updated[lane_number][idx] = u[lane_number][idx] + RHO * (x[lane_number][idx] - z[lane_number][idx])

    return u_updated

def consensus_admm_algorithm(intersected_information,platooning_information, map_to_lane, map_to_vehicle_num, length_of_lanes):

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
    n_lanes = 4 #constant
    lane_number = 0
    number_of_vehicle = 0
    cars_in_lanes = {}

    #Consensus ADMM variables are hold in np 2D array like [array([0., 0., 0.]) array([0., 0., 0., 0., 0.])]
    #0 = intersected; 1,2,3,4 = platooning lanes
    # Create a 2D array with different column sizes
    z = np.empty((len(length_of_lanes),), dtype=object)
    u = np.empty((len(length_of_lanes),), dtype=object)
    x = np.empty((len(length_of_lanes),), dtype=object)
    result = np.empty((len(length_of_lanes),), dtype=object)
    for i, length in enumerate(length_of_lanes):
        z[i] = np.zeros(length)
        u[i] = np.zeros(length)
        x[i] = np.zeros(length)
        result[i] = np.zeros(length)

    #Vehicle knowledge like speed, position, acceleration are hold in dictionary like v_inter: {(1, 1): 10.5, (1, 2): 12.3, (1, 3): 9.8}
    distances_dict = {}
    xr_dict = {}

    for iteration in range(MAX_ITER):

        # Store previous values of consensus variables for dual residual calculation
        z_prev = np.copy(z)
        print("Iteration:" + str(iteration))
        print("z:" + str(z)) 
        print("u:" + str(u))
        print("x:" + str(x))
        print("result:" + str(result))

        # Prepare data for intersected cars
        v_inter, x_inter, xr_inter, x_pos_inter, number_of_vehicle = prepare_data(intersected_list, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, map_to_lane, map_to_vehicle_num, number_of_vehicle)

        # Step 1: Local optimization for intersected group
        if number_of_vehicle!= 0:
            consensus_idx = 0
            for laneID in range(1, 5): # For lane 1,2,3,4
                #parsing_vehicle_data to take current car data
                number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle, cars_in_lanes = parsing_vehicle_data(4, 0, v_inter, x_inter, xr_inter, x_pos_inter, laneID)

                if cars_in_lanes[laneID] != -1:
                    print("First car of LaneID:"+str(laneID)+ " Consensus_index:"+ str(consensus_idx))
                    result[0][consensus_idx], x[0][consensus_idx] = intersected_optimization(number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle, parameters_intersected, z[0][consensus_idx], u[0][consensus_idx], distances_dict, xr_dict, laneID) #Intersected is hold in 0 index
                    print("Accelaration:" + str(result[0][consensus_idx]) + "Local_v:" + str(x[0][consensus_idx]))
                    consensus_idx+=1

        # Step 2: Local optimization for platooning group (each vehicle)
        
        for laneID in range(1, 5): # For lane 1,2,3,4
            consensus_idx=len(z[laneID])-1 #index starts from 0 so need -1
            number_of_vehicle = 0
            #prepare_data_platooning to take car data which are current lane
            v_lane, x_lane, xr_lane, x_pos_lane, number_of_vehicle = prepare_data_platooning(platooning_list,laneID, v_platooning, x_platooning, xr_cons_platooning, x_pos_platooning, map_to_lane, map_to_vehicle_num, number_of_vehicle)

            # Perform optimization for all vehicles in the current lane
            if number_of_vehicle!= 0:
                for idx in reversed(range(1,len(z[laneID])+1)):
                    #parsing_vehicle_data to take current car data
                    number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle = parsing_vehicle_data_platooning(laneID, number_of_vehicle, v_lane, x_lane, xr_lane, x_pos_lane, idx)
                    result[laneID][consensus_idx], x[laneID][consensus_idx] = platooning_optimization(laneID, number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, parameters_platooning, z[laneID][consensus_idx], u[laneID][consensus_idx], distances_dict, xr_dict, idx)
                    print("Accelaration:" + str(result[laneID][consensus_idx]) + "Local_v:" + str(x[laneID][consensus_idx]))
                    consensus_idx-=1
        # Step 3: Consensus step

        z = update_consensus(z, u, x, cars_in_lanes, length_of_lanes)
        print("updated z:" + str(z))

        # Step 4: Update dual variables

        u = update_dual(z_prev, u, x)
        print("updated u:" + str(u))

        # Step 5: Convergence check

        if check_convergence(x, z, z_prev, length_of_lanes):

            print(f"Convergence reached after {iteration} iterations.")
            break

    return result

######################################################################################################
# def admm_algorithm(intersected_information,platooning_information, map_to_lane, map_to_vehicle_num):

#     print(intersected_information)

#     # Unpack intersected information
#     (
#         number_of_lane_intersected, 
#         number_of_vehicle_intersected, 
#         v_intersected, 
#         x_intersected, 
#         xr_cons_intersected, 
#         x_pos_intersected, 
#         parameters_intersected, 
#         intersected_list
#     ) = intersected_information

#     # Unpack platooning information
#     (
#         number_of_lane_platooning, 
#         number_of_vehicle_platooning, 
#         v_platooning, 
#         x_platooning, 
#         xr_cons_platooning, 
#         x_pos_platooning, 
#         parameters_platooning, 
#         platooning_list
#     ) = platooning_information

#     # Initialization
#     n_lanes = 4 #constant TO DO: CHECK
#     z = np.zeros(n_lanes+1) # Consensus variable TO DO: can be improved to give average x0 values !!!CHECK FASTER CONVERGE WITH X0

#     # New
#     #z_intersected = np.zeros(number_of_lane_intersected)
#     #z_platooning = np.zeros(number_of_vehicle_platooning)

#     u = np.zeros(n_lanes+1) # Dual variable (Lagrange multipliers)
#     x_local_combined = np.zeros(n_lanes+1)
#     distances_dict = {}
#     xr_dict = {}

#     for iteration in range(MAX_ITER):
#         index = 0
#         # Temporary arrays to store local solutions
#         x_intersected_local = np.zeros(number_of_vehicle_intersected)
#         x_platooning_local = np.zeros(number_of_vehicle_platooning)

#         # Store previous values of consensus variables for dual residual calculation
#         z_prev = np.copy(z)

#         #TO DO: Do we need to reset idx ? If not we need to hold idx after intersected list to not overwright the values in platooning 
#         # Step 1: Local optimization for intersected group (each vehicle)# Perform local optimization for intersected vehicles, we are sending whole intersected cars because they depent on each others.
#         if number_of_vehicle_intersected != 0:
#             x_intersected_local = intersected_optimization(
#                 number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, parameters_intersected, z[index], u[index], distances_dict, xr_dict
#             )

#             x_local_combined[index] = np.average(x_intersected_local)
        
#         if x_local_combined[index] == 0:
#             print("ERROR: Infeasible")
#             break
#         # Step 2: Local optimization for platooning group (each vehicle)

#         for lane_number in range(1, number_of_lane_platooning + 1):

#             index += 1

#             # Collect vehicle indices for the current lane
#             vehicles_in_lane = [
#                 vehicle_id for vehicle_id in platooning_list if map_to_lane[vehicle_id] == lane_number
#             ]

#             # Check if there are any vehicles in this lane
#             if not vehicles_in_lane:
#                 continue  # Skip if no vehicles are found in the current lane

#             # Extract data for all vehicles in this lane
#             v_lane = {}
#             x_lane = {}
#             xr_lane = {}
#             x_pos_lane = {}

#             # Populate the lane-specific data structures
#             for vehicle_id in enumerate(vehicles_in_lane):
#                 vehicle_index = map_to_vehicle_num[vehicle_id[1]]

#                 # Fill lane-specific data dictionaries
#                 v_lane[(lane_number, vehicle_index)] = v_platooning.get((lane_number, vehicle_index), 0)
#                 x_lane[(lane_number, vehicle_index)] = x_platooning.get((lane_number, vehicle_index), 0)
#                 xr_lane[(lane_number, vehicle_index)] = xr_cons_platooning.get((lane_number, vehicle_index), 0)
#                 x_pos_lane[(lane_number, vehicle_index)] = x_pos_platooning.get((lane_number, vehicle_index), 0)
#             # Perform optimization for all vehicles in the current lane
#             if len(vehicles_in_lane) != 0:
#                 print(vehicles_in_lane)
#                 print(xr_lane[(lane_number, vehicle_index)])
#                 print(lane_number)
#                 print(vehicle_index)
#                 # TO DO: WE ARE HERE!!! When we check the lane by lane there is a problem like: We want to optimize (3,1) but there is Xcons value for (1,1) as well 
#                 print("lane_number",lane_number)
#                 print("len(vehicles_in_lane)",len(vehicles_in_lane))
#                 print("vehicles_in_lane",vehicles_in_lane)
#                 print("v_lane",v_lane)
#                 print("x_lane",x_lane)
#                 print("xr_lane",xr_lane)
#                 print("x_pos_lane",x_pos_lane)
#                 print("parameters_platooning",parameters_platooning)
#                 x_platooning_local = platooning_optimization(
#                     lane_number, 
#                     len(vehicles_in_lane), 
#                     v_lane, 
#                     x_lane, 
#                     xr_lane, 
#                     parameters_platooning, 
#                     z[index], 
#                     u[index], 
#                     distances_dict,
#                     xr_dict
#                 )

#                 # Update the results for each vehicle in this lane
#                 x_local_combined[index] = np.average(x_platooning_local)
                
#         # Step 3: Consensus step (The division by 2 ensures the consensus is the average of the primal and dual updates.)
#         #TO DO: we are not sure, they are solving together but their u's and z's different so it can be N but they are consensused in each other during solving, therefore we are having 5 z and u values 
#         z = (x_local_combined + u / RHO) / (n_lanes+1) #TO DO: we can need to have summation to sum whole values of array CHECK!!!!standard practice typically divides by 2, balancing primal and dual variables equally.!!!

#         # Step 4: Update dual variables
#         u = u + RHO * (x_local_combined - z)

#         # Step 5: Convergence check
#         if check_convergence(x_local_combined, z, z_prev):

#             print(f"Convergence reached after {iteration} iterations.")
#             break

#     return x_intersected_local, x_platooning_local