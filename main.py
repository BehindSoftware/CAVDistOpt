#!/usr/bin/env python
# @file    runner.py
# @author  Berkay Saydam
# @date    2024-05-17

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import logging
import itertools

from dist.simulator import optimized_case
from map_lib import create_map, add_manual_vehicle, case_1, case_1_twosec
from manhattan_lib import network_file_creation
from report_lib import parse_col, parse_fuel, create_report
from TCs import uncontrolled_case_TC1, sumocontrolled_case_TC1, sumocontrolled_case_TC1_row, uncontrolled_case_TC2, sumocontrolled_case_TC2, sumocontrolled_case_TC2_row, uncontrolled_case_TC3, sumocontrolled_case_TC3, sumocontrolled_case_TC3_row, uncontrolled_case_TC4, sumocontrolled_case_TC4, sumocontrolled_case_TC4_row, uncontrolled_case_TC5, sumocontrolled_case_TC5, sumocontrolled_case_TC5_row, uncontrolled_case_TC5_TL
from TCs_dist import uncontrolled_case_TC1_dist, sumocontrolled_case_TC1_dist, sumocontrolled_case_TC1_row_dist, uncontrolled_case_TC2_dist, uncontrolled_case_TC3_dist, uncontrolled_case_TC4_dist

#DESC Conf: Panel for configurations
LOGGER_ACTIVE = False
OPTIMIZATION_ACTIVE = True #For use optimization in the intersection
SUMO_ACTIVE = True
MAPCREATION_ACTIVE = True #Creating the generation of map according to raw_intersection_num,column_intersection_num,edge_len,detector_pos
MAPGENERATION_ACTIVE = False #Manhattan generation usage
ADDMANUALVEHICLE_ACTIVE = False #Adding to new vehicle for present scenario 
ROUTECREATION_ACTIVE = False #Creating the generation of route file
TL = False #Adding Traffic_Lights
AUTO_START = True

def set_parameters(t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance, vehicle_length, edge_len, raw_intersection_num, column_intersection_num, detector_pos, node_num, MAX_ITER, TIME_GAP, TOLERANCE, RHO):
    #parameters
    # t = 1
    # max_speed = 90 #-> 60 90 test it time decrease fuel increase
    # lower_acc = -3
    # upper_acc = 3 #If you do this as 4, there is crash on our scenario test with too much accelaration
    # speed_loc_fac = 0.1 #-> 0.1 0.2 0.3 test it fuel decrease time increase
    # reaction_t = 1
    # safety_distance = 2
    # vehicle_length = 4
    # edge_len = 500
    # raw_intersection_num = 3 #intersection number for x line (parametric)
    # column_intersection_num = 3 #intersection number for y line (parametric)
    # detector_pos = 2 #detector position (parametric)
    node_num = raw_intersection_num*column_intersection_num
    # MAX_ITER = 5
    # TIME_GAP = 0.8
    # TOLERANCE = 7.5 #Determine according to sensitivity (A car distance to other/intersection can be about 7.5(min gap+car_len)) -> If tolerance is increasing from 2.5, there are collisions
    # RHO = 0.5 #Infeasible when it is higher than 2.5 in TC4 -> Reverse relation with tolerance if decrease to tolerance you need to increase RHO

    parameters = [t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance, vehicle_length, edge_len, raw_intersection_num, column_intersection_num, detector_pos, node_num, MAX_ITER, TIME_GAP, TOLERANCE, RHO]
    #print(parameters)
    return parameters
#DESC Conf: END

## DESC LOGGER: To export detail log file 
if(LOGGER_ACTIVE==True):
    class StreamToLogger:
        def __init__(self, logger, log_level=logging.INFO):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            pass

    # Configure logging
    logging.basicConfig(filename='output.log', level=logging.INFO)
    logger = logging.getLogger()

    # Redirect stdout to logging
    sys.stdout = StreamToLogger(logger, logging.INFO)
## DESC LOGGER: END

# DESC SUMO: we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa
# DESC SUMO: END

# DESC RUN: Creating communication with simulator via TraCI
def run(parameters):
    """execute the TraCI control loop"""
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print("Step:"+str(step))

        if(OPTIMIZATION_ACTIVE==True):
            optimized_case(step,parameters)
        elif(SUMO_ACTIVE==True):
            #sumocontrolled_case(step)
            #sumocontrolled_case_TC1(step)
            #sumocontrolled_case_TC1_row(step)
            #sumocontrolled_case_TC2(step)
            #sumocontrolled_case_TC2_row(step)
            #sumocontrolled_case_TC3(step)
            #sumocontrolled_case_TC3_row(step)
            #sumocontrolled_case_TC4(step)
            #sumocontrolled_case_TC4_row(step)
            #sumocontrolled_case_TC5(step)
            #sumocontrolled_case_TC5_row(step)
            sumocontrolled_case_TC1_dist(step) 
            sumocontrolled_case_TC1_row_dist(step)

        else:
            #uncontrolled_case(step)
            #uncontrolled_case_TC1(step)
            #uncontrolled_case_TC2(step)
            #uncontrolled_case_TC3(step)
            #uncontrolled_case_TC4(step)
            #uncontrolled_case_TC5(step)
            #uncontrolled_case_TC5_TL(step)
            #uncontrolled_case_TC1_dist(step)
            uncontrolled_case_TC2_dist(step)
            #uncontrolled_case_TC3_dist(step)
            #uncontrolled_case_TC4_dist(step)
            pass

        step += 1
    traci.close()
    sys.stdout.flush()
# DESC RUN: END

# DESC Main: Main part 
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":
    
    t = [1]
    max_speed = [90, 120, 180]
    lower_acc = [-2, -3, -4]
    upper_acc = [2, 3, 4]
    speed_loc_fac = [0.1, 0.2, 0.3, 0.4]
    reaction_t = [0.5, 1, 2]
    safety_distance = [2, 5, 8]
    vehicle_length = [3, 4, 5]
    #node_num = raw_intersection_num*column_intersection_num
    MAX_ITER = [3, 5, 7]
    TIME_GAP = [0.8 , 2, 4]
    TOLERANCE = [0.5, 2.5, 7.5] 
    RHO = [0.5, 1.5, 2.5]
    
    for param1, param2, param3, param4, param5, param6, param7, param8, param9, param10, param11, param12 in itertools.product(t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance, vehicle_length, MAX_ITER, TIME_GAP, TOLERANCE, RHO):
        #parameters = []
        parameters = set_parameters(param1, param2, param3, param4, param5, param6, param7, param8, 500, 3, 3, 2, 0, param9, param10, param11, param12)

        options = get_options()

        # this script has been called from the command line. It will start sumo as a server, then connect and run
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

        if(MAPCREATION_ACTIVE==True):

            create_map(parameters[9],parameters[10],parameters[8],parameters[11], TL)
            
            #generation net.xml from nod,edg and con
            os.system("netconvert --node-files=data/cross.nodtest.xml --edge-files=data/cross.edgtest.xml --connection-files=data/cross.contest.xml  --output-file=data/cross.nettest.xml --tls.red.time=60 --tls.yellow.time=3 --tls.green.time=30 --speed.minimum=50 --default.speed=50")
            
            #generation rou.xml according to net.xml
            if(ROUTECREATION_ACTIVE==True):
                os.system("python3 tools/randomTrips.py -n data/cross.nettest.xml -e 50 --route-file data/cross.routest.xml --validate ")

        elif(MAPGENERATION_ACTIVE==True):
            network_file_creation(parameters[9],parameters[10],parameters[8])
        else:
            print("Map can not be created, please check the defines.")
            pass

        if(ADDMANUALVEHICLE_ACTIVE==True):
            add_manual_vehicle()

        # this is the normal way of using traci. sumo is started as a
        # subprocess and then the python script connects and runs
        if(OPTIMIZATION_ACTIVE==True):
        #     traci.start([sumoBinary, "-c", "data/cross.sumocfg",
        #                          "--tripinfo-output", "reports/tripinfo.xml", "--netstate-dump=reports/testdump.xml", "--emergency-insert", "--collision.action=none", "--emission-output=reports/emissions.xml", "--full-output=reports/fulloutput.xml", "--emissions.volumetric-fuel", "--log=log.txt" , "--emergencydecel.warning-threshold=100", "--collision.mingap-factor=0"])
        # else:
            if(AUTO_START==True):
                traci.start([sumoBinary, "--start", "--quit-on-end", "-c", "data/cross.sumocfg",
                                "--tripinfo-output", "reports/tripinfo.xml", "--netstate-dump=reports/testdump.xml", "--collision.check-junctions", "--emergency-insert", "--collision.action=remove", "--emission-output=reports/emissions.xml", "--full-output=reports/fulloutput.xml", "--emissions.volumetric-fuel", "--log=log.txt" , "--emergencydecel.warning-threshold=100", "--collision.mingap-factor=0"])
            else:
                traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                                "--tripinfo-output", "reports/tripinfo.xml", "--netstate-dump=reports/testdump.xml", "--collision.check-junctions", "--emergency-insert", "--collision.action=remove", "--emission-output=reports/emissions.xml", "--full-output=reports/fulloutput.xml", "--emissions.volumetric-fuel", "--log=log.txt" , "--emergencydecel.warning-threshold=100", "--collision.mingap-factor=0"])

        run(parameters)
        create_report(parameters)
# DESC Main: END 