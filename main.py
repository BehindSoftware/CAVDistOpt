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

from dist.simulator import optimized_case
from map_lib import create_map, add_manual_vehicle, case_1, case_1_twosec
from manhattan_lib import network_file_creation
from report_lib import parse_col, parse_fuel, create_report
from TCs import uncontrolled_case_TC1, sumocontrolled_case_TC1, sumocontrolled_case_TC1_row, uncontrolled_case_TC2, sumocontrolled_case_TC2, sumocontrolled_case_TC2_row, uncontrolled_case_TC3, sumocontrolled_case_TC3, sumocontrolled_case_TC3_row, uncontrolled_case_TC4, sumocontrolled_case_TC4, sumocontrolled_case_TC4_row, uncontrolled_case_TC5, sumocontrolled_case_TC5, sumocontrolled_case_TC5_row, uncontrolled_case_TC5_TL
from TCs_dist import uncontrolled_case_TC1_dist, sumocontrolled_case_TC1_dist, sumocontrolled_case_TC1_row_dist

#DESC Conf: Panel for configurations
LOGGER_ACTIVE = False
OPTIMIZATION_ACTIVE = True #For use optimization in the intersection
SUMO_ACTIVE = True
MAPCREATION_ACTIVE = True #Creating the generation of map according to raw_intersection_num,column_intersection_num,edge_len,detector_pos
MAPGENERATION_ACTIVE = False #Manhattan generation usage
ADDMANUALVEHICLE_ACTIVE = False #Adding to new vehicle for present scenario 
ROUTECREATION_ACTIVE = False #Creating the generation of route file
TL = False #Adding Traffic_Lights

def set_parameters(parameters):
    #parameters
    t = 1
    max_speed = 90
    lower_acc = -7
    upper_acc = 7 #If you do this as 4, there is crash on our scenario test with too much accelaration
    speed_loc_fac = 0.49
    reaction_t = 1
    safety_distance = 2.5
    vehicle_length = 4

    parameters = [t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance, vehicle_length]
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
def run(induction_loop_number,edge_len,parameters):
    """execute the TraCI control loop"""
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print("Step:"+str(step))

        if(OPTIMIZATION_ACTIVE==True):
            optimized_case(step,induction_loop_number,edge_len,parameters)
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
            uncontrolled_case_TC1_dist(step)
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
    options = get_options()

    # this script has been called from the command line. It will start sumo as a server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    if(MAPCREATION_ACTIVE==True):
        raw_intersection_num = 3 #intersection number for x line (parametric)
        column_intersection_num = 3 #intersection number for y line (parametric)
        edge_len = 500 #the length of edge (parametric)
        detector_pos = 12 #detector position (parametric)
        create_map(raw_intersection_num,column_intersection_num,edge_len,detector_pos, TL)
        
        #generation net.xml from nod,edg and con
        os.system("netconvert --node-files=data/cross.nodtest.xml --edge-files=data/cross.edgtest.xml --connection-files=data/cross.contest.xml  --output-file=data/cross.nettest.xml --tls.red.time=60 --tls.yellow.time=3 --tls.green.time=30 --speed.minimum=50 --default.speed=50")
        
        #generation rou.xml according to net.xml
        if(ROUTECREATION_ACTIVE==True):
            os.system("python3 tools/randomTrips.py -n data/cross.nettest.xml -e 50 --route-file data/cross.routest.xml --validate ")

    elif(MAPGENERATION_ACTIVE==True):
        raw_intersection_num = 3
        column_intersection_num = 3
        edge_len = 500
        network_file_creation(raw_intersection_num,column_intersection_num,edge_len)
    else:
        print("Map can not be created, please check the defines.")
        pass

    if(ADDMANUALVEHICLE_ACTIVE==True):
        add_manual_vehicle()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "reports/tripinfo.xml", "--netstate-dump=reports/testdump.xml", "--collision.check-junctions", "--emergency-insert", "--collision.action=remove", "--emission-output=reports/emissions.xml", "--full-output=reports/fulloutput.xml", "--emissions.volumetric-fuel", "--log=log.txt"])
    
    node_num = raw_intersection_num*column_intersection_num

    parameters = []
    parameters = set_parameters(parameters)
    run(node_num,edge_len,parameters)
    create_report(parameters)
# DESC Main: END 