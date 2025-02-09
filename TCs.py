import traci

#Case 1: Uncontrolled -> Speed Mode 32 -> OPT False SUMO False TL False -> Crash Low Time
#Case 2: Sumo         -> Speed Mode 24 -> OPT False SUMO True TL False  -> High Fuel Low Crash High Time
#Case 3: Sumo Row     -> Speed Mode 31 -> OPT False SUMO True TL True   -> High Fuel Low Crash High Time
#Case 4: Cent Opt     -> Speed Mode 32 -> OPT True SUMO True TL False   -> No Crash Average Fuel Low Time


def uncontrolled_case_TC1(step):
    print("Uncontrolled TC-1")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1004", "step": 1, "speed": 2.5},
        {"id": "1007", "step": 1, "speed": 2.6},
        {"id": "1002", "step": 1, "speed": 2.4},
        {"id": "2004", "step": 1, "speed": 2.5},
        {"id": "2007", "step": 1, "speed": 2.55},
        {"id": "2002", "step": 1, "speed": 2.45},
        {"id": "1005", "step": 3, "speed": 4.0},
        {"id": "1008", "step": 3, "speed": 5.0},
        {"id": "1003", "step": 3, "speed": 6.0},
        {"id": "2005", "step": 3, "speed": 2.5},
        {"id": "2008", "step": 3, "speed": 2.9},
        {"id": "2003", "step": 3, "speed": 2.5},
        {"id": "1006", "step": 5, "speed": 2.5},
        {"id": "1009", "step": 5, "speed": 2.5},
        {"id": "1001", "step": 5, "speed": 2.5},
        {"id": "2006", "step": 5, "speed": 2.5},
        {"id": "2009", "step": 5, "speed": 2.5},
        {"id": "2001", "step": 5, "speed": 2.5},
        {"id": "1010", "step": 7, "speed": 2.5},
        {"id": "2010", "step": 7, "speed": 2.5}
    ]
        
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def sumocontrolled_case_TC1(step):
    print("Sumocontrolled TC-1")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1004", "step": 1, "speed": 2.5},
        {"id": "1007", "step": 1, "speed": 2.6},
        {"id": "1002", "step": 1, "speed": 2.4},
        {"id": "2004", "step": 1, "speed": 2.5},
        {"id": "2007", "step": 1, "speed": 2.55},
        {"id": "2002", "step": 1, "speed": 2.45},
        {"id": "1005", "step": 3, "speed": 4.0},
        {"id": "1008", "step": 3, "speed": 5.0},
        {"id": "1003", "step": 3, "speed": 6.0},
        {"id": "2005", "step": 3, "speed": 2.5},
        {"id": "2008", "step": 3, "speed": 2.9},
        {"id": "2003", "step": 3, "speed": 2.5},
        {"id": "1006", "step": 5, "speed": 2.5},
        {"id": "1009", "step": 5, "speed": 2.5},
        {"id": "1001", "step": 5, "speed": 2.5},
        {"id": "2006", "step": 5, "speed": 2.5},
        {"id": "2009", "step": 5, "speed": 2.5},
        {"id": "2001", "step": 5, "speed": 2.5},
        {"id": "1010", "step": 7, "speed": 2.5},
        {"id": "2010", "step": 7, "speed": 2.5}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 24)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)
    

def sumocontrolled_case_TC1_row(step):
    print("Sumocontrolled TC-1 row")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "1004", "step": 1, "speed": 2.5},
        {"id": "1007", "step": 1, "speed": 2.6},
        {"id": "1002", "step": 1, "speed": 2.4},
        {"id": "2004", "step": 1, "speed": 2.5},
        {"id": "2007", "step": 1, "speed": 2.55},
        {"id": "2002", "step": 1, "speed": 2.45},
        {"id": "1005", "step": 3, "speed": 4.0},
        {"id": "1008", "step": 3, "speed": 5.0},
        {"id": "1003", "step": 3, "speed": 6.0},
        {"id": "2005", "step": 3, "speed": 2.5},
        {"id": "2008", "step": 3, "speed": 2.9},
        {"id": "2003", "step": 3, "speed": 2.5},
        {"id": "1006", "step": 5, "speed": 2.5},
        {"id": "1009", "step": 5, "speed": 2.5},
        {"id": "1001", "step": 5, "speed": 2.5},
        {"id": "2006", "step": 5, "speed": 2.5},
        {"id": "2009", "step": 5, "speed": 2.5},
        {"id": "2001", "step": 5, "speed": 2.5},
        {"id": "1010", "step": 7, "speed": 2.5},
        {"id": "2010", "step": 7, "speed": 2.5}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 31)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def uncontrolled_case_TC2(step):
    print("Uncontrolled TC-2")

    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "3001", "step": 1, "speed": 1.575},
        {"id": "3002", "step": 1, "speed": 2.575},
        {"id": "3003", "step": 1, "speed": 2.0},
        {"id": "3004", "step": 1, "speed": 4.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)
    
    

def sumocontrolled_case_TC2(step):
    print("Sumocontrolled TC-2")

    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "3001", "step": 1, "speed": 1.575},
        {"id": "3002", "step": 1, "speed": 2.575},
        {"id": "3003", "step": 1, "speed": 2.0},
        {"id": "3004", "step": 1, "speed": 4.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 24)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def sumocontrolled_case_TC2_row(step):
    print("Sumocontrolled TC-2 row")
    
    # List of vehicle IDs with their respective steps and speeds
    vehicle_list = [
        {"id": "3001", "step": 1, "speed": 1.575},
        {"id": "3002", "step": 1, "speed": 2.575},
        {"id": "3003", "step": 1, "speed": 2.0},
        {"id": "3004", "step": 1, "speed": 4.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 31)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def uncontrolled_case_TC3(step):
    print("Uncontrolled TC-3")
    
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
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
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
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def sumocontrolled_case_TC3(step):
    print("Sumocontrolled TC-3")

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
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
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
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 24)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def sumocontrolled_case_TC3_row(step):
    print("Sumocontrolled TC-3 row")
    
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
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
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
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 31)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def uncontrolled_case_TC4(step):
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
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
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
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def sumocontrolled_case_TC4(step):
    print("sumocontrolled TC-4")
    
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
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
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
            traci.vehicle.setSpeedMode(vehicle["id"], 24)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def sumocontrolled_case_TC4_row(step):
    print("sumocontrolled TC-4 row")
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
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
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
            traci.vehicle.setSpeedMode(vehicle["id"], 31)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)

def uncontrolled_case_TC5(step):
    print("Uncontrolled TC-5")

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
        {"id": "7001", "step": 1, "speed": 3.0},
        {"id": "7008", "step": 1, "speed": 3.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0},
        {"id": "6005", "step": 2, "speed": 4.0},
        {"id": "6006", "step": 2, "speed": 2.0},
        {"id": "6007", "step": 2, "speed": 4.0},
        {"id": "6008", "step": 2, "speed": 4.0},
        {"id": "7002", "step": 2, "speed": 2.0},
        {"id": "7009", "step": 2, "speed": 3.5},
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "7003", "step": 3, "speed": 3.0},
        {"id": "7010", "step": 3, "speed": 3.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
        {"id": "7004", "step": 4, "speed": 3.0},
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
        {"id": "7006", "step": 6, "speed": 3.0},
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0},
        {"id": "7007", "step": 7, "speed": 3.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 32)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)


def uncontrolled_case_TC5_TL(step):
    print("Uncontrolled TC-5 TL")
    #intersection_1
    if(step==1):
        traci.vehicle.setSpeedMode("3001",24)
        traci.vehicle.setLaneChangeMode("3001", 0)
        #traci.vehicle.setSpeed("3001",1.575)
        traci.vehicle.setSpeedMode("3002",24)
        traci.vehicle.setLaneChangeMode("3002", 0)
        #traci.vehicle.setSpeed("3002",2.575) #Crash for 8 with 1002
        traci.vehicle.setSpeedMode("3003",24)
        traci.vehicle.setLaneChangeMode("3003", 0)
        #traci.vehicle.setSpeed("3003",2)
        traci.vehicle.setSpeedMode("3004",24)
        traci.vehicle.setLaneChangeMode("3004", 0)
        #traci.vehicle.setSpeed("3004",4)
        #series 1000s
        traci.vehicle.setSpeedMode("1004",24)
        traci.vehicle.setLaneChangeMode("1004", 0)
        #traci.vehicle.setSpeed("1004",1.575)
        traci.vehicle.setSpeedMode("1007",24)
        traci.vehicle.setLaneChangeMode("1007", 0)
        #traci.vehicle.setSpeed("1007",2.575) 
        traci.vehicle.setSpeedMode("1002",24)
        traci.vehicle.setLaneChangeMode("1002", 0)
        #traci.vehicle.setSpeed("1002",2)
        #series 2000s
        traci.vehicle.setSpeedMode("2004",24)
        traci.vehicle.setLaneChangeMode("2004", 0)
        #traci.vehicle.setSpeed("2004",4)
        traci.vehicle.setSpeedMode("2007",24)
        traci.vehicle.setLaneChangeMode("2007", 0)
        #traci.vehicle.setSpeed("2007",2)
        traci.vehicle.setSpeedMode("2002",24)
        traci.vehicle.setLaneChangeMode("2002", 0)
        #traci.vehicle.setSpeed("2002",4)
        #TC5
        traci.vehicle.setSpeedMode("7001",24)
        traci.vehicle.setLaneChangeMode("7001", 0)
        #traci.vehicle.setSpeed("7001",3)
        traci.vehicle.setSpeedMode("7008",24)
        traci.vehicle.setLaneChangeMode("7008", 0)
        #traci.vehicle.setSpeed("7008",3)
    elif(step==2):
        traci.vehicle.setSpeedMode("3005",24)
        traci.vehicle.setLaneChangeMode("3005", 0)
        #traci.vehicle.setSpeed("3005",4)
        traci.vehicle.setSpeedMode("3006",24)
        traci.vehicle.setLaneChangeMode("3006", 0)
        #traci.vehicle.setSpeed("3006",2.6)
        traci.vehicle.setSpeedMode("3007",24)
        traci.vehicle.setLaneChangeMode("3007", 0)
        #traci.vehicle.setSpeed("3007",4)
        traci.vehicle.setSpeedMode("3008",24)
        traci.vehicle.setLaneChangeMode("3008", 0)
        #traci.vehicle.setSpeed("3008",4)
        traci.vehicle.setSpeedMode("6005",24)
        traci.vehicle.setLaneChangeMode("6005", 0)
        #traci.vehicle.setSpeed("6005",4)
        traci.vehicle.setSpeedMode("6006",24)
        traci.vehicle.setLaneChangeMode("6006", 0)
        #traci.vehicle.setSpeed("6006",2)
        traci.vehicle.setSpeedMode("6007",24)
        traci.vehicle.setLaneChangeMode("6007", 0)
        #traci.vehicle.setSpeed("6007",4)
        traci.vehicle.setSpeedMode("6008",24)
        traci.vehicle.setLaneChangeMode("6008", 0)
        #traci.vehicle.setSpeed("6008",4)
        #TC5
        traci.vehicle.setSpeedMode("7002",24)
        traci.vehicle.setLaneChangeMode("7002", 0)
        #traci.vehicle.setSpeed("7002",2)
        traci.vehicle.setSpeedMode("7009",24)
        traci.vehicle.setLaneChangeMode("7009", 0)
        #traci.vehicle.setSpeed("7009",3.5)
    #intersection_2
    elif(step==3):
        traci.vehicle.setSpeedMode("4005",24)
        traci.vehicle.setLaneChangeMode("4005", 0)
        #traci.vehicle.setSpeed("4005",4)
        traci.vehicle.setSpeedMode("4006",24)
        traci.vehicle.setLaneChangeMode("4006", 0)
        #traci.vehicle.setSpeed("4006",5)
        traci.vehicle.setSpeedMode("4007",24)
        traci.vehicle.setLaneChangeMode("4007", 0)
        #traci.vehicle.setSpeed("4007",6)
        traci.vehicle.setSpeedMode("4008",24)
        traci.vehicle.setLaneChangeMode("4008", 0)
        #traci.vehicle.setSpeed("4008",2.5)
        traci.vehicle.setSpeedMode("4009",24)
        traci.vehicle.setLaneChangeMode("4009", 0)
        #traci.vehicle.setSpeed("4009",2.9)
        traci.vehicle.setSpeedMode("4010",24)
        traci.vehicle.setLaneChangeMode("4010", 0)
        #traci.vehicle.setSpeed("4010",2.5)
        #series 1000s
        traci.vehicle.setSpeedMode("1005",24)
        traci.vehicle.setLaneChangeMode("1005", 0)
        #traci.vehicle.setSpeed("1005",1.575)
        traci.vehicle.setSpeedMode("1008",24)
        traci.vehicle.setLaneChangeMode("1008", 0)
        #traci.vehicle.setSpeed("1008",2.575) 
        traci.vehicle.setSpeedMode("1003",24)
        traci.vehicle.setLaneChangeMode("1003", 0)
        #traci.vehicle.setSpeed("1003",2)
        #series 2000s
        traci.vehicle.setSpeedMode("2005",24)
        traci.vehicle.setLaneChangeMode("2005", 0)
        #traci.vehicle.setSpeed("2005",4)
        traci.vehicle.setSpeedMode("2008",24)
        traci.vehicle.setLaneChangeMode("2008", 0)
        #traci.vehicle.setSpeed("2008",2)
        traci.vehicle.setSpeedMode("2003",24)
        traci.vehicle.setLaneChangeMode("2003", 0)
        #traci.vehicle.setSpeed("2003",2)
        #TC5
        traci.vehicle.setSpeedMode("7003",24)
        traci.vehicle.setLaneChangeMode("7003", 0)
        #traci.vehicle.setSpeed("7003",3)
        traci.vehicle.setSpeedMode("7010",24)
        traci.vehicle.setLaneChangeMode("7010", 0)
        #traci.vehicle.setSpeed("7010",3)
    elif(step==4):
        traci.vehicle.setSpeedMode("4001",24)
        traci.vehicle.setLaneChangeMode("4001", 0)
        #traci.vehicle.setSpeed("4001",2.5)
        traci.vehicle.setSpeedMode("4002",24)
        traci.vehicle.setLaneChangeMode("4002", 0)
        #traci.vehicle.setSpeed("4002",2.5)
        traci.vehicle.setSpeedMode("4003",24)
        traci.vehicle.setLaneChangeMode("4003", 0)
        #traci.vehicle.setSpeed("4003",2.5)
        traci.vehicle.setSpeedMode("4004",24)
        traci.vehicle.setLaneChangeMode("4004", 0)
        #traci.vehicle.setSpeed("4004",2.5)
        #TC5
        traci.vehicle.setSpeedMode("7004",24)
        traci.vehicle.setLaneChangeMode("7004", 0)
        #traci.vehicle.setSpeed("7004",3)
    #intersection_4
    elif(step==5):
        traci.vehicle.setSpeedMode("5001",24)
        traci.vehicle.setLaneChangeMode("5001", 0)
        #traci.vehicle.setSpeed("5001",2.5)
        traci.vehicle.setSpeedMode("5002",24)
        traci.vehicle.setLaneChangeMode("5002", 0)
        #traci.vehicle.setSpeed("5002",2.5)
        traci.vehicle.setSpeedMode("5003",24)
        traci.vehicle.setLaneChangeMode("5003", 0)
        #traci.vehicle.setSpeed("5003",2.5)
        traci.vehicle.setSpeedMode("5004",24)
        traci.vehicle.setLaneChangeMode("5004", 0)
        #traci.vehicle.setSpeed("5004",2.5)
        #series 1000s
        traci.vehicle.setSpeedMode("1006",24)
        traci.vehicle.setLaneChangeMode("1006", 0)
        #traci.vehicle.setSpeed("1006",1.575)
        traci.vehicle.setSpeedMode("1009",24)
        traci.vehicle.setLaneChangeMode("1009", 0)
        #traci.vehicle.setSpeed("1009",2.575) 
        traci.vehicle.setSpeedMode("1001",24)
        traci.vehicle.setLaneChangeMode("1001", 0)
        #traci.vehicle.setSpeed("1001",2)
        #series 2000s
        traci.vehicle.setSpeedMode("2006",24)
        traci.vehicle.setLaneChangeMode("2006", 0)
        #traci.vehicle.setSpeed("2006",4)
        traci.vehicle.setSpeedMode("2009",24)
        traci.vehicle.setLaneChangeMode("2009", 0)
        #traci.vehicle.setSpeed("2009",2)
        traci.vehicle.setSpeedMode("2001",24)
        traci.vehicle.setLaneChangeMode("2001", 0)
        #traci.vehicle.setSpeed("2001",4)
        #TC5
        traci.vehicle.setSpeedMode("7005",24)
        traci.vehicle.setLaneChangeMode("7005", 0)
        #traci.vehicle.setSpeed("7005",3)
    elif(step==6):
        traci.vehicle.setSpeedMode("6001",24)
        traci.vehicle.setLaneChangeMode("6001", 0)
        #traci.vehicle.setSpeed("6001",4)
        traci.vehicle.setSpeedMode("6002",24)
        traci.vehicle.setLaneChangeMode("6002", 0)
        #traci.vehicle.setSpeed("6002",2)
        traci.vehicle.setSpeedMode("6003",24)
        traci.vehicle.setLaneChangeMode("6003", 0)
        #traci.vehicle.setSpeed("6003",4)
        traci.vehicle.setSpeedMode("6004",24)
        traci.vehicle.setLaneChangeMode("6004", 0)
        #traci.vehicle.setSpeed("6004",4)
        #TC5
        traci.vehicle.setSpeedMode("7006",24)
        traci.vehicle.setLaneChangeMode("7006", 0)
        #traci.vehicle.setSpeed("7006",3)
    elif(step==7):
        #series 1000s
        traci.vehicle.setSpeedMode("1010",24)
        traci.vehicle.setLaneChangeMode("1010", 0)
        #traci.vehicle.setSpeed("1010",1.575)
        #series 2000s
        traci.vehicle.setSpeedMode("2010",24)
        traci.vehicle.setLaneChangeMode("2010", 0)
        #traci.vehicle.setSpeed("2010",4)
        #TC5
        traci.vehicle.setSpeedMode("7007",24)
        traci.vehicle.setLaneChangeMode("7007", 0)
        #traci.vehicle.setSpeed("7007",3)
    else:
        pass

def sumocontrolled_case_TC5(step):
    print("sumocontrolled TC-5")
    
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
        {"id": "7001", "step": 1, "speed": 3.0},
        {"id": "7008", "step": 1, "speed": 3.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0},
        {"id": "6005", "step": 2, "speed": 4.0},
        {"id": "6006", "step": 2, "speed": 2.0},
        {"id": "6007", "step": 2, "speed": 4.0},
        {"id": "6008", "step": 2, "speed": 4.0},
        {"id": "7002", "step": 2, "speed": 3.0},
        {"id": "7009", "step": 2, "speed": 3.0},
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "7003", "step": 3, "speed": 3.0},
        {"id": "7010", "step": 3, "speed": 3.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
        {"id": "7004", "step": 4, "speed": 3.0},
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
        {"id": "7006", "step": 6, "speed": 3.0},
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0},
        {"id": "7007", "step": 7, "speed": 3.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeedMode(vehicle["id"], 24)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
    

def sumocontrolled_case_TC5_row(step):
    print("sumocontrolled TC-5 row")
    
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
        {"id": "7001", "step": 1, "speed": 3.0},
        {"id": "7008", "step": 1, "speed": 3.0},
        {"id": "3005", "step": 2, "speed": 4.0},
        {"id": "3006", "step": 2, "speed": 2.6},
        {"id": "3007", "step": 2, "speed": 4.0},
        {"id": "3008", "step": 2, "speed": 4.0},
        {"id": "6005", "step": 2, "speed": 4.0},
        {"id": "6006", "step": 2, "speed": 2.0},
        {"id": "6007", "step": 2, "speed": 4.0},
        {"id": "6008", "step": 2, "speed": 4.0},
        {"id": "7002", "step": 2, "speed": 3.0},
        {"id": "7009", "step": 2, "speed": 3.0},
        {"id": "4005", "step": 3, "speed": 4.0},
        {"id": "4006", "step": 3, "speed": 5.0},
        {"id": "4007", "step": 3, "speed": 6.0},
        {"id": "4008", "step": 3, "speed": 2.5},
        {"id": "4009", "step": 3, "speed": 2.9},
        {"id": "4010", "step": 3, "speed": 2.5},
        {"id": "1005", "step": 3, "speed": 1.575},
        {"id": "1008", "step": 3, "speed": 2.575},
        {"id": "1003", "step": 3, "speed": 2.0},
        {"id": "2005", "step": 3, "speed": 4.0},
        {"id": "2008", "step": 3, "speed": 2.0},
        {"id": "2003", "step": 3, "speed": 2.0},
        {"id": "7003", "step": 3, "speed": 3.0},
        {"id": "7010", "step": 3, "speed": 3.0},
        {"id": "4001", "step": 4, "speed": 2.5},
        {"id": "4002", "step": 4, "speed": 2.5},
        {"id": "4003", "step": 4, "speed": 2.5},
        {"id": "4004", "step": 4, "speed": 2.5},
        {"id": "7004", "step": 4, "speed": 3.0},
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
        {"id": "7006", "step": 6, "speed": 3.0},
        {"id": "1010", "step": 7, "speed": 1.575},
        {"id": "2010", "step": 7, "speed": 4.0},
        {"id": "7007", "step": 7, "speed": 3.0}
    ]
    
    # Process vehicles for the current step
    for vehicle in vehicle_list:
        if vehicle["step"] == step:
            traci.vehicle.setSpeed(vehicle["id"], vehicle["speed"])
            traci.vehicle.setSpeedMode(vehicle["id"], 31)
            traci.vehicle.setLaneChangeMode(vehicle["id"], 0)
    