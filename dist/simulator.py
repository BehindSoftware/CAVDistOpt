import traci
import time

DIST_OPT=True
#from veh_opt import get_parameters_on_the_intersection, create_the_inputs, set_optimized_acceleration
if(DIST_OPT==False):
    from opt_lib import get_optimized_acceleration
else:
    from dist_opt import get_optimized_acceleration
from test import uncontrolled_case, test_case_four
from dist.platooning import platooning_optimization
from dist.intersected import intersected_optimization
from dist.coordinator import consensus_admm_algorithm #,admm_algorithm
from TCs import uncontrolled_case_TC1, uncontrolled_case_TC2, uncontrolled_case_TC3, uncontrolled_case_TC4, uncontrolled_case_TC5
from TCs_dist import uncontrolled_case_TC1_dist, uncontrolled_case_TC2_dist, uncontrolled_case_TC3_dist, uncontrolled_case_TC4_dist

map_to_lane = {}
map_to_vehicle_num = {}

#DESC SORT: Sorting the cars in array
def sortSecond(val):
    return val[1]

def get_sorted_vehicle_positions(detector_cars, vehicle_list_in_scenario):
    vehicle_positions = [(vehicle, traci.vehicle.getLanePosition(vehicle)) for vehicle in detector_cars if vehicle in vehicle_list_in_scenario]

    # Sort the list of tuples by the position
    vehicle_positions.sort(key=sortSecond,reverse=True)

    vehicle_ids = [vehicle for vehicle, position in vehicle_positions]
    return vehicle_ids
#DESC SORT: END

#DESC CAL: Xr calculation
def calculate_desired_route(vehicle_id):
    # Calculate the total distance
    total_distance = 0
    # Retrieve the route for the vehicle
    route_edges = traci.vehicle.getRoute(vehicle_id)

    for edge in route_edges:
        edge_length = traci.lane.getLength(edge + "_0")  # Assuming single lane
        total_distance += edge_length
    
    #TO DO: Add junction with test a junction length checking dif traveled vs. odyometer
    #print(f"Total distance for vehicle {vehicle_id}: {total_distance} meters")
    return total_distance
#DESC CAL: END

#DESC FILL: Fills arrays for optimization
def create_the_inputs(number_of_lane, number_of_vehicle, v, x, xr_cons, x_pos):
    for i in range(5): #number_of_lane+1
        for j in range(number_of_vehicle+1):
            if not((i==0 or j==0)):
                if (i,j) in xr_cons:
                    pass
                else:
                    v[i,j] = 0
                    x[i,j] = 0
                    xr_cons[i,j] = 0
                    x_pos[i,j] = 0

    # print("v",v)
    # print("x",x)
    # print("xr",xr_cons)
    # print("x_pos",x_pos)
    return number_of_lane, number_of_vehicle, v, x, xr_cons, x_pos
#DESC FILL: END

#DESC SET_OPT_FOR_CENT : Set optimized acceleration for centralized optimization
def set_optimized_acceleration(number_of_lane, number_of_vehicle, detected_list, acceleration, step):
    vehicle_list_in_scenario = traci.vehicle.getIDList()
    
    if(bool(acceleration)):
        for vehicle in detected_list:
            if vehicle in vehicle_list_in_scenario: #Adding for traci.exceptions.TraCIException: Vehicle 'XXX' is not known.
                calculated_speed = traci.vehicle.getSpeed(vehicle)+acceleration[map_to_lane[vehicle],map_to_vehicle_num[vehicle]]*1 #t=1
                if(calculated_speed>=0):
                    traci.vehicle.setSpeed(vehicle,calculated_speed)
                else:
                    traci.vehicle.setSpeed(j, -1)
                    traci.vehicle.setSpeedMode(vehicle, 31)
                    traci.vehicle.setLaneChangeMode(vehicle, 512)
                # #FOR TEST
                # if(step==8):
                #     traci.vehicle.setSpeed('3005',22.22)
#DESC SET_OPT_FOR_CENT : END

#DESC SET_OPT_FOR_DIST : Set optimized acceleration for distributed optimization
def get_vehicle_position(vehicle_id, ids_for_result):
    for lane_index, lane_array in enumerate(ids_for_result):
        for position_tuple in lane_array:
            if position_tuple[1] == vehicle_id:
                return (lane_index, position_tuple[0])  # (lane, vehicle_index)
    return (-1, -1)  # Not found

def set_dist_acceleration(number_of_lane, detected_list, result, ids_for_result, step):
    vehicle_list_in_scenario = traci.vehicle.getIDList()
    t = 1 #TO DO: hardcoded, it should be changed after all
    if result is not None and any(len(r) > 0 for r in result):
        for vehicle in detected_list:
            if vehicle in vehicle_list_in_scenario: #Adding for traci.exceptions.TraCIException: Vehicle 'XXX' is not known.
                lane_index, vehicle_index = get_vehicle_position(vehicle, ids_for_result)
                if(result[lane_index][vehicle_index]!=-1):
                    calculated_speed = traci.vehicle.getSpeed(vehicle)+result[lane_index][vehicle_index]*t #t=1
                    print(f"Step {step} | Vehicle ID: {vehicle} | Before speed: {traci.vehicle.getSpeed(vehicle):.2f} m/s | "
                            f"Acceleration: {result[lane_index][vehicle_index]:.2f} m/s² | New speed: {calculated_speed:.2f} m/s")
                    traci.vehicle.setSpeed(vehicle,calculated_speed)
                else:
                    traci.vehicle.setSpeed(j, -1)
                    traci.vehicle.setSpeedMode(vehicle, 31)
                    traci.vehicle.setLaneChangeMode(vehicle, 512)

                # #FOR TEST
                # if(step==8):
                #     traci.vehicle.setSpeed('3005',22.22)
#DESC SET_OPT_FOR_DIST : END

#DESC OPTIMIZATION: Optimization phase is calling for each step
def optimized_case(step,parameters):
    #Not optimization for add vehicles to scenario
    if(step<6): #8 for uncontrolled case (Clarify value according to catch cars however they are created)
        #uncontrolled_case(step)
        #test_case_four(step)
        #uncontrolled_case_TC1(step)
        #uncontrolled_case_TC2(step)
        #uncontrolled_case_TC3(step)
        #uncontrolled_case_TC4(step)
        #uncontrolled_case_TC5(step)
        #uncontrolled_case_TC1_dist(step)
        parameters.append(uncontrolled_case_TC3_dist(step)) #Vehicle numbers
        #uncontrolled_case_TC3_dist(step)
        #uncontrolled_case_TC4_dist(step)
        print("Optimized case has been activated.")
        return

    #Initialization step
    if(DIST_OPT==False):
        v = {}
        x = {}
        xr_cons = {}
        x_pos = {}
        length_of_lanes = [0,0,0,0,0]
        number_of_vehicle_intersected = 0
        number_of_vehicle_platooning = 0
    else:
        #Reset values for next step
        intersected_list = []
        platooning_list = []
        intersected_information = []
        platooning_information = []
        length_of_lanes = [0,0,0,0,0]
        number_of_vehicle_intersected = 0
        number_of_vehicle_platooning = 0
        number_of_lane = 0
        v_intersected = {}
        x_intersected = {}
        xr_cons_intersected = {}
        x_pos_intersected = {}
        v_platooning = {}
        x_platooning = {}
        xr_cons_platooning = {}
        x_pos_platoning = {}
        intersection_circle = 425 #Determines intersected and platooning cars
    number_of_vehicle = 0
    detected_list = []

    vehicle_list_in_scenario = traci.vehicle.getIDList() #take optimization parameters of the vehicles on the induction (Check there is a car on the intersection(induction loop))
    for j in vehicle_list_in_scenario:
        print("Vehicle {} speed: {}".format(j,traci.vehicle.getSpeed(j)))
        traci.vehicle.setSpeed(j, -1)
        traci.vehicle.setSpeedMode(j,31) #Take control about speed (not sure 0 or 32 but not 31)
        traci.vehicle.setLaneChangeMode(j, 512) #Take control about lanechange

    #Gathering information step 
    for intersection_number in range(0,(parameters[12])): #parameters[12] comes from map creation
        #print("Intersection Number:{}".format(intersection_number))
        #each lane of an intersection
        for lane_number in range(1,5): #Lane 1,2,3,4 clockwise (***Lane designed as constant 4***)
            number_of_vehicle_platooning = 0
            thereisflag = False
            vehicle_index = 1 #Should be reset for each lane
            detector_cars = [item[0] for item in traci.inductionloop.getVehicleData(str(lane_number+(intersection_number*8)))]
            detector_cars = get_sorted_vehicle_positions(detector_cars, vehicle_list_in_scenario)
            if len(detector_cars) > 0:
                print("Sorted detector cars:",detector_cars) 
                for vehicle_on_lane in detector_cars: #For each car in the same lane
                    if vehicle_on_lane in vehicle_list_in_scenario: #The car is still in the simulation
                        #print("Vehicle on lane {}:".format(lane_number) + vehicle_on_lane)
                        detected_list.append(vehicle_on_lane) #For holding vehicle number
                        if(DIST_OPT==True):
                            if(traci.vehicle.getLanePosition(vehicle_on_lane)>intersection_circle):
                                return
                        traci.vehicle.setSpeedMode(vehicle_on_lane,32) #Take control about speed (not sure 0 or 32 but not 31)
                        traci.vehicle.setLaneChangeMode(vehicle_on_lane, 0) #Take control about lanechange
                        if(DIST_OPT==False):
                            v[lane_number,vehicle_index] = traci.vehicle.getSpeed(vehicle_on_lane) #Take v0
                            x_pos[lane_number,vehicle_index] = traci.vehicle.getLanePosition(vehicle_on_lane) #Take position for safety cons.
                            x[lane_number,vehicle_index] = traci.vehicle.getDistance(vehicle_on_lane) #odyometer for traveled distance
                            xr_cons[lane_number,vehicle_index] = calculate_desired_route(vehicle_on_lane) #Take Xr
                            map_to_lane[vehicle_on_lane] = lane_number #Assign lane number to use at set_optimized_acceleration
                            map_to_vehicle_num[vehicle_on_lane] = vehicle_index
                        else:
                            if(vehicle_index==1) and (traci.vehicle.getLanePosition(vehicle_on_lane)>intersection_circle):
                                intersected_list.append(vehicle_on_lane)
                                v_intersected[lane_number,vehicle_index] = traci.vehicle.getSpeed(vehicle_on_lane) #Take v0
                                x_intersected[lane_number,vehicle_index] = traci.vehicle.getDistance(vehicle_on_lane) #odyometer for traveled distance
                                xr_cons_intersected[lane_number,vehicle_index] = calculate_desired_route(vehicle_on_lane) #Take Xr
                                x_pos_intersected[lane_number,vehicle_index] = traci.vehicle.getLanePosition(vehicle_on_lane)
                                number_of_vehicle_intersected+= 1
                                map_to_lane[vehicle_on_lane] = lane_number #Assign lane number to use at set_optimized_acceleration
                                map_to_vehicle_num[vehicle_on_lane] = vehicle_index
                                thereisflag = True
                            else:
                                platooning_list.append(vehicle_on_lane)
                                if(thereisflag==False):
                                    v_platooning[lane_number,vehicle_index] = traci.vehicle.getSpeed(vehicle_on_lane) #Take v0
                                    x_platooning[lane_number,vehicle_index] = traci.vehicle.getDistance(vehicle_on_lane) #odyometer for traveled distance
                                    xr_cons_platooning[lane_number,vehicle_index] = calculate_desired_route(vehicle_on_lane) #Take Xr
                                    x_pos_platoning[lane_number,vehicle_index] = traci.vehicle.getLanePosition(vehicle_on_lane)
                                    map_to_lane[vehicle_on_lane] = lane_number #Assign lane number to use at set_optimized_acceleration
                                    map_to_vehicle_num[vehicle_on_lane] = vehicle_index
                                else:
                                    v_platooning[lane_number,vehicle_index-1] = traci.vehicle.getSpeed(vehicle_on_lane) #Take v0
                                    x_platooning[lane_number,vehicle_index-1] = traci.vehicle.getDistance(vehicle_on_lane) #odyometer for traveled distance
                                    xr_cons_platooning[lane_number,vehicle_index-1] = calculate_desired_route(vehicle_on_lane) #Take Xr
                                    x_pos_platoning[lane_number,vehicle_index-1] = traci.vehicle.getLanePosition(vehicle_on_lane)
                                    map_to_lane[vehicle_on_lane] = lane_number #Assign lane number to use at set_optimized_acceleration
                                    map_to_vehicle_num[vehicle_on_lane] = vehicle_index-1
                                number_of_vehicle_platooning+= 1
                        number_of_vehicle+= 1 
                        #number_of_lane = lane_number #last lane ID which has a car (comment out because it is using as a constant)
                        vehicle_index+= 1 #vehicle ID in the same lane
                        #number_of_vehicle+= 1
                    else:
                        #print("The car on this lane is no more exist")
                        pass
            else:
                #print("There is no vehicle in this induction loop:",str(lane_number))
                pass
            length_of_lanes[0] = number_of_vehicle_intersected
            length_of_lanes[lane_number] = number_of_vehicle_platooning

        number_of_lane = 4 #TO DO: Assumed there is 4 lanes for each intersections
        #print("lane:{} vehicle:{}".format(number_of_lane,number_of_vehicle))
        #print("intersection:{} vehicle_list:{}".format(intersection_number,detected_list))
        if(number_of_vehicle!=0):
            print("*Summarize* intersection:{}, total_vehicle_number:{}".format(intersection_number,number_of_vehicle))
        for lane in range(0,5):
            print("lane:{}length_of_lanes:{}".format(lane,length_of_lanes[lane]))

        #Calling Optimization Step
        if(DIST_OPT==False):
            number_of_lane, number_of_vehicle, v, x, xr_cons, x_pos = create_the_inputs(number_of_lane, number_of_vehicle, v, x, xr_cons, x_pos)
        else:
            number_of_lane, number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected = create_the_inputs(number_of_lane, number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected)
            number_of_lane, number_of_vehicle_platooning, v_platooning, x_platooning, xr_cons_platooning, x_pos_platoning = create_the_inputs(number_of_lane, number_of_vehicle_platooning, v_platooning, x_platooning, xr_cons_platooning, x_pos_platoning)
        if(number_of_vehicle>0):
            if(DIST_OPT==False):
                start = time.perf_counter()
                acceleration = get_optimized_acceleration(number_of_lane, number_of_vehicle, v, x, xr_cons, x_pos, parameters)
                end = time.perf_counter()
                elapsed_ms = (end - start) * 1000  # milisaniye
                with open("süreler_cent.txt", "a", encoding="utf-8") as f:
                    f.write(f"süresi: {elapsed_ms:.2f} ms\n")
                
                print(acceleration)
                set_optimized_acceleration(number_of_lane, number_of_vehicle, detected_list, acceleration, step)
            else:
                intersected_information.extend([number_of_lane, number_of_vehicle_intersected, v_intersected, x_intersected, xr_cons_intersected, x_pos_intersected, parameters, intersected_list])
                platooning_information.extend([number_of_lane, number_of_vehicle_platooning, v_platooning, x_platooning, xr_cons_platooning, x_pos_platoning, parameters, platooning_list])
                result, ids_for_result = consensus_admm_algorithm(intersected_information,platooning_information, map_to_lane, map_to_vehicle_num, length_of_lanes)
                set_dist_acceleration(number_of_lane, detected_list, result, ids_for_result, step)
        
        #Resetting Step
        if(DIST_OPT==False):
            v = {}
            x = {}
            xr_cons = {}
            x_pos = {}
        else:
            v_platooning = {}
            x_platooning = {}
            xr_cons_platooning = {}
            x_pos_platoning = {}
            v_intersected = {}
            x_intersected = {}
            xr_cons_intersected = {}
            x_pos_intersected = {}
            intersected_list = []
            platooning_list = []
            intersected_information.clear()
            platooning_information.clear()

        detected_list = []
        number_of_vehicle = 0
        number_of_vehicle_intersected = 0
        number_of_vehicle_platooning = 0
        vehicle_list_in_scenario = traci.vehicle.getIDList()
        number_of_lane = 0
    pass
#DESC OPTIMIZATION: END