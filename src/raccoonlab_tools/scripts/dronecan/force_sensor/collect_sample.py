#!/usr/bin/env python3
# This software is distributed under the terms of the MIT License.
# Copyright (c) 2024 Dmitry Ponomarev.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
import os
import secrets
import pandas as pd
import dronecan
import time
from enum import IntEnum

from raccoonlab_tools.common.protocol_parser import CanProtocolParser, Protocol
from raccoonlab_tools.dronecan.global_node import DronecanNode
from raccoonlab_tools.dronecan.utils import (
    Parameter,
    ParametersInterface,
    NodeCommander,
)

PARAM_UAVCAN_NODE_ID = "uavcan.node.id"
PARAM_BATTERY_SOC_PCT = "battery.soc_pct"
PARAM_BATTERY_ID = "battery.battery_id"
PARAM_BATTERY_MODEL_INSTANCE_ID = "battery.model_instance_id"
PARAM_BATTERY_CAPACITY_MAH = "battery.capacity_mah"
PARAM_BATTERY_FULL_VOLTAGE_MV = "battery.full_voltage_mv"
PARAM_BATTERY_EMPTY_VOLTAGE_MV = "battery.empty_voltage_mv"
PARAM_BUZZER_ERROR_MELODY = "buzzer.error_melody"
PARAM_BUZZER_ARM_MELODY = "buzzer.arm_melody"
PARAM_BUZZER_FREQUENCY = "buzzer.frequency"
PARAM_BUZZER_BEEP_FRACTION = "buzzer.beep_fraction"
PARAM_BUZZER_BEEP_PERIOD = "buzzer.beep_period"
PARAM_BUZZER_VERBOSE = "buzzer.verbose"
PARAM_GATE_THRESHOLD = "gate.threshold"


class ErrorMelodies(IntEnum):
    ANNOYING = 0
    TOLERABLE = 1
    BIMMER = 2
    DEFINED_BY_PARAMS = 127


class ParamLightsType(IntEnum):
    SOLID = 0
    BLINKING = 1
    PULSING = 2


class PMUNode:
    min_frequency: int = 50

    def __init__(self) -> None:
        self.node = DronecanNode()

    def recv_force(self, timeout_sec=0.03):
        res = self.node.sub_once(
            dronecan.uavcan.equipment.actuator.Status, timeout_sec = timeout_sec
        )
        return res.message

    def configure(self, config):
        params = ParametersInterface()
        commander = NodeCommander()

        params.set(config)
        commander.store_persistent_states()
        commander.restart()


def make_beeper_cmd_from_values(frequency: float, duration: float):
    return dronecan.uavcan.equipment.indication.BeepCommand(
        frequency=frequency, duration=duration
    )

class TestGateOk:
    """
    The test class with maximum gate_threshold value, 
    so the node will always listen to the BeepCommands
    """

    config = [
        Parameter(name=PARAM_BATTERY_ID, value=0),
        Parameter(name=PARAM_BATTERY_MODEL_INSTANCE_ID, value=0),
        Parameter(name=PARAM_BUZZER_ERROR_MELODY, value=127),
        Parameter(name=PARAM_BUZZER_FREQUENCY, value=ParamLightsType.SOLID),
        Parameter(name=PARAM_GATE_THRESHOLD, value=4095),
        Parameter(name=PARAM_BUZZER_VERBOSE, value=1),
    ]
    pmu = PMUNode()
    randomizer = secrets.SystemRandom()
    @staticmethod
    def configure_node():
        TestGateOk.pmu.configure(TestGateOk.config)
        time.sleep(5)

    def get_force_measurement(self, n_mes: int = 100, name: str = "", dir = ""):
        pmu = TestGateOk.pmu
        directory = os.path.dirname(os.path.realpath(__file__))

        save_dir = os.path.join(directory, dir)
        # TestGateOk.configure_node()
        result = []
        i = 0
        j = 0
        while i < n_mes or j < n_mes:
            try:
            
            # for i in range(n_mes):
                recv = pmu.recv_force()
                if recv.actuator_id == 1:
                    i +=1
                    print(f"got {i} msg {recv}")
                if recv.actuator_id == 0:
                    j +=1
                    print(f"got {j} msg {recv}")
                result.append(recv)
            except:
                continue
        results = []
        for i, res in enumerate(result):
            ptc = res.power_rating_pct
            force = res.force
            position = res.position
            id = res.actuator_id
            results.append({"ptc": ptc, "force": force, "position": position, "actuator_id": id, "timestamp": time.time()})
        pd.DataFrame(results).to_csv(f"{save_dir}/{name}.csv", index=False)



def main():
    test = TestGateOk()
    test.get_force_measurement(name="0.00", dir="tests_data/broken_optical_pair_metalic_barrier_with_black_rubber_from_1.1_to_2.0/reverse_0.00")
#     cmd = ["pytest", os.path.abspath(__file__)]
#     cmd += ["--tb=no"]  # No traceback at all
#     cmd += ["-v"]  # Increase verbosity
#     cmd += ["-W", "ignore::DeprecationWarning"]  # Ignore specific warnings
#     cmd += sys.argv[1:]  # Forward optional user flags
#     print(len(cmd))
#     print(cmd)
#     sys.exit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
