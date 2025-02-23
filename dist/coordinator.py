import cvxpy as cp
import numpy as np
from dist.intersected import intersected_optimization
from dist.platooning import platooning_optimization
from dist.simulator import *

#(number_of_lane, number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, parameters)

# Consensus ADMM parameters
MAX_ITER = 1000
RHO = 1.0
TOLERANCE = 1e-4

# Function to check convergence
def check_convergence(x_local_combined, z, z_prev_intersected, z_prev_platooning):
    """Convergence check based on primal and dual residuals."""
    # Compute primal residuals
    primal_residual = np.linalg.norm(x_local_combined - z)
    
    # Compute dual residuals using the change in consensus variables
    dual_residual = RHO * np.linalg.norm(z - z_prev)

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
                number_of_lane_intersected, number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, parameters_intersected, z[index], u[index], RHO, distances_dict, xr_dict
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
                    x_pos_lane, 
                    parameters_platooning, 
                    z[index], 
                    u[index], 
                    RHO,
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

    z_intersected = np.zeros(number_of_vehicle_intersected) #Consensus for intersected
    u_local_intersected = np.zeros(number_of_vehicle_intersected)
    
    z_platooning = np.zeros(number_of_vehicle_platooning) #Consensus for platooning
    u_local_platooning = np.zeros(number_of_vehicle_platooning)

    x_local_combined = np.zeros(number_of_vehicle_intersected+number_of_vehicle_platooning)

    distances_dict = {}
    xr_dict = {}

    for iteration in range(MAX_ITER):
        index = 0
        # Temporary arrays to store local solutions
        x_intersected_local = np.zeros(number_of_vehicle_intersected)
        x_platooning_local = np.zeros(number_of_vehicle_platooning)

        # Store previous values of consensus variables for dual residual calculation
        z_prev_intersected = np.copy(z_intersected)
        z_prev_platooning = np.copy(z_platooning)

        # Collect vehicle indices for the intersection
        vehicles_in_inter = [
            vehicle_id for vehicle_id in intersected_list
        ]

        # Check if there are any vehicles in the intersection
        if not vehicles_in_inter:
            continue  # Skip if no vehicles are found in the intersection

        # Extract data for all vehicles in the intersection
        v_inter = {}
        x_inter = {}
        xr_inter = {}
        x_pos_inter = {}

        # Populate the vehicle-specific data structures
        for vehicle_id in enumerate(vehicles_in_inter):
            vehicle_index = map_to_vehicle_num[vehicle_id[1]]

            # Fill vehicle-specific data dictionaries
            v_inter[(lane_number, vehicle_index)] = v_intersected.get((lane_number, vehicle_index), 0)
            x_inter[(lane_number, vehicle_index)] = x_intersected.get((lane_number, vehicle_index), 0)
            xr_inter[(lane_number, vehicle_index)] = xr_cons_intersected.get((lane_number, vehicle_index), 0)
            x_pos_inter[(lane_number, vehicle_index)] = x_pos_intersected.get((lane_number, vehicle_index), 0)
    
        #TO DO: Do we need to reset idx ? If not we need to hold idx after intersected list to not overwright the values in platooning 
        # Step 1: Local optimization for intersected group (each vehicle)# Perform local optimization for intersected vehicles, we are sending whole intersected cars because they depent on each others.
        for lane_number in range(1, number_of_vehicle_intersected + 1):
            #TO DO: Adding one constraint for z; returning z,u and x_local values and also a value to map x_local values; change optimization for one car; optimization will be called for a thread
            #TO DO: x_local >= z + u xlocal = (Xl^t+1 - Fl)=zl (X^t+1 -Fm)=zm -> Clarify it
            x_intersected_local = intersected_optimization(
                number_of_lane_intersected, number_of_vehicle_intersected, v_inter, x_inter, xr_inter, x_pos_inter, parameters_intersected, z_intersected[index], u_local_intersected[index], RHO, distances_dict, xr_dict
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
                #TO DO: Adding one constraint for z; returning z,u and x_local values and also a value to map x_local values; change optimization for one car; optimization will be called for a thread
                #TO DO: x_local >= z + u xlocal = (Xl^t+1 - Xm^t+1)=zl (Xm^t+1 -Xn^t+1)=zm -> Clarify it
                x_platooning_local = platooning_optimization(
                    lane_number, 
                    len(vehicles_in_lane), 
                    v_lane, 
                    x_lane, 
                    xr_lane, 
                    x_pos_lane, 
                    parameters_platooning, 
                    z[index], 
                    u[index], 
                    RHO,
                    distances_dict,
                    xr_dict
                )

                # Update the results for each vehicle in this lane
                x_local_combined[index] = np.average(x_platooning_local)
                
        # Step 3: Consensus step (The division by 2 ensures the consensus is the average of the primal and dual updates.)
        #TO DO: we are not sure, they are solving together but their u's and z's different so it can be N but they are consensused in each other during solving, therefore we are having 5 z and u values 
        #TO DO: it will be change for other cars like max()
        #TO DO: it will be change for platooning like taking average        
        z = (x_local_combined + u / RHO) / (n_lanes+1) #TO DO: we can need to have summation to sum whole values of array CHECK!!!!standard practice typically divides by 2, balancing primal and dual variables equally.!!!

        # Step 4: Update dual variables
        #TO DO: It should be for whole car's u value
        u = u + RHO * (x_local_combined - z)

        # Step 5: Convergence check
        #TO DO: It will be updated
        if check_convergence(x_local_combined, z, z_prev_intersected, z_prev_platooning):

            print(f"Convergence reached after {iteration} iterations.")
            break

    return x_intersected_local, x_platooning_local