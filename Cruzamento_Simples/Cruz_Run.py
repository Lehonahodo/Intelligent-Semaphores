# we need to import Traci Lybrary from python in the specifiesd SUMO_HOME
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'"
	 
# This assumes that the environment variable SUMO_HOME is set before running the script

from sumolib import checkBinary  # noqa


# Start the simulation and connect to it with our script
import traci
traci.start(sumoCmd) 
step = 0
while step < 1000:
   traci.simulationStep()
   if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
       traci.trafficlight.setRedYellowGreenState("0", "GrGr")
   step += 1

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

# After connecting to the simulation, you can emit various commands and execute simulation steps 
# until you want to finish by closing the connection. 
# by default the close command will wait until the sumo process really finishes. 
# You can disable this by calling traci.close(False)