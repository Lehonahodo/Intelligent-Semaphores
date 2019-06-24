# @file    Run.py
# @author  Leo Vergueiro
# @date    2019-05-26

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import traci.constants as tc

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
    tempo = 0
    """ Number of executions"""
    while step < 1000:
        traci.simulationStep()
		
		#Se passou um veiculo. Ou seja um Contador
        if traci.inductionloop.getLastStepVehicleNumber("e1Detector_Faixa_7_0_0") > 0:
            count += 1
            print ('Numero de Veiculos', count)
            x = traci.trafficlight.getNextSwitch("Inter")
            # print (x)

        phase = traci.trafficlight.getPhaseDuration("Inter")
        print ('Duracao do Semaforo',phase)
			
        #Logica do semaforo
        #logic = traci.trafficlight.getCompleteRedYellowGreenDefinition('Inter')
        #print ('Logica do semaforo',logic)
        """[Logic(programID='0', type=0, currentPhaseIndex=2, phases=[Phase(duration=42.0, 
        state='GGGGrrrrGGGGgrrrr', minDur=42.0, maxDur=42.0, next=-1), Phase(duration=3.0, 
        state='yyyyrrrryyyyyrrrr', minDur=3.0, maxDur=3.0, next=-1), Phase(duration=42.0, 
        state='rrrrGGGGrrrrrGGGG', minDur=42.0, maxDur=42.0, next=-1), Phase(duration=3.0, 
        state='rrrryyyyrrrrryyyy', minDur=3.0, maxDur=3.0, next=-1)], subParameter={})]"""
		
        #Variavel Norte/Sul que soma o número de veículos nesse fluxo a cada timestep
        nor_sul=traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_7_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_7_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_7_2_2") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_3_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_3_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_3_2_2")
		
        #Variavel Leste/Oeste que soma o número de veículos nesse fluxo a cada timestep
        les_oes=traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_2_2") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_1_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_1_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_1_2_2")

        print ('Veiculos na via Norte/Sul: ',nor_sul)
        print ('Veiculos na via Leste/Oeste: ',les_oes)		
		
        z =	traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_2_2")
        y = traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_0_0") + traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_1_1") + traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_2_2")
        print ('Veiculos na Area', z)
        print ('Veiculos Parados', y)		
		
		#teste logica simples de mudança de fase (0 - nor sul, 1 - amarelo nor sul, 2 - les oes, 3 - amarelo les oes) - necessárias condições para mudança de fase ainda.
        #if nor_sul>les_oes:
        #    traci.trafficlight.setPhase('Inter',0)	
        #if les_oes>nor_sul:
        #    traci.trafficlight.setPhase('Inter',2)
        Dur_fase = (traci.trafficlight.getNextSwitch("Inter") - traci.simulation.getTime())
        if Dur_fase == 0:
            print('Duracao da fase ainda: ', (traci.trafficlight.getNextSwitch("Inter") - traci.simulation.getTime()))
            print('Tempo Parado Faixa 5: ', (traci.lane.getWaitingTime('Faixa_5_0')+traci.lane.getWaitingTime('Faixa_5_1')+traci.lane.getWaitingTime('Faixa_5_2')))
            tempo += traci.lane.getWaitingTime('Faixa_5_0')+traci.lane.getWaitingTime('Faixa_5_1')+traci.lane.getWaitingTime('Faixa_5_2')+ traci.lane.getWaitingTime('Faixa_1_0')+traci.lane.getWaitingTime('Faixa_1_1')+traci.lane.getWaitingTime('Faixa_1_2') + traci.lane.getWaitingTime('Faixa_3_0')+traci.lane.getWaitingTime('Faixa_3_1')+traci.lane.getWaitingTime('Faixa_3_2')+traci.lane.getWaitingTime('Faixa_7_0')+traci.lane.getWaitingTime('Faixa_7_1')+traci.lane.getWaitingTime('Faixa_7_2')

			
        step += 1
	
    print('Espera (s): ', tempo)
    #traci.junction.subscribeContext("Inter", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
    #print('Results: ', traci.junction.getContextSubscriptionResults("Inter"))
	
    #scResults = traci.junction.getContextSubscriptionResults("Inter")
    #halting = 0
    #if scResults:
    #    relSpeeds = [d[tc.VAR_SPEED] / d[tc.VAR_ALLOWED_SPEED] for d in scResults.values()]
    #    # compute values corresponding to summary-output
    #    running = len(relSpeeds)
    #    halting = len([1 for d in scResults.values() if d[tc.VAR_SPEED] < 0.1])
    #    meanSpeedRelative = sum(relSpeeds) / running
    #    timeLoss = (1 - meanSpeedRelative) * running * stepLength
    #    print(traci.simulation.getTime(), timeLoss, halting)
   
    #traci.close()
    #sys.stdout.flush()  

def run_2():
    """execute the TraCI control loop"""
    step = 0
    count = 0
    tempo = 0
    """ Number of executions"""
    while step < 1000:
        traci.simulationStep()
		
		#Se passou um veiculo. Ou seja um Contador
        if traci.inductionloop.getLastStepVehicleNumber("e1Detector_Faixa_7_0_0") > 0:
            count += 1
            print ('Numero de Veiculos', count)
            x = traci.trafficlight.getNextSwitch("Inter")
            # print (x)

        phase = traci.trafficlight.getPhaseDuration("Inter")
        print ('Duracao do Semaforo',phase)
			
        #Logica do semaforo
        #logic = traci.trafficlight.getCompleteRedYellowGreenDefinition('Inter')
        #print ('Logica do semaforo',logic)
        """[Logic(programID='0', type=0, currentPhaseIndex=2, phases=[Phase(duration=42.0, 
        state='GGGGrrrrGGGGgrrrr', minDur=42.0, maxDur=42.0, next=-1), Phase(duration=3.0, 
        state='yyyyrrrryyyyyrrrr', minDur=3.0, maxDur=3.0, next=-1), Phase(duration=42.0, 
        state='rrrrGGGGrrrrrGGGG', minDur=42.0, maxDur=42.0, next=-1), Phase(duration=3.0, 
        state='rrrryyyyrrrrryyyy', minDur=3.0, maxDur=3.0, next=-1)], subParameter={})]"""
		
        #Variavel Norte/Sul que soma o número de veículos nesse fluxo a cada timestep
        nor_sul=traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_7_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_7_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_7_2_2") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_3_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_3_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_3_2_2")
		
        #Variavel Leste/Oeste que soma o número de veículos nesse fluxo a cada timestep
        les_oes=traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_2_2") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_1_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_1_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_1_2_2")

        print ('Veiculos na via Norte/Sul: ',nor_sul)
        print ('Veiculos na via Leste/Oeste: ',les_oes)		
		
        z =	traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_0_0") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_1_1") + traci.lanearea.getLastStepVehicleNumber("e2Detector_Faixa_5_2_2")
        y = traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_0_0") + traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_1_1") + traci.lanearea.getJamLengthVehicle("e2Detector_Faixa_5_2_2")
        print ('Veiculos na Area', z)
        print ('Veiculos Parados', y)		
		
		#teste logica simples de mudança de fase (0 - nor sul, 1 - amarelo nor sul, 2 - les oes, 3 - amarelo les oes) - necessárias condições para mudança de fase ainda.
        #if nor_sul>les_oes:
        #    traci.trafficlight.setPhase('Inter',0)	
        #if les_oes>nor_sul:
        #    traci.trafficlight.setPhase('Inter',2)
        Dur_fase = (traci.trafficlight.getNextSwitch("Inter") - traci.simulation.getTime())
        if Dur_fase == 0:
            print('Duracao da fase ainda: ', (traci.trafficlight.getNextSwitch("Inter") - traci.simulation.getTime()))
            print('Tempo Parado Faixa 5: ', (traci.lane.getWaitingTime('Faixa_5_0')+traci.lane.getWaitingTime('Faixa_5_1')+traci.lane.getWaitingTime('Faixa_5_2')))
            tempo += traci.lane.getWaitingTime('Faixa_5_0')+traci.lane.getWaitingTime('Faixa_5_1')+traci.lane.getWaitingTime('Faixa_5_2')+ traci.lane.getWaitingTime('Faixa_1_0')+traci.lane.getWaitingTime('Faixa_1_1')+traci.lane.getWaitingTime('Faixa_1_2') + traci.lane.getWaitingTime('Faixa_3_0')+traci.lane.getWaitingTime('Faixa_3_1')+traci.lane.getWaitingTime('Faixa_3_2')+traci.lane.getWaitingTime('Faixa_7_0')+traci.lane.getWaitingTime('Faixa_7_1')+traci.lane.getWaitingTime('Faixa_7_2')

			
        step += 1
	
    print('Espera (s): ', tempo)
    #traci.junction.subscribeContext("Inter", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
    #print('Results: ', traci.junction.getContextSubscriptionResults("Inter"))
	
    #scResults = traci.junction.getContextSubscriptionResults("Inter")
    #halting = 0
    #if scResults:
    #    relSpeeds = [d[tc.VAR_SPEED] / d[tc.VAR_ALLOWED_SPEED] for d in scResults.values()]
    #    # compute values corresponding to summary-output
    #    running = len(relSpeeds)
    #    halting = len([1 for d in scResults.values() if d[tc.VAR_SPEED] < 0.1])
    #    meanSpeedRelative = sum(relSpeeds) / running
    #    timeLoss = (1 - meanSpeedRelative) * running * stepLength
    #    print(traci.simulation.getTime(), timeLoss, halting)
   
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
    #run()
    run_2()