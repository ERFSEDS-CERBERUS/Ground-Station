import numpy as np

def calc_accel_mag(accel_arr):
    accel_mag_arr = np.zeros((len(accel_arr[0]),1))
    for index in range (len(accel_arr[0])):
        x_accel_arr = accel_arr[0]
        x_accel = x_accel_arr[index]

        y_accel_arr = accel_arr[1]
        y_accel = y_accel_arr[index]

        z_accel_arr = accel_arr[2]
        z_accel = z_accel_arr[index]
        
        accel_mag_arr[index] = ((((x_accel)**2) + ((y_accel)**2) + ((z_accel)**2))**0.5)

    return accel_mag_arr

def calc_time(accel_arr, time_arr, noise_floor=0.0005):
    t0 = 0
    tb = 0
    accel_mag_arr = calc_accel_mag(accel_arr)

    # Find t0 with noise floor of 0.0005 m/s^2
    for index in range(len(accel_mag_arr)):
        accel_mag = accel_mag_arr[index]
        if(accel_mag>=noise_floor):
            t0 = time_arr[index]
            break
    
    # Find tb
    max_accel = 0
    max_accel_time = 0
    for index in range(len(accel_mag_arr)):
        accel_mag = accel_mag_arr[index]
        if(accel_mag>max_accel):
            max_accel = accel_mag
            max_accel_time = time_arr[index]

    tb = max_accel_time - t0

    out_arr = np.zeros((2,1))
    out_arr[0] = t0
    out_arr[1] = tb

    return out_arr