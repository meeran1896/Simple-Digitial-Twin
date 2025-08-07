
from flask import Flask, jsonify
from components import Tank, Pump1, Pump2, Valve, Pressure
import threading
import time,random

app = Flask(__name__)

import random
import time

class Simulator:
    def __init__(self, level):
        self.level = level
        self.L_T1 = Tank(hh=1000, high=800, low=300, level=self.level)
        self.PU1 = Pump1()
        self.PU2 = Pump2()
        self.V1 = Valve()
        self.JP1 = Pressure()
        self.JPV1 = Pressure()

        self.prev_state = 1
        self.mode = "fill"

        self.possible_states = {
            1: (self.PU1.run(), self.PU2.run(), self.V1.open(), self.JP1.flow(), self.JPV1.valve_flow(), 2),
            2: (self.PU1.run(), self.PU2.run(), self.V1.close(), self.JP1.flow(), self.JPV1.noflow(), 2),
            3: (self.PU1.run(), self.PU2.stop(), self.V1.open(), self.JP1.half_flow(), self.JPV1.flow(), 0.75),
            4: (self.PU1.stop(), self.PU2.stop(), self.V1.open(), self.JP1.noflow(), self.JPV1.flow(), -1),
            5: (self.PU1.stop(), self.PU2.stop(), self.V1.close(), self.JP1.noflow(), self.JP1.noflow(), 0)
        }

        self.current_state = 0
        self.current_level = self.L_T1.current_level
        self.plant_state = None

    def run_step(self):
        tank_state = self.L_T1.get_tank_state()[0]

        if tank_state == 'HH':
            self.mode = "drain"

        elif tank_state == 'L' and self.mode == "drain":
            self.mode = "fill"

        if self.mode == "drain":
            self.current_state = 4

        elif tank_state == 'L':
            self.current_state = 2

        elif tank_state == 'H':
            self.current_state = 3

        elif tank_state == 'N' and self.L_T1.current_level > 0.95 * self.L_T1.hh:
            self.current_state = 1

        else:
            self.current_state = self.prev_state

        self.plant_state = self.possible_states[self.current_state]
        self.prev_state = self.current_state
        self.L_T1.water_input(self.plant_state[5])
        self.current_level = self.L_T1.current_level
        p_state1, p_state2, v_state = self.plant_state[0], self.plant_state[1], self.plant_state[2]
        jp_state = self.plant_state[3] + random.uniform(0.01, 0.10) if self.plant_state[3] != 0 else self.plant_state[3]
        jpv1_state = self.plant_state[4] + random.uniform(0.01, 0.10) if self.plant_state[4] != 0 else self.plant_state[4]

        return {
            "tank_level": round(self.current_level, 2),
            "tank_state": tank_state,
            "mode": self.mode,
            "pump1_state": p_state1,
            "pump2_state": p_state2,
            "valve_state": v_state,
            "JP_state": jp_state,
            "JPV1_state": jpv1_state,
            "timestamp": int(time.time() * 1000)
        }


# Create global instance
sim = Simulator(level=550)
def simulate_continuously():
    while True:
        result = sim.run_step()
        print(result)
        time.sleep(1)

@app.route("/simulate", methods=["GET"])
def simulate_step():
    result = sim.run_step()
    return jsonify(result)

@app.route("/reset", methods=["POST"])
def reset_simulator():
    global sim
    sim = Simulator(level=0)
    return jsonify({"message": "Simulator reset."})

if __name__ == "__main__":
    t = threading.Thread(target=simulate_continuously, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5001)
