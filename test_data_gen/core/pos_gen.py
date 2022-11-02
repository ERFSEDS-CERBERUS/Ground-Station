"""
Position Generator
Version: 1.0.0
Author(s): Paul Conway

Description: This file generates a series of points based off the parameters contained in a JSON file.
The points follow a parabolic trajectory assuming standard gravity and zero air resistance
"""

# Formatted with Black, the uncompromising Python code formatter.

import json
import os
import math
import pandas as pd


def generate(json_path):
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        a = json_data["x_weight"]
        b = json_data["y_weight"]
        c = 9.80665  # Standard gravitational acceleration
        h = json_data["altitude"]

        p0 = 101325  # N/m^2 - Pressure at sea level
        T0 = 288.15  # K - Temperature at sea level

        noise_level = json_data["noise_level"]
        json_name = json_data["json_name"]
        steps_per_second = json_data["steps_per_second"]
        message_num = 0
    df = pd.DataFrame(
        columns=["message_num", "time", "x_pos", "y_pos", "z_pos", "pressure"]
    )
    # df.to_csv(os.path.join(os.path.dirname(json_path), os.path.pardir,'generated', json_name +'.csv'), index=False)
    root = math.sqrt(h / c)
    # range is defined such that the flight goes from 1 second before launch to 1 second after it contacts ground
    for time_val in range(
        -steps_per_second, math.ceil(2 * steps_per_second * root + steps_per_second), 1
    ):
        time_stamp = (
            time_val / steps_per_second
        ) - root  # It was easier to define the curve such that apoapsis is at t=0
        x_pos = a * (time_stamp + root)
        y_pos = b * (time_stamp + root)
        z_pos = h - (c * (time_stamp ** 2))
        pressure = p0 * (
            (1 - 0.0065 * (z_pos / T0)) ** 5.2561
        )  # ISA pressure formula - http://fisicaatmo.at.fcen.uba.ar/practicas/ISAweb.pdf (P. 5, Eq. 7)
        # TODO: Move the below z position correction
        message_num = message_num + 1
        if z_pos > 0:  # Needed in case z becomes negative
            x_last = x_pos
            y_last = y_pos
            z_last = z_pos
        elif (
            message_num > 1
        ):  # If z < 0 later in flight, locks the current position (rocket has hit the ground)
            x_pos = x_last
            y_pos = y_last
            z_pos = 0
        elif (
            message_num <= 1
        ):  # If z < 0 for values of t close to the start, should be ignored and position should be 0
            x_pos = x_last = 0
            y_pos = y_last = 0
            z_pos = z_last = 0
        if math.remainder(message_num, steps_per_second) == 0:
            print(
                str(message_num / steps_per_second) + " seconds of data generated"
            )  # Prints message for every second of flight generated
        df = df.append(
            pd.Series(
                [message_num, (time_stamp + (root) + 1), x_pos, y_pos, z_pos, pressure],
                index=df.columns,
            ),
            ignore_index=True,
        )
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print('Position data generation complete!')
    csv_path = os.path.abspath(
        os.path.join(
            os.path.dirname(json_path), os.path.pardir, "generated", json_name + ".csv"
        )
    )
    df.to_csv(
        csv_path,
        index=False,
    )
    print('Position data saved to file: ' + csv_path)

    return json_name + '.csv'

def generate_real(json_path):
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        a = json_data["x_weight"]
        b = json_data["y_weight"]
        c = 9.80665  # Standard gravitational acceleration
        h = json_data["altitude"]
        p0 = 101325  # N/m^2 - Pressure at sea level
        T0 = 288.15  # K - Temperature at sea level
        noise_level = json_data["noise_level"]
        json_name = json_data["json_name"]
        steps_per_second = json_data["steps_per_second"]
        message_num = 0
    df = pd.DataFrame(
        columns=["message_num", "time", "x_pos", "y_pos", "z_pos", "pressure"]
    )
    # df.to_csv(os.path.join(os.path.dirname(json_path), os.path.pardir,'generated', json_name +'.csv'), index=False)
    root = math.sqrt(h / c)
    # range is defined such that the flight goes from 1 second before launch to 1 second after it contacts ground
    for time_val in range(
        -steps_per_second, math.ceil(2 * steps_per_second * root + steps_per_second), 1
    ):
        time_stamp = (
            time_val / steps_per_second
        ) - root  # It was easier to define the curve such that apoapsis is at t=0
        x_pos = a * (time_stamp + root)
        y_pos = b * (time_stamp + root)
        z_pos = h - (c * (time_stamp ** 2))
        pressure = p0 * (
            (1 - 0.0065 * (z_pos / T0)) ** 5.2561
        )  # ISA pressure formula - http://fisicaatmo.at.fcen.uba.ar/practicas/ISAweb.pdf (P. 5, Eq. 7)
        # TODO: Move the below z position correction
        message_num = message_num + 1
        if z_pos > 0:  # Needed in case z becomes negative
            x_last = x_pos
            y_last = y_pos
            z_last = z_pos
        elif (
            message_num > 1
        ):  # If z < 0 later in flight, locks the current position (rocket has hit the ground)
            x_pos = x_last
            y_pos = y_last
            z_pos = 0
        elif (
            message_num <= 1
        ):  # If z < 0 for values of t close to the start, should be ignored and position should be 0
            x_pos = x_last = 0
            y_pos = y_last = 0
            z_pos = z_last = 0
        if math.remainder(message_num, steps_per_second) == 0:
            print(
                str(message_num / steps_per_second) + " seconds of data generated"
            )  # Prints message for every second of flight generated
        df = df.append(
            pd.Series(
                [message_num, (time_stamp + (root) + 1), x_pos, y_pos, z_pos, pressure],
                index=df.columns,
            ),
            ignore_index=True,
        )
    
    for time_stamp in range(math.ceil(steps_per_second*60)):
        time_val = time_stamp / steps_per_second
        if time_val <= 1:
            x_pos = 0
            y_pos = 0
            z_pos = 0
        else:
            pass
        

        pressure = p0 * (
            (1 - 0.0065 * (z_pos / T0)) ** 5.2561
        ) 
        # Writing Data
        df = df.append(
            pd.Series(
                [message_num, (time_stamp + (root) + 1), x_pos, y_pos, z_pos, pressure],
                index=df.columns,
            ),
            ignore_index=True,

        )
        

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print('Position data generation complete!')
    csv_path = os.path.abspath(
        os.path.join(
            os.path.dirname(json_path), os.path.pardir, "generated", json_name + ".csv"
        )
    )
    df.to_csv(
        csv_path,
        index=False,
    )
    print('Position data saved to file: ' + csv_path)

    return json_name + '.csv'
