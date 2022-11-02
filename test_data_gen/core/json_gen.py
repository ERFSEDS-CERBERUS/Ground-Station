"""
JSON Generator
Version: 1.0.0
Author(s): Paul Conway

Description: This file generates a JSON file containing the given user inputs.
"""

# Formatted with Black, the uncompromising Python code formatter.

import json
import math



def generate(json_name, json_path):
    # TODO: input checking
    x_range = float(input("Specify a max X distance (m): "))
    y_range = float(input("Specify a max Y distance (m): "))
    altitude = float(input("Specify a max altitude (m): "))
    noise_level = float(input("Specify a noise level (m, not implemented): "))
    steps_per_second = int(input("Specify how many steps per second (int): "))
    notes = input("Notes: ")
    json_data = {
        "json_name": json_name[
            0:-5
        ],  # TODO: Use regex to get this from the json_path string
        "x_weight": (
            x_range / 2 * 
          .sqrt(9.80665 / altitude)
        ),  # Calculated based on standard gravity
        "y_weight": (
            y_range / 2 * math.sqrt(9.80665 / altitude)
        ),  # Calculated based on standard gravity
        "altitude": altitude,
        "noise_level": noise_level,
        "steps_per_second": steps_per_second,
        "notes": notes,
    }
    with open(json_path, "w") as outfile:
        json.dump(json_data, outfile)

    return None
