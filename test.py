import traci

#There is one junction collision at the intersection between 1002 and 1004, there is also rear collision between 1007 and 1008.
def uncontrolled_case(step):
    print("Uncontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeedMode("1004",32)
        traci.vehicle.setLaneChangeMode("1004", 0)
        traci.vehicle.setSpeed("1004",2.5)
        traci.vehicle.setSpeedMode("1007",32)
        traci.vehicle.setLaneChangeMode("1007", 0)
        traci.vehicle.setSpeed("1007",2.6)
        traci.vehicle.setSpeedMode("1002",32)
        traci.vehicle.setLaneChangeMode("1002", 0)
        traci.vehicle.setSpeed("1002",2.4)
        traci.vehicle.setSpeedMode("2004",32)
        traci.vehicle.setLaneChangeMode("2004", 0)
        traci.vehicle.setSpeed("2004",2.5)
        traci.vehicle.setSpeedMode("2007",32)
        traci.vehicle.setLaneChangeMode("2007", 0)
        traci.vehicle.setSpeed("2007",2.55)
        traci.vehicle.setSpeedMode("2002",32)
        traci.vehicle.setLaneChangeMode("2002", 0)
        traci.vehicle.setSpeed("2002",2.45)
    elif(step==3):
        traci.vehicle.setSpeedMode("1005",32)
        traci.vehicle.setLaneChangeMode("1005", 0)
        traci.vehicle.setSpeed("1005",4)
        traci.vehicle.setSpeedMode("1008",32)
        traci.vehicle.setLaneChangeMode("1008", 0)
        traci.vehicle.setSpeed("1008",5)
        traci.vehicle.setSpeedMode("1003",32)
        traci.vehicle.setLaneChangeMode("1003", 0)
        traci.vehicle.setSpeed("1003",6)
        traci.vehicle.setSpeedMode("2005",32)
        traci.vehicle.setLaneChangeMode("2005", 0)
        traci.vehicle.setSpeed("2005",2.5)
        traci.vehicle.setSpeedMode("2008",32)
        traci.vehicle.setLaneChangeMode("2008", 0)
        traci.vehicle.setSpeed("2008",2.9)
        traci.vehicle.setSpeedMode("2003",32)
        traci.vehicle.setLaneChangeMode("2003", 0)
        traci.vehicle.setSpeed("2003",2.5)
    elif(step==5):
        traci.vehicle.setSpeedMode("1006",32)
        traci.vehicle.setLaneChangeMode("1006", 0)
        traci.vehicle.setSpeed("1006",2.5)
        traci.vehicle.setSpeedMode("1009",32)
        traci.vehicle.setLaneChangeMode("1009", 0)
        traci.vehicle.setSpeed("1009",2.5)
        traci.vehicle.setSpeedMode("1001",32)
        traci.vehicle.setLaneChangeMode("1001", 0)
        traci.vehicle.setSpeed("1001",2.5)
        traci.vehicle.setSpeedMode("2006",32)
        traci.vehicle.setLaneChangeMode("2006", 0)
        traci.vehicle.setSpeed("2006",2.5)
        traci.vehicle.setSpeedMode("2009",32)
        traci.vehicle.setLaneChangeMode("2009", 0)
        traci.vehicle.setSpeed("2009",2.5)
        traci.vehicle.setSpeedMode("2001",32)
        traci.vehicle.setLaneChangeMode("2001", 0)
        traci.vehicle.setSpeed("2001",2.5)
    elif(step==7):
        traci.vehicle.setSpeedMode("1010",32)
        traci.vehicle.setLaneChangeMode("1010", 0)
        traci.vehicle.setSpeed("1010",2.5)
        traci.vehicle.setSpeedMode("2010",32)
        traci.vehicle.setLaneChangeMode("2010", 0)
        traci.vehicle.setSpeed("2010",2.5)
    else:
        pass

def test_case_four(step):
    print("test_case_four case has been activated.")
    #intersection_1
    if(step==1):
        traci.vehicle.setSpeedMode("3001",32)
        traci.vehicle.setLaneChangeMode("3001", 0)
        traci.vehicle.setSpeed("3001",1.575)
        traci.vehicle.setSpeedMode("3002",32)
        traci.vehicle.setLaneChangeMode("3002", 0)
        traci.vehicle.setSpeed("3002",2.575) #Crash for 8 with 1002
        traci.vehicle.setSpeedMode("3003",32)
        traci.vehicle.setLaneChangeMode("3003", 0)
        traci.vehicle.setSpeed("3003",2)
        traci.vehicle.setSpeedMode("3004",32)
        traci.vehicle.setLaneChangeMode("3004", 0)
        traci.vehicle.setSpeed("3004",4)
    elif(step==2):
        traci.vehicle.setSpeedMode("3005",32)
        traci.vehicle.setLaneChangeMode("3005", 0)
        traci.vehicle.setSpeed("3005",4)
        traci.vehicle.setSpeedMode("3006",32)
        traci.vehicle.setLaneChangeMode("3006", 0)
        traci.vehicle.setSpeed("3006",2.6)
        traci.vehicle.setSpeedMode("3007",32)
        traci.vehicle.setLaneChangeMode("3007", 0)
        traci.vehicle.setSpeed("3007",4)
        traci.vehicle.setSpeedMode("3008",32)
        traci.vehicle.setLaneChangeMode("3008", 0)
        traci.vehicle.setSpeed("3008",4)
    #intersection_2
    # elif(step==3):
    #     traci.vehicle.setSpeedMode("4005",32)
    #     traci.vehicle.setLaneChangeMode("4005", 0)
    #     traci.vehicle.setSpeed("4005",4)
    #     traci.vehicle.setSpeedMode("4006",32)
    #     traci.vehicle.setLaneChangeMode("4006", 0)
    #     traci.vehicle.setSpeed("4006",5)
    #     traci.vehicle.setSpeedMode("4007",32)
    #     traci.vehicle.setLaneChangeMode("4007", 0)
    #     traci.vehicle.setSpeed("4007",6)
    #     traci.vehicle.setSpeedMode("4008",32)
    #     traci.vehicle.setLaneChangeMode("4008", 0)
    #     traci.vehicle.setSpeed("4008",2.5)
    #     traci.vehicle.setSpeedMode("4009",32)
    #     traci.vehicle.setLaneChangeMode("4009", 0)
    #     traci.vehicle.setSpeed("4009",2.9)
    #     traci.vehicle.setSpeedMode("4010",32)
    #     traci.vehicle.setLaneChangeMode("4010", 0)
    #     traci.vehicle.setSpeed("4010",2.5)
    # elif(step==4):
    #     traci.vehicle.setSpeedMode("4001",32)
    #     traci.vehicle.setLaneChangeMode("4001", 0)
    #     traci.vehicle.setSpeed("4001",2.5)
    #     traci.vehicle.setSpeedMode("4002",32)
    #     traci.vehicle.setLaneChangeMode("4002", 0)
    #     traci.vehicle.setSpeed("4002",2.5)
    #     traci.vehicle.setSpeedMode("4003",32)
    #     traci.vehicle.setLaneChangeMode("4003", 0)
    #     traci.vehicle.setSpeed("4003",2.5)
    #     traci.vehicle.setSpeedMode("4004",32)
    #     traci.vehicle.setLaneChangeMode("4004", 0)
    #     traci.vehicle.setSpeed("4004",2.5)
    # #intersection_4
    # elif(step==5):
    #     traci.vehicle.setSpeedMode("5001",32)
    #     traci.vehicle.setLaneChangeMode("5001", 0)
    #     traci.vehicle.setSpeed("5001",2.5)
    #     traci.vehicle.setSpeedMode("5002",32)
    #     traci.vehicle.setLaneChangeMode("5002", 0)
    #     traci.vehicle.setSpeed("5002",2.5)
    #     traci.vehicle.setSpeedMode("5003",32)
    #     traci.vehicle.setLaneChangeMode("5003", 0)
    #     traci.vehicle.setSpeed("5003",2.5)
    #     traci.vehicle.setSpeedMode("5004",32)
    #     traci.vehicle.setLaneChangeMode("5004", 0)
    #     traci.vehicle.setSpeed("5004",2.5)
    else:
        pass

def uncontrolled_case_twosec(step):
    print("Uncontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeedMode("1004",32)
        traci.vehicle.setLaneChangeMode("1004", 0)
        traci.vehicle.setSpeed("1004",25)
        traci.vehicle.setSpeedMode("1007",32)
        traci.vehicle.setLaneChangeMode("1007", 0)
        traci.vehicle.setSpeed("1007",25.5)
        traci.vehicle.setSpeedMode("1002",32)
        traci.vehicle.setLaneChangeMode("1002", 0)
        traci.vehicle.setSpeed("1002",24.5)
    elif(step==3):
        traci.vehicle.setSpeedMode("1005",32)
        traci.vehicle.setLaneChangeMode("1005", 0)
        traci.vehicle.setSpeed("1005",25)
        traci.vehicle.setSpeedMode("1008",32)
        traci.vehicle.setLaneChangeMode("1008", 0)
        traci.vehicle.setSpeed("1008",29)
        traci.vehicle.setSpeedMode("1003",32)
        traci.vehicle.setLaneChangeMode("1003", 0)
        traci.vehicle.setSpeed("1003",25)
    elif(step==5):
        traci.vehicle.setSpeedMode("1006",32)
        traci.vehicle.setLaneChangeMode("1006", 0)
        traci.vehicle.setSpeed("1006",25)
        traci.vehicle.setSpeedMode("1009",32)
        traci.vehicle.setLaneChangeMode("1009", 0)
        traci.vehicle.setSpeed("1009",25)
        traci.vehicle.setSpeedMode("1001",32)
        traci.vehicle.setLaneChangeMode("1001", 0)
        traci.vehicle.setSpeed("1001",25)
    elif(step==7):
        traci.vehicle.setSpeedMode("1010",32)
        traci.vehicle.setLaneChangeMode("1010", 0)
        traci.vehicle.setSpeed("1010",25)
    else:
        pass

def uncontrolled_case2(step):
    print("Uncontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeedMode("1004",32)
        traci.vehicle.setLaneChangeMode("1004", 0)
        traci.vehicle.setSpeed("1004",70)
        traci.vehicle.setSpeedMode("1007",32)
        traci.vehicle.setLaneChangeMode("1007", 0)
        traci.vehicle.setSpeed("1007",70.25)
        traci.vehicle.setSpeedMode("1002",32)
        traci.vehicle.setLaneChangeMode("1002", 0)
        traci.vehicle.setSpeed("1002",69.75)
    elif(step==3):
        traci.vehicle.setSpeedMode("1005",32)
        traci.vehicle.setLaneChangeMode("1005", 0)
        traci.vehicle.setSpeed("1005",13.85)
        traci.vehicle.setSpeedMode("1008",32)
        traci.vehicle.setLaneChangeMode("1008", 0)
        traci.vehicle.setSpeed("1008",14)
        traci.vehicle.setSpeedMode("1003",32)
        traci.vehicle.setLaneChangeMode("1003", 0)
        traci.vehicle.setSpeed("1003",14.15)
    elif(step==5):
        traci.vehicle.setSpeedMode("1006",32)
        traci.vehicle.setLaneChangeMode("1006", 0)
        traci.vehicle.setSpeed("1006",55)
        traci.vehicle.setSpeedMode("1009",32)
        traci.vehicle.setLaneChangeMode("1009", 0)
        traci.vehicle.setSpeed("1009",55)
        traci.vehicle.setSpeedMode("1001",32)
        traci.vehicle.setLaneChangeMode("1001", 0)
        traci.vehicle.setSpeed("1001",55)
    elif(step==7):
        traci.vehicle.setSpeedMode("1010",32)
        traci.vehicle.setLaneChangeMode("1010", 0)
        traci.vehicle.setSpeed("1010",25)
    else:
        pass

def uncontrolled_case3(step):
    print("Uncontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeedMode("1004",32)
        traci.vehicle.setLaneChangeMode("1004", 0)
        traci.vehicle.setSpeed("1004",90)
        traci.vehicle.setSpeedMode("1007",32)
        traci.vehicle.setLaneChangeMode("1007", 0)
        traci.vehicle.setSpeed("1007",91)
        traci.vehicle.setSpeedMode("1002",32)
        traci.vehicle.setLaneChangeMode("1002", 0)
        traci.vehicle.setSpeed("1002",89)
    elif(step==3):
        traci.vehicle.setSpeedMode("1005",32)
        traci.vehicle.setLaneChangeMode("1005", 0)
        traci.vehicle.setSpeed("1005",80.25)
        traci.vehicle.setSpeedMode("1008",32)
        traci.vehicle.setLaneChangeMode("1008", 0)
        traci.vehicle.setSpeed("1008",80.35)
        traci.vehicle.setSpeedMode("1003",32)
        traci.vehicle.setLaneChangeMode("1003", 0)
        traci.vehicle.setSpeed("1003",79.85)
    elif(step==5):
        traci.vehicle.setSpeedMode("1006",32)
        traci.vehicle.setLaneChangeMode("1006", 0)
        traci.vehicle.setSpeed("1006",75)
        traci.vehicle.setSpeedMode("1009",32)
        traci.vehicle.setLaneChangeMode("1009", 0)
        traci.vehicle.setSpeed("1009",75)
        traci.vehicle.setSpeedMode("1001",32)
        traci.vehicle.setLaneChangeMode("1001", 0)
        traci.vehicle.setSpeed("1001",75)
    elif(step==7):
        traci.vehicle.setSpeedMode("1010",32)
        traci.vehicle.setLaneChangeMode("1010", 0)
        traci.vehicle.setSpeed("1010",85)
    else:
        pass

def uncontrolled_case4(step):
    print("Uncontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeedMode("1004",32)
        traci.vehicle.setLaneChangeMode("1004", 0)
        traci.vehicle.setSpeed("1004",90)
        traci.vehicle.setSpeedMode("1007",32)
        traci.vehicle.setLaneChangeMode("1007", 0)
        traci.vehicle.setSpeed("1007",91)
    elif(step==3):
        traci.vehicle.setSpeedMode("1005",32)
        traci.vehicle.setLaneChangeMode("1005", 0)
        traci.vehicle.setSpeed("1005",80.25)
        traci.vehicle.setSpeedMode("1008",32)
        traci.vehicle.setLaneChangeMode("1008", 0)
        traci.vehicle.setSpeed("1008",80.35)
        traci.vehicle.setSpeedMode("1003",32)
        traci.vehicle.setLaneChangeMode("1003", 0)
        traci.vehicle.setSpeed("1003",79.85)
        traci.vehicle.setSpeedMode("1002",32)
        traci.vehicle.setLaneChangeMode("1002", 0)
        traci.vehicle.setSpeed("1002",80.5)
        traci.vehicle.setSpeedMode("1006",32)
        traci.vehicle.setLaneChangeMode("1006", 0)
        traci.vehicle.setSpeed("1006",80)
    elif(step==5):
        traci.vehicle.setSpeedMode("1009",32)
        traci.vehicle.setLaneChangeMode("1009", 0)
        traci.vehicle.setSpeed("1009",75)
        traci.vehicle.setSpeedMode("1001",32)
        traci.vehicle.setLaneChangeMode("1001", 0)
        traci.vehicle.setSpeed("1001",75)
    elif(step==7):
        traci.vehicle.setSpeedMode("1010",32)
        traci.vehicle.setLaneChangeMode("1010", 0)
        traci.vehicle.setSpeed("1010",85)
    else:
        pass

def uncontrolled_case5(step):
    print("Uncontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeedMode("1004",32)
        traci.vehicle.setLaneChangeMode("1004", 0)
        traci.vehicle.setSpeed("1004",50)
        traci.vehicle.setSpeedMode("1007",32)
        traci.vehicle.setLaneChangeMode("1007", 0)
        traci.vehicle.setSpeed("1007",50.5)
    elif(step==3):
        traci.vehicle.setSpeedMode("1005",32)
        traci.vehicle.setLaneChangeMode("1005", 0)
        traci.vehicle.setSpeed("1005",50)
        traci.vehicle.setSpeedMode("1008",32)
        traci.vehicle.setLaneChangeMode("1008", 0)
        traci.vehicle.setSpeed("1008",58)
    elif(step==5):
        traci.vehicle.setSpeedMode("1006",32)
        traci.vehicle.setLaneChangeMode("1006", 0)
        traci.vehicle.setSpeed("1006",25)
        traci.vehicle.setSpeedMode("1009",32)
        traci.vehicle.setLaneChangeMode("1009", 0)
        traci.vehicle.setSpeed("1009",25)
    elif(step==7):
        traci.vehicle.setSpeedMode("1010",32)
        traci.vehicle.setLaneChangeMode("1010", 0)
        traci.vehicle.setSpeed("1010",25)
    else:
        pass

#There is right of way rules, so there will not be any collision
def sumocontrolled_case(step):
    #print("Sumocontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeed("1004",25)
        traci.vehicle.setSpeed("1007",25.5)
        traci.vehicle.setSpeed("1002",24.5)
    elif(step==3):
        traci.vehicle.setSpeed("1005",13.85)
        traci.vehicle.setSpeed("1008",14)
        traci.vehicle.setSpeed("1003",14.15)
    elif(step==5):
        traci.vehicle.setSpeed("1006",25)
        traci.vehicle.setSpeed("1009",25)
        traci.vehicle.setSpeed("1001",25)
    else:
        pass

def sumocontrolled_case2(step):
    #print("Sumocontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeed("1004",70)
        traci.vehicle.setSpeed("1007",70.25)
        traci.vehicle.setSpeed("1002",69.75)
    elif(step==3):
        traci.vehicle.setSpeed("1005",13.5)
        traci.vehicle.setSpeed("1008",14)
        traci.vehicle.setSpeed("1003",13.75)
    elif(step==5):
        traci.vehicle.setSpeed("1006",55)
        traci.vehicle.setSpeed("1009",55)
        traci.vehicle.setSpeed("1001",55)
    else:
        pass

def sumocontrolled_case3(step):
    #print("Sumocontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeed("1004",90)
        traci.vehicle.setSpeed("1007",91)
        traci.vehicle.setSpeed("1002",89)
    elif(step==3):
        traci.vehicle.setSpeed("1005",80.25)
        traci.vehicle.setSpeed("1008",80.35)
        traci.vehicle.setSpeed("1003",79.85)
    elif(step==5):
        traci.vehicle.setSpeed("1006",75)
        traci.vehicle.setSpeed("1009",75)
        traci.vehicle.setSpeed("1001",75)
    else:
        pass

def sumocontrolled_case4(step):
    #print("Sumocontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeed("1004",90)
        traci.vehicle.setSpeed("1007",91)
    elif(step==3):
        traci.vehicle.setSpeed("1005",80.25)
        traci.vehicle.setSpeed("1008",80.35)
        traci.vehicle.setSpeed("1003",79.85)
        traci.vehicle.setSpeed("1002",89)
        traci.vehicle.setSpeed("1006",75)
    elif(step==5):
        traci.vehicle.setSpeed("1009",75)
        traci.vehicle.setSpeed("1001",75)
    else:
        pass

def sumocontrolled_case5(step):
    #print("Sumocontrolled case has been activated.")
    if(step==1):
        traci.vehicle.setSpeed("1004",50)
        traci.vehicle.setSpeed("1007",50.5)
    elif(step==3):
        traci.vehicle.setSpeed("1005",50)
        traci.vehicle.setSpeed("1008",58)
    elif(step==5):
        traci.vehicle.setSpeed("1006",25)
        traci.vehicle.setSpeed("1009",25)
    else:
        pass
