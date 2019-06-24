#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa


def run():
    """execute the TraCI control loop"""
    step = 0
    count = 0
    while step < 1000:
        traci.simulationStep()
		#Se passou um veiculo. Ou seja um Contador
        if traci.inductionloop.getLastStepVehicleNumber("e1Detector_Faixa_7_0_0") > 0:
            count += 1
            print ('Numero de Veiculos', count)
            x = traci.trafficlight.getNextSwitch("Inter")
            # print (x)
        z =	traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_2_2")
        y = traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_0_0") + traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_1_1") + traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_2_2")
        print ('Veiculos na Area', z)
        print ('Veiculos Parados', y)		
		
		
        step += 1
	
    scResults = traci.junction.getContextSubscriptionResults("Inter")
    halting = 0
    if scResults:
        relSpeeds = [d[tc.VAR_SPEED] / d[tc.VAR_ALLOWED_SPEED] for d in scResults.values()]
        # compute values corresponding to summary-output
        running = len(relSpeeds)
        halting = len([1 for d in scResults.values() if d[tc.VAR_SPEED] < 0.1])
        meanSpeedRelative = sum(relSpeeds) / running
        timeLoss = (1 - meanSpeedRelative) * running * stepLength
        print(traci.simulation.getTime(), timeLoss, halting)
   
    traci.close()
    sys.stdout.flush()  
 


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')


    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "Cruz_Simples.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()