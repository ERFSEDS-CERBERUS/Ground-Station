"""
TODO: Docstring
"""

# Formatted with Black, the uncompromising Python code formatter.

# Imports
import matplotlib.pyplot as plt

import numpy as np
import core.data_in
import core.integrate

# import core.ang_vel
import core.ISA_Altitude_gen
import core.rotation
import core.stitches
import core.force_calc
import core.impulse_calc
import core.time_calc


def main():
    # Imports data. This will return a stuct containing the data in SI units and any metadata
    base_data, mdata = core.data_in.extract(mode="live")
    threshold = mdata["accel_range"]
    m_i = mdata["m_i"]
    m_f = mdata["m_f"]
    C_D = mdata["C_D"]
    A_f = mdata["A_f"]
    burn_time = mdata["burn_time"]
    # TODO: Add rest of metadata

    time = base_data[:, 0]

    accel_low = np.vstack((base_data[:, 1], base_data[:, 2], base_data[:, 3]))
    accel_high = np.vstack((base_data[:, 4], base_data[:, 5], base_data[:, 6]))
    accel = core.stitches.stitch(time, accel_low, accel_high, threshold)
    accel_mag = [
        np.sqrt(accel[0][i] ** 2 + accel[1][i] ** 2 + accel[2][i] ** 2)
        for i, _ in enumerate(time)
    ]

    omega = np.vstack((base_data[:, 7], base_data[:, 8], base_data[:, 9]))
    compass = np.vstack((base_data[:, 10], base_data[:, 11], base_data[:, 12]))
    phi = np.asarray(
        (
            core.integrate.left_sum(time, omega[0]),
            core.integrate.left_sum(time, omega[1]),
            core.integrate.left_sum(time, omega[2]),
        )
    )
    phi_mag = [
        np.sqrt(phi[0][i] ** 2 + phi[1][i] ** 2 + phi[2][i] ** 2)
        for i, _ in enumerate(time)
    ]
    pressure = base_data[:, 13]

    pressure_alt = core.ISA_Altitude_gen.ISA_altitude(pressure)
    # TODO: Calibrate pressure
    # TODO: Calibrate angular position

    # Rotating vectors
    accel = core.rotation.rotate(omega, time, accel)

    vel_x = core.integrate.left_sum(time, accel_low[0])
    vel_y = core.integrate.left_sum(time, accel_low[1])
    vel_z = core.integrate.left_sum(time, accel_low[2])
    vel = np.asarray([vel_x, vel_y, vel_z])
    vel_mag = [
        np.sqrt(vel[0][i] ** 2 + vel[1][i] ** 2 + vel[2][i] ** 2)
        for i, _ in enumerate(time)
    ]

    pos_x = core.integrate.left_sum(time, vel[0])
    pos_y = core.integrate.left_sum(time, vel[1])
    pos_z = core.integrate.left_sum(time, vel[2])
    pos = np.asarray([pos_x, pos_y, pos_z])
    xy_pos = [np.sqrt(pos[0][i] ** 2 + pos[1][i] ** 2) for i, _ in enumerate(time)]
    pos_mag = [
        np.sqrt(pos[0][i] ** 2 + pos[1][i] ** 2 + pos[2][i] ** 2)
        for i, _ in enumerate(time)
    ]
    alt_diff = [v - pressure_alt[i] for i, v in enumerate(pos_z)]

    force = core.force_calc.calculate_force(time, accel, m_i, m_f, burn_time)
    force_mag = [
        np.sqrt(force[0][i] ** 2 + force[1][i] ** 2 + force[2][i] ** 2)
        for i, _ in enumerate(time)
    ]

    # TODO: Calculate aero forces

    # TODO: Calculate impulse
    # ts_tb_arr = np.asarray(core.time_calc.calc_time(accel, time))
    # impulse = core.impulse_calc.calculate_impulse(m_i, m_f, vel, ts_tb_arr, time)[1]
    # TODO: Calculate ISA and accel calculated altitude divergence

    # Plottting happens here:

    print("Generating plots...")

    # Acceleration (x, y, x, mag w.r.t. t)
    plt.subplot(3, 3, 1)
    plt.plot(time, accel[0])
    plt.plot(time, accel[1])
    plt.plot(time, accel[2])
    plt.plot(time, accel_mag)
    plt.legend(["x", "y", "z", "net"])
    plt.title("Acceleration, m/s^2")

    # Down Range (x, y, mag w.r.t. t)
    plt.subplot(3, 3, 2)
    plt.plot(time, pos_x)
    plt.plot(time, pos_y)
    plt.plot(time, xy_pos)
    plt.legend(["x", "y", "net"])
    plt.title("Down Range, m")

    # Vertical Position, pressure altitude (z, hp, w.r.t. t)
    plt.subplot(3, 3, 3)
    plt.plot(time, alt_diff)
    plt.legend(["diff"])
    plt.title("pos_z - press. alt, m")

    # Velocity (x, y, z, mag w.r.t. t)
    plt.subplot(3, 3, 4)
    plt.plot(time, vel_x)
    plt.plot(time, vel_y)
    plt.plot(time, vel_z)
    plt.plot(time, vel_mag)
    plt.legend(["x", "y", "z", "net"])
    plt.title("Velocity, m/s")

    # Altitude (from Pressure and acceleration w.r.t. t)
    plt.subplot(3, 3, 5)
    plt.plot(time, pos_z)
    plt.plot(time, pressure_alt)
    plt.legend(["accel_alt, pressure_alt"])
    plt.title("Altitude, m")

    # Position (x, y, z w.r.t. t)
    plt.subplot(3, 3, 7)
    plt.plot(time, pos_x)
    plt.plot(time, pos_y)
    plt.plot(time, pos_z)
    plt.plot(time, xy_pos)
    plt.legend(["x", "y", "z", "net"])
    plt.title("Position, m")

    # Force (x, y, z w.r.t. t)
    plt.subplot(3, 3, 8)
    plt.plot(time, force[0])
    plt.plot(time, force[1])
    plt.plot(time, force[2])
    plt.plot(time, force_mag)
    plt.legend(["x", "y", "z", "net"])
    plt.title("Force, N")

    # Angle from Vertical (x,y,z w.r.t. t)
    plt.subplot(3, 3, 6)
    plt.plot(time, phi[0])
    plt.plot(time, phi[1])
    plt.plot(time, phi[2])
    plt.legend(["x", "y", "z"])
    plt.title("Vertical Angle, phi")

    # Table of Values goes here
    max_accel = np.around(np.max(accel_mag), decimals=3)
    max_accel_time = np.around(time[np.argmax(accel_mag)], decimals=3)

    max_force = np.around(np.max(force_mag), decimals=3)
    max_force_time = np.around(time[np.argmax(force_mag)], decimals=3)

    max_vel = np.around(np.max(vel_mag), decimals=3)
    max_vel_time = np.around(time[np.argmax(vel_mag)], decimals=3)

    max_alt = np.around(np.max(pos_z), decimals=3)
    max_alt_time = np.around(time[np.argmax(pos_z)], decimals=3)

    max_downrange = np.around(np.max(xy_pos), decimals=3)
    max_downrange_time = np.around(time[np.argmax(xy_pos)], decimals=3)

    max_angle = np.around(np.max(phi_mag), decimals=3)
    max_angle_time = np.around(time[np.argmax(phi_mag)], decimals=3)

    # total_impulse = np.around(np.max(impulse),decimals=3)
    # total_impulse_time = np.around(time[np.argmax(impulse)],decimals=3)

    ax = plt.subplot(3, 3, 9)
    plt.title("Max Values")
    data = [
        ["Max Accel", str(max_accel) + " m/s^2", str(max_accel_time) + " s"],
        ["Max Force", str(max_force) + " N", str(max_force_time) + " s"],
        ["Max Velocity", str(max_vel) + " m/s", str(max_vel_time) + " s"],
        ["Max Altitude", str(max_alt) + " m", str(max_alt_time) + " s"],
        ["Max Downrange", str(max_downrange) + " m", str(max_downrange_time) + " s"],
        ["Total Impulse", "?????" + " N*s", "?????" + " s"],
        ["Max Angle", str(max_angle) + " rad", str(max_angle_time) + " s"],
    ]
    ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=data, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    # Plot Formatting
    plt.tight_layout(pad=0.5)
    print("Displaying all plots...")
    plt.show()

    if input("Display plots individually? (y/n) ").lower() == "y":
        print("Displaying plots individually...")
        print("Plot 1/9")
        plt.plot(time, accel[0])
        plt.plot(time, accel[1])
        plt.plot(time, accel[2])
        plt.plot(time, accel_mag)
        plt.legend(["x", "y", "z", "net"])
        plt.title("Acceleration, m/s^2")
        plt.show()

        print("Plot 2/9")
        plt.plot(time, pos_x)
        plt.plot(time, pos_y)
        plt.plot(time, xy_pos)
        plt.legend(["x", "y", "net"])
        plt.title("Down Range, m")
        plt.show()

        print("Plot 3/9")
        plt.plot(time, alt_diff)
        plt.legend(["diff"])
        plt.title("pos_z - press. alt, m")
        plt.show()

        print("Plot 4/9")
        plt.plot(time, vel_x)
        plt.plot(time, vel_y)
        plt.plot(time, vel_z)
        plt.plot(time, vel_mag)
        plt.legend(["x", "y", "z", "net"])
        plt.title("Velocity, m/s")
        plt.show()

        print("Plot 5/9")
        plt.plot(time, pos_z)
        plt.plot(time, pressure_alt)
        plt.legend(["accel_alt, pressure_alt"])
        plt.title("Altitude, m")
        plt.show()

        print("Plot 6/9")
        plt.plot(time, pos_x)
        plt.plot(time, pos_y)
        plt.plot(time, pos_z)
        plt.plot(time, xy_pos)
        plt.legend(["x", "y", "z", "net"])
        plt.title("Position, m")
        plt.show()

        print("Plot 7/9")
        plt.plot(time, force[0])
        plt.plot(time, force[1])
        plt.plot(time, force[2])
        plt.plot(time, force_mag)
        plt.legend(["x", "y", "z", "net"])
        plt.title("Force, N")
        plt.show()

        print("Plot 8/9")
        plt.plot(time, phi[0])
        plt.plot(time, phi[1])
        plt.plot(time, phi[2])
        plt.legend(["x", "y", "z"])
        plt.title("Vertical Angle, phi")
        plt.show()

        print("Plot 9/9")
        ax = plt.subplot(1, 1, 1)
        plt.title("Max Values")
        data = [
            ["Max Accel", str(max_accel) + " m/s^2", str(max_accel_time) + " s"],
            ["Max Force", str(max_force) + " N", str(max_force_time) + " s"],
            ["Max Velocity", str(max_vel) + " m/s", str(max_vel_time) + " s"],
            ["Max Altitude", str(max_alt) + " m", str(max_alt_time) + " s"],
            [
                "Max Downrange",
                str(max_downrange) + " m",
                str(max_downrange_time) + " s",
            ],
            ["Total Impulse", "?????" + " N*s", "?????" + " s"],
            ["Max Angle", str(max_angle) + " rad", str(max_angle_time) + " s"],
        ]
        ax.axis("tight")
        ax.axis("off")
        table = ax.table(cellText=data, loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(7)
        plt.show()

    return None


if __name__ == "__main__":
    main()
