import cvxpy as cp
import numpy as np
from dist.intersected import intersected_optimization, parsing_vehicle_data
from dist.platooning import platooning_optimization, parsing_vehicle_data_platooning
from dist.simulator import *

#DESC CONF: Consensus ADMM parameters
WEIGHTED_AVERAGE_CONSENSUS_ACTIVE = False

MAX_ITER = 5
RHO = 1
TOLERANCE = 7.5 #Determine according to sensitivity (A car distance to other/intersection can be about 7.5(min gap+car_len))
TIME_GAP = 0.8
#DESC CONF: END

#DESC CONV CRIT: Function to check convergence
def check_convergence(x, z_new, z_prev, length_of_lanes):
    """Convergence check based on primal and dual residuals."""
    # Initialize residuals
    primal_residual_sum = 0
    dual_residual_sum = 0

    # Compute residuals for each lane
    for lane_number in range(len(length_of_lanes)):
        
        # Compute primal residuals for the current lane
        diff = x[lane_number] - z_new[lane_number]
        mask = x[lane_number] != -1
        primal_residual_sum += np.linalg.norm(diff[mask])
        #print(primal_residual_sum)

        # Compute dual residuals for the current lane using the change in consensus variables
        diff2 = z_new[lane_number] - z_prev[lane_number]
        mask2 = x[lane_number] != -1
        dual_residual_sum += np.linalg.norm(diff2[mask2])
        #print(dual_residual_sum)

    # Compute overall residuals
    primal_residual = primal_residual_sum
    dual_residual = RHO * dual_residual_sum

    print(primal_residual, dual_residual)

    # Check convergence
    return (primal_residual < TOLERANCE) and (dual_residual < TOLERANCE)
#DESC CONV CRIT: END

#DESC PREP INTER: Intersected cars data preparation -> Init z values
def prepare_data(intersected_list, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, map_to_lane, map_to_vehicle_num, number_of_vehicle, ids_for_result, iteration, z):
    
    # Extract data for all vehicles in the intersection
    v_inter = {}
    x_inter = {}
    xr_inter = {}
    x_pos_inter = {}
    consensus_idx = 0

    # Collect vehicle indices for the intersection
    vehicles_in_inter = [vehicle_id for vehicle_id in intersected_list]

    # Check if there are any vehicles in the intersection
    if not vehicles_in_inter:
        print("prepare_data: No car in intersection for whole lanes")
        return v_inter, x_inter, xr_inter, x_pos_inter, number_of_vehicle, ids_for_result# Skip if no vehicles are found in the intersection

    # Populate the vehicle-specific data structures
    for vehicle_id in enumerate(vehicles_in_inter):
        vehicle_index = map_to_vehicle_num[vehicle_id[1]]
        lane_number = map_to_lane[vehicle_id[1]]
        ids_for_result[0][consensus_idx] = vehicle_id

        # Fill vehicle-specific data dictionaries
        v_inter[(lane_number, vehicle_index)] = v_intersected.get((lane_number, vehicle_index), 0)
        x_inter[(lane_number, vehicle_index)] = x_intersected.get((lane_number, vehicle_index), 0)
        xr_inter[(lane_number, vehicle_index)] = xr_cons_intersected.get((lane_number, vehicle_index), 0)
        x_pos_inter[(lane_number, vehicle_index)] = x_pos_intersected.get((lane_number, vehicle_index), 0)

        #HARDCODED!!! z initial set
        F = 495
        if iteration == 0:
            z[0][consensus_idx] = (F - x_inter[(lane_number, vehicle_index)]) / v_inter[(lane_number, vehicle_index)]

        number_of_vehicle += 1
        consensus_idx += 1
    
    return v_inter, x_inter, xr_inter, x_pos_inter, number_of_vehicle, ids_for_result
#DESC PREP INTER: END

#DESC PREP PLAT: Platooning cars data preparation -> Init z values
def prepare_data_platooning(platooning_list,lane_number, v_platooning, x_platooning, xr_cons_platooning, x_pos_platooning, map_to_lane, map_to_vehicle_num, number_of_vehicle, ids_for_result, iteration, z):

    # Extract data for all vehicles in this lane
    v_lane = {}
    x_lane = {}
    xr_lane = {}
    x_pos_lane = {}
    consensus_idx = 0

    # Collect vehicle indices for the current lane
    vehicles_in_lane = [vehicle_id for vehicle_id in platooning_list if map_to_lane[vehicle_id] == lane_number]

    # Check if there are any vehicles in this lane
    if not vehicles_in_lane:
        print("No car in lane: " + str(lane_number))
        return v_lane, x_lane, xr_lane, x_pos_lane, number_of_vehicle, ids_for_result # Skip if no vehicles are found in the current lane

    # Populate the lane-specific data structures
    for vehicle_id in enumerate(vehicles_in_lane):
        vehicle_index = map_to_vehicle_num[vehicle_id[1]]
        ids_for_result[lane_number][consensus_idx] = vehicle_id

        if iteration == 0:
            z[lane_number][consensus_idx] = v_platooning.get((lane_number, vehicle_index), 0)

        # Fill lane-specific data dictionaries
        v_lane[(lane_number, vehicle_index)] = v_platooning.get((lane_number, vehicle_index), 0)
        x_lane[(lane_number, vehicle_index)] = x_platooning.get((lane_number, vehicle_index), 0)
        xr_lane[(lane_number, vehicle_index)] = xr_cons_platooning.get((lane_number, vehicle_index), 0)
        x_pos_lane[(lane_number, vehicle_index)] = x_pos_platooning.get((lane_number, vehicle_index), 0)
        number_of_vehicle += 1
        consensus_idx += 1

    print("prepare_data_platooning: ")
    print(v_lane, x_lane, xr_lane, x_pos_lane)
    return v_lane, x_lane, xr_lane, x_pos_lane, number_of_vehicle, ids_for_result
#DESC PREP PLAT: END

#DESC SORT: Sort for determine slot in intersection
def sort_lanes_by_first_vehicle_position(x):

    lane_positions = {}
    for consensus_idx in range(0,len(x[0])):
        lane_positions[consensus_idx] = x[0][consensus_idx]  # First vehicle in the lane
    
    # Sort lane numbers by first vehicle's x position (ascending)
    sorted_lanes = sorted(lane_positions.items(), key=lambda item: item[1])
    return [consensus_idx for consensus_idx, _ in sorted_lanes]
#DESC SORT: END

#DESC UPDATE CONSENSUS:
def update_consensus(z, u, x, cars_in_lanes, length_of_lanes):

    #Create same structure with z
    z_updated = np.copy(z)

    for lane_number in range(0, 5): # it is constant lane 0= intersection, lane 1,2,3,4 lanes
        if lane_number==0: #for intersection
            first_flag = True
            consensus_idx = 0 #For intersection index 0 z[0], u[0], x[0]
            for consensus_idx in sort_lanes_by_first_vehicle_position(x): #each lane in the intersection lane 1,2,3,4
                if first_flag==True:
                    z_updated[lane_number][consensus_idx] = x[lane_number][consensus_idx] + u[lane_number][consensus_idx] / RHO
                    first_flag = False
                    pre_idx = consensus_idx
                else:
                    #TO DO: It should be checked because it is not correct orientation
                    z_updated[lane_number][consensus_idx] = min(x[lane_number][consensus_idx] + u[lane_number][consensus_idx] / RHO, z_updated[lane_number][pre_idx]) + TIME_GAP
                    pre_idx = consensus_idx
                print(lane_number,consensus_idx,z_updated[lane_number][consensus_idx],x[lane_number][consensus_idx])
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
                    row_average = np.mean(x[lane_number])
                    z_updated[lane_number] = np.full_like(z_updated[lane_number], row_average)

    return z_updated
#DESC UPDATE CONSENSUS: END

#DESC UPDATE DUAL:
def update_dual(z, u, x):

    u_updated = np.copy(u)

    for lane_number in range(0, 5): # it is constant lane 0= intersection, lane 1,2,3,4 lanes
        for idx in range(0,len(u[lane_number])):
            u_updated[lane_number][idx] = u[lane_number][idx] + (x[lane_number][idx] - z[lane_number][idx]) * RHO

    return u_updated
#DESC UPDATE DUAL: END

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
    ids_for_result = np.empty((len(length_of_lanes),), dtype=object)
    for i, length in enumerate(length_of_lanes):
        z[i] = np.zeros(length)
        u[i] = np.zeros(length)
        x[i] = np.zeros(length)
        result[i] = np.zeros(length)
        ids_for_result[i] = np.zeros(length, dtype=object)

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
        print("result:" + str(ids_for_result))

        # Prepare data for intersected cars
        v_inter, x_inter, xr_inter, x_pos_inter, number_of_vehicle, ids_for_result = prepare_data(intersected_list, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, map_to_lane, map_to_vehicle_num, number_of_vehicle, ids_for_result, iteration, z)

        # Step 1: Local optimization for intersected group
        if number_of_vehicle!= 0:
            consensus_idx = 0
            for laneID in range(1, 5): # For lane 1,2,3,4
                #parsing_vehicle_data to take current car data
                number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle, cars_in_lanes = parsing_vehicle_data(4, 0, v_inter, x_inter, xr_inter, x_pos_inter, laneID)

                if cars_in_lanes[laneID] != -1:
                    print("First car of LaneID:"+str(laneID)+ " Consensus_index:"+ str(consensus_idx))
                    lane_has_multiple_cars = number_of_vehicle > 1
                    result[0][consensus_idx], x[0][consensus_idx] = intersected_optimization(number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle, parameters_intersected, z[0][consensus_idx], u[0][consensus_idx], distances_dict, xr_dict, laneID, RHO) #if lane_has_multiple_cars else 0) #Intersected is hold in 0 index
                    print("Accelaration:" + str(result[0][consensus_idx]) + "Local_v:" + str(x[0][consensus_idx]))
                    consensus_idx+=1

        # Step 2: Local optimization for platooning group (each vehicle)
        for laneID in range(1, 5): # For lane 1,2,3,4
            consensus_idx=len(z[laneID])-1 #index starts from 0 so need -1
            number_of_vehicle = 0
            #prepare_data_platooning to take car data which are current lane
            v_lane, x_lane, xr_lane, x_pos_lane, number_of_vehicle, ids_for_result = prepare_data_platooning(platooning_list,laneID, v_platooning, x_platooning, xr_cons_platooning, x_pos_platooning, map_to_lane, map_to_vehicle_num, number_of_vehicle, ids_for_result, iteration, z)

            # Perform optimization for all vehicles in the current lane
            if number_of_vehicle!= 0:
                for idx in reversed(range(1,len(z[laneID])+1)):
                    #parsing_vehicle_data to take current car data
                    number_of_vehicle,v_vehicle, x_vehicle, xrcons_vehicle, xpos_vehicle = parsing_vehicle_data_platooning(laneID, number_of_vehicle, v_lane, x_lane, xr_lane, x_pos_lane, idx)
                    lane_has_multiple_cars = number_of_vehicle > 1
                    result[laneID][consensus_idx], x[laneID][consensus_idx] = platooning_optimization(laneID, number_of_vehicle, v_vehicle, x_vehicle, xrcons_vehicle, parameters_platooning, z[laneID][consensus_idx], u[laneID][consensus_idx], distances_dict, xr_dict, idx, RHO) #if lane_has_multiple_cars else 0)
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

    print(result)
    print(ids_for_result)
    
    return result, ids_for_result