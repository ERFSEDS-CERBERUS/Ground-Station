import numpy as np
from .force_calc import calculate_mass
from .time_calc import calc_accel_mag as calc_momentum_mag
from .integrate import left_sum

def calculate_impulse(mass_i, mass_f, vel_arr, ts_tb_arr, time_arr):

    print("Calculating impulse...")

    t_S = ts_tb_arr[0]
    t_B = ts_tb_arr[1]
    t_S_index = 0
    t_B_index = 0
    x_momentum_arr = np.zeros([len(time_arr),1])
    y_momentum_arr = np.zeros([len(time_arr),1])
    z_momentum_arr = np.zeros([len(time_arr),1])

    for index in range(len(time_arr)):
        # TODO: Change comparing float to comparing to within range of float
        if(time_arr[index]==t_S):
            t_S_index = index
        elif(time_arr[index]==t_B):
            t_B_index = index
            break

    adjusted_time_length = t_B_index - t_S-index
    adjusted_time_arr = np.zeros([adjusted_time_length, 1])

    # Create new time array that starts at t_S instead of t_0
    for index in range(len(time_arr[0])):
        t = time_arr[index]
        i = 0
        if(t >= t_S and t <= t_B):
            adjusted_time_arr[i] = t
            i += 1

    # X momentum
    x_vel_arr = vel_arr[0]
    for index in range(len(vel_arr[0])):
        t = adjusted_time_arr[index]
        x_vel = x_vel_arr[index]
        x_momentum_arr[index] = calculate_mass(t, mass_i, mass_f, t_S, t_B) * x_vel

    # Y momentum
    y_vel_arr = vel_arr[1]
    for index in range(len(vel_arr[1])):
        t = adjusted_time_arr[index]
        y_vel = y_vel_arr[index]
        y_momentum_arr[index] = calculate_mass(t, mass_i, mass_f, t_S, t_B) * y_vel

    # Z momentum
    z_vel_arr = vel_arr[2]
    for index in range(len(vel_arr[2])):
        t = adjusted_time_arr[index]
        z_vel = z_vel_arr[index]
        z_momentum_arr[index] = calculate_mass(t, mass_i, mass_f, t_S, t_B) * z_vel
    
    momentum_arr = np.zeros([len(x_momentum_arr),3])
    momentum_arr[0] = x_momentum_arr
    momentum_arr[1] = y_momentum_arr
    momentum_arr[2] = z_momentum_arr

    momentum_mag_arr = calc_momentum_mag(momentum_arr)
    impulse_arr = left_sum(adjusted_time_arr, momentum_mag_arr)

    impulse_total = [v * adjusted_time_arr[1]-adjusted_time_arr[0] for _,v in enumerate(impulse_arr)]

    print("Impulse calculation complete!")

    return (impulse_arr, impulse_total)