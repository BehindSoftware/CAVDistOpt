import traci

#Case 1: Uncontrolled -> Speed Mode 32 -> OPT False SUMO False TL False -> Crash Low Time
#Case 2: Sumo         -> Speed Mode 24 -> OPT False SUMO True TL False  -> High Fuel Low Crash High Time
#Case 3: Sumo Row     -> Speed Mode 31 -> OPT False SUMO True TL True   -> High Fuel Low Crash High Time
#Case 4: Cent Opt     -> Speed Mode 32 -> OPT True SUMO True TL False   -> No Crash Average Fuel Low Time


def uncontrolled_case_TC1_dist(step):
    print("Uncontrolled TC-1")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1101", "step": 1, "speed": 7.5},
        {"id": "1102", "step": 1, "speed": 7.5},
        {"id": "1103", "step": 1, "speed": 7.5},
        {"id": "1104", "step": 1, "speed": 7.5},
        {"id": "1106", "step": 3, "speed": 4.0},
        {"id": "1108", "step": 3, "speed": 4.0},
        {"id": "1109", "step": 3, "speed": 4.0},
        {"id": "1111", "step": 5, "speed": 2.5},
        {"id": "1114", "step": 5, "speed": 2.5},
        {"id": "1116", "step": 7, "speed": 1.5},
        {"id": "1118", "step": 7, "speed": 1.5}
    ]
        
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 512)
    return len(vehicle_list)

def sumocontrolled_case_TC1_dist(step):
    print("Sumocontrolled TC-1")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1101", "step": 1, "speed": 2.5},
        {"id": "1102", "step": 1, "speed": 2.5},
        {"id": "1103", "step": 1, "speed": 2.5},
        {"id": "1104", "step": 1, "speed": 2.5},
        {"id": "1106", "step": 3, "speed": 4.0},
        {"id": "1108", "step": 3, "speed": 4.0},
        {"id": "1109", "step": 3, "speed": 4.0},
        {"id": "1111", "step": 5, "speed": 3.5},
        {"id": "1114", "step": 5, "speed": 3.5},
        {"id": "1116", "step": 7, "speed": 7.5},
        {"id": "1118", "step": 7, "speed": 7.5}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 24)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 512)
    
    return len(vehicle_list)

def sumocontrolled_case_TC1_row_dist(step):
    print("Sumocontrolled TC-1 row")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1101", "step": 1, "speed": 2.5},
        {"id": "1102", "step": 1, "speed": 2.5},
        {"id": "1103", "step": 1, "speed": 2.5},
        {"id": "1104", "step": 1, "speed": 2.5},
        {"id": "1106", "step": 3, "speed": 4.0},
        {"id": "1108", "step": 3, "speed": 4.0},
        {"id": "1109", "step": 3, "speed": 4.0},
        {"id": "1111", "step": 5, "speed": 3.5},
        {"id": "1114", "step": 5, "speed": 3.5},
        {"id": "1116", "step": 7, "speed": 7.5},
        {"id": "1118", "step": 7, "speed": 7.5}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 31)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 512)

    return len(vehicle_list)

def uncontrolled_case_TC2_dist(step):
    print("Uncontrolled TC-2")

    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "3001", "step": 1, "speed": 2.5},
        {"id": "3002", "step": 1, "speed": 2.575},
        {"id": "3003", "step": 1, "speed": 2.0},
        {"id": "3004", "step": 1, "speed": 4.0},
        {"id": "1004", "step": 1, "speed": 1.575},
        {"id": "1007", "step": 1, "speed": 2.575},
        {"id": "1002", "step": 1, "speed": 2.0},
        {"id": "2004", "step": 1, "speed": 3.0},
        {"id": "2007", "step": 1, "speed": 2.0},
        {"id": "2002", "step": 1, "speed": 3.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "1006", "step": 5, "speed": 1.575},
        {"id": "1009", "step": 5, "speed": 2.575},
        {"id": "1001", "step": 5, "speed": 2.0},
        {"id": "2006", "step": 5, "speed": 4.0},
        {"id": "2009", "step": 5, "speed": 2.0},
        {"id": "2001", "step": 5, "speed": 4.0},
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 512)

    return len(vehicle_list)

def uncontrolled_case_TC3_dist(step):
    print("Uncontrolled TC-3")

    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1004", "step": 1, "speed": 1.575},
        {"id": "1007", "step": 1, "speed": 2.575},
        {"id": "1002", "step": 1, "speed": 2.5},
        {"id": "2004", "step": 1, "speed": 3.0},
        {"id": "2007", "step": 1, "speed": 2.0},
        {"id": "2002", "step": 1, "speed": 3.0},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "1006", "step": 5, "speed": 1.575},
        {"id": "1009", "step": 5, "speed": 2.575},
        {"id": "1001", "step": 5, "speed": 2.0},
        {"id": "2006", "step": 5, "speed": 4.0},
        {"id": "2009", "step": 5, "speed": 2.0},
        {"id": "2001", "step": 5, "speed": 4.0},
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 512)

    return len(vehicle_list)

def uncontrolled_case_TC4_dist(step):
    print("Uncontrolled TC-4")
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "3001", "step": 1, "speed": 1.575},
        {"id": "3002", "step": 1, "speed": 2.575},
        {"id": "3003", "step": 1, "speed": 2.0},
        {"id": "3004", "step": 1, "speed": 4.0},
        {"id": "1004", "step": 1, "speed": 1.575},
        {"id": "1007", "step": 1, "speed": 2.575},
        {"id": "1002", "step": 1, "speed": 2.0},
        {"id": "2004", "step": 1, "speed": 4.0},
        {"id": "2007", "step": 1, "speed": 2.0},
        {"id": "2002", "step": 1, "speed": 4.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0},
        {"id": "6005", "step": 2, "speed": 4.0},
        {"id": "6006", "step": 2, "speed": 2.0},
        {"id": "6007", "step": 2, "speed": 4.0},
        {"id": "6008", "step": 2, "speed": 4.0},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "5001", "step": 5, "speed": 2.5},
        {"id": "5002", "step": 5, "speed": 2.5},
        {"id": "5003", "step": 5, "speed": 2.5},
        {"id": "5004", "step": 5, "speed": 2.5},
        {"id": "1006", "step": 5, "speed": 1.575},
        {"id": "1009", "step": 5, "speed": 2.575},
        {"id": "1001", "step": 5, "speed": 2.0},
        {"id": "2006", "step": 5, "speed": 4.0},
        {"id": "2009", "step": 5, "speed": 2.0},
        {"id": "2001", "step": 5, "speed": 4.0},
        {"id": "6001", "step": 6, "speed": 4.0},
        {"id": "6002", "step": 6, "speed": 2.0},
        {"id": "6003", "step": 6, "speed": 4.0},
        {"id": "6004", "step": 6, "speed": 4.0},
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 512)

    return len(vehicle_list)