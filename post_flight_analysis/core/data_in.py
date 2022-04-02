import numpy as np
import pandas as pd
import os

def extract(mode="live"):
    """
    Parameters:
        pl
    Outputs:
        pl
    Raises:
        None
    """
    match mode:
        case "live":
            # Get unprocessed data
            # TODO: grab raw data based on input parameters

            # Get parameters/metadata
            # TODO: Separate metadata from flight data.
            #   ISA correction
            #   Motor parameters
            #   Rocket parameters
            #   Sensor parameters

            # Convert raw sensor voltages to SI values if neccesary
            # TODO: Implement ability to translate from voltage to SI eqiv
            # TODO: Implement ability to change between modes.

            # Apply low pass filters
            # TODO: Implement low pass filters based in metadata and component specs

            pass
        case "test":
            # TODO: Implement
            # This is only for testing purposes. Will export pre-made data

            # This is just placeholder data. Better data should be made
            # t|axl|ayl|azl|axh|ayh|azh|wx|wy|wz|Ex|Ey|Ez|P
            # 0| 1 | 2 | 3 | 4 | 5 | 6 | 7| 8| 9|10|11|12|13
            # low-g threshold = 8 m/s
            rows = 15
            data = np.zeros((rows, 14))
            t = np.linspace(0, 3, rows)
            for n in range(len(t)):
                # time
                data[n, 0] = n
                # accel low
                data[n, 1] = 8 + n
                data[n, 2] = 7 + n
                data[n, 3] = np.exp(n)
                # accel high
                data[n, 4:7] = 15+(n*0.1)
                # angular accel
                data[n, 7:10] = 1000
                # compass
                data[n, 10:13] = 111
                # pressure
                data[n, 13] = 1000000

            # Metadata
            mdata = {
                "gyro_range" : 2000,
                "gyro_res" : 2000/(2**16),
                "accel_range" : 8,
                "accel_res" : 8/(2**16),
                "mag_range" : 2000,
                "mag_res" : 2000/(2**16),
                "C_D" : 1.1,
                "A_f" : 0.008,
                "m_i" : 10,
                "m_f" : 5,
                "burn_time" : 8,
                "P_0" : 101325,
                "T_0" : 277
            }
            return (data, mdata)
        case "from_file":
            #Define which files should be imported from the test data
            col_list = ["time","pressure","x_acceleration","y_acceleration","z_acceleration","x_angle","y_angle","z_angle"]
            #Define the name of the test data csv and import it
            TestData = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw_data", "yae.csv"), usecols=col_list)
            #Gather all the info from the columns
            time, pressure, x_accel, y_accel, z_accel, x_ang, y_ang, z_ang = TestData["time"], TestData["pressure"], TestData["x_acceleration"], TestData["y_acceleration"], TestData["z_acceleration"], TestData["x_angle"], TestData["y_angle"], TestData["z_angle"]
            # t|axl|ayl|azl|axh|ayh|azh|wx|wy|wz|Ex|Ey|Ez|P
            data = np.zeros((len(time),14))
            for i,v in enumerate(time):
                data[i,0] = v
                data[i,1] = x_accel[i]
                data[i,2] = y_accel[i]
                data[i,3] = z_accel[i]
                data[i,4] = x_accel[i]
                data[i,5] = y_accel[i]
                data[i,6] = z_accel[i]
                data[i,7] = x_ang[i]
                data[i,8] = y_ang[i]
                data[i,9] = z_ang[i]
                data[i,10] = 0
                data[i,11] = 0
                data[i,12] = 0
                data[i,13] = pressure[i]
            # Metadata
            mdata = {
                "gyro_range" : 2000,
                "gyro_res" : 2000/(2**16),
                "accel_range" : 8,
                "accel_res" : 8/(2**16),
                "mag_range" : 2000,
                "mag_res" : 2000/(2**16),
                "C_D" : 1.1,
                "A_f" : 0.008,
                "m_i" : 10,
                "m_f" : 5,
                "burn_time" : 8,
                "P_0" : 101325,
                "T_0" : 277
            }
            return (data, mdata)
        case _:
            # TODO: Raise exception
            pass

    # Return struct containing flight data and metadata
    return (data, mdata)

# Test
