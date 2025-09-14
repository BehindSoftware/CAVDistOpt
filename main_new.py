from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import logging
import numpy as np
from scipy.stats import qmc

from dist.simulator import optimized_case
from map_lib import create_map, add_manual_vehicle
from manhattan_lib import network_file_creation
from report_lib import create_report
from TCs_dist import sumocontrolled_case_TC1_dist, sumocontrolled_case_TC1_row_dist, uncontrolled_case_TC2_dist

#DESC Conf: Panel for configurations
LOGGER_ACTIVE = False
OPTIMIZATION_ACTIVE = True
SUMO_ACTIVE = True
MAPCREATION_ACTIVE = True
MAPGENERATION_ACTIVE = False
ADDMANUALVEHICLE_ACTIVE = False
ROUTECREATION_ACTIVE = False
TL = False
AUTO_START = True

def set_parameters(t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance,
                   vehicle_length, edge_len, raw_intersection_num, column_intersection_num, detector_pos,
                   node_num, MAX_ITER, TIME_GAP, TOLERANCE, RHO):

    node_num = raw_intersection_num * column_intersection_num
    parameters = [t, max_speed, lower_acc, upper_acc, speed_loc_fac, reaction_t, safety_distance,
                  vehicle_length, edge_len, raw_intersection_num, column_intersection_num, detector_pos,
                  node_num, MAX_ITER, TIME_GAP, TOLERANCE, RHO]
    return parameters

# Logger (opsiyonel)
if LOGGER_ACTIVE:
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

    logging.basicConfig(filename='output.log', level=logging.INFO)
    logger = logging.getLogger()
    sys.stdout = StreamToLogger(logger, logging.INFO)

# SUMO import
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

# DESC RUN
def run(parameters):
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print("Step:" + str(step))

        if OPTIMIZATION_ACTIVE:
            optimized_case(step, parameters)
        elif SUMO_ACTIVE:
            sumocontrolled_case_TC1_dist(step)
            sumocontrolled_case_TC1_row_dist(step)
        else:
            uncontrolled_case_TC2_dist(step)

        step += 1
    traci.close()
    sys.stdout.flush()

# CLI options
def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# === Yeni: LHS Experiments ===
def run_lhs_experiments(n_samples=20):
    # Parametre havuzları
    t = [1]
    max_speed = [60, 90, 120, 180, 240]
    lower_acc = [-6, -3, -1]
    upper_acc = [1, 3, 6]
    speed_loc_fac = [0.0, 0.2, 0.4, 0.5]
    reaction_t = [0.2, 0.5, 1.0]
    safety_distance = [0, 2, 5]
    vehicle_length = [2, 4, 6]
    MAX_ITER = [3, 6, 9]
    TIME_GAP = [0.8, 2.0, 4.0]
    TOLERANCE = [0.5, 2.5, 7.5]
    RHO = [0.5, 1.5, 2.5, 10.0]

    param_space = [
        t, max_speed, lower_acc, upper_acc,
        speed_loc_fac, reaction_t, safety_distance, vehicle_length,
        MAX_ITER, TIME_GAP, TOLERANCE, RHO
    ]

    sampler = qmc.LatinHypercube(d=len(param_space))
    lhs_samples = sampler.random(n=n_samples)

    lhs_scaled = []
    for i, space in enumerate(param_space):
        values = np.linspace(min(space), max(space), num=len(space))
        idx = (lhs_samples[:, i] * (len(values) - 1)).astype(int)
        lhs_scaled.append(values[idx])

    lhs_scaled = np.array(lhs_scaled).T
    print(f"[INFO] {n_samples} adet LHS senaryosu üretildi.")

    for i, row in enumerate(lhs_scaled):
        print(f"\n[RUN] Senaryo {i+1}/{n_samples} çalışıyor...")

        parameters = set_parameters(
            int(row[0]), float(row[1]), float(row[2]), float(row[3]),
            float(row[4]), float(row[5]), float(row[6]), float(row[7]),
            500, 3, 3, 2, 0, int(row[8]), float(row[9]), float(row[10]), float(row[11])
        )

        options = get_options()
        sumoBinary = checkBinary('sumo-gui') if not options.nogui else checkBinary('sumo')

        if OPTIMIZATION_ACTIVE:
            if AUTO_START:
                traci.start([sumoBinary, "--start", "--quit-on-end", "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "reports/tripinfo.xml", "--netstate-dump=reports/testdump.xml",
                             "--collision.check-junctions", "--emergency-insert", "--collision.action=remove",
                             "--emission-output=reports/emissions.xml", "--full-output=reports/fulloutput.xml",
                             "--emissions.volumetric-fuel", "--log=log.txt",
                             "--emergencydecel.warning-threshold=100", "--collision.mingap-factor=0"])
            else:
                traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "reports/tripinfo.xml", "--netstate-dump=reports/testdump.xml",
                             "--collision.check-junctions", "--emergency-insert", "--collision.action=remove",
                             "--emission-output=reports/emissions.xml", "--full-output=reports/fulloutput.xml",
                             "--emissions.volumetric-fuel", "--log=log.txt",
                             "--emergencydecel.warning-threshold=100", "--collision.mingap-factor=0"])

        run(parameters)
        create_report(parameters)

# === Main Entry ===
if __name__ == "__main__":
    run_lhs_experiments(n_samples=30)   # buradaki sayıyı istediğin kadar senaryo için değiştirebilirsin
