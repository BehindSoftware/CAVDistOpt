import traci

#Case 1: Uncontrolled -> Speed Mode 32 -> OPT False SUMO False TL False -> Crash Low Time
#Case 2: Sumo         -> Speed Mode 24 -> OPT False SUMO True TL False  -> High Fuel Low Crash High Time
#Case 3: Sumo Row     -> Speed Mode 31 -> OPT False SUMO True TL True   -> High Fuel Low Crash High Time
#Case 4: Cent Opt     -> Speed Mode 32 -> OPT True SUMO True TL False   -> No Crash Average Fuel Low Time


def uncontrolled_case_TC1_dist(step):
    print("Uncontrolled TC-1")
    
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
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

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
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)
    

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
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)