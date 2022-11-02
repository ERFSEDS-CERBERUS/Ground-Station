import numpy as np
import pandas as pd
import os
import json

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

            print("Place the JSON data file in the 'raw_data' folder")
            print("Input the exact name of the file you wish to process\nExample: foo_Bar.json\n")
            f_name = input("File name: ")

            print("Attempting data input from JSON file...")

            f = open("/home/pciii/nova-ground-station-sw/post_flight_analysis/raw_data/" + f_name, 'r')

            data = json.load(f)

            print("Data input from JSON sucessful!\nPrinting out data...")


            for i in data:
                print(str(i))


            # Determining flight time
            print("Determing timestamp of each data point...")
            time_raw = np.zeros((len(data)),)
            flight_time = 0
            tps = 1024
            max_tps = tps
            for i,v in enumerate(data):
                flight_time = flight_time + (v['ticks_since_last_message'] / tps)
                time_raw[i] = flight_time
                if list(v['data'].keys()) == ['TicksPerSecond']:
                    ntps = v['data']['TicksPerSecond']
                    if ntps > tps:
                        max_tps = ntps
                    tps = ntps
            print("Time stamping complete!\nTotal flight time (s): " + str(flight_time))
            # This is done


            # Generating zeros array for each data type
            resolution = 100 # number of subdivisions per second
            print("Generating zeros arrays for each data field at " + str(resolution) + "subintervals per second\nTotal data points per field: " + str(resolution*flight_time))
            print("Generating time zeros array...")
            time = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("Time zeros array generated!\nGenerating low G arrays...")
            low_G_x = np.zeros(int((np.ceil(resolution*flight_time)),))
            low_G_y = np.zeros(int((np.ceil(resolution*flight_time)),))
            low_G_z = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("Low G zeros arrays generated!\nGenerating high G arrays...")
            high_G_x = np.zeros(int((np.ceil(resolution*flight_time)),))
            high_G_y = np.zeros(int((np.ceil(resolution*flight_time)),))
            high_G_z = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("High G arrays generated!\nGenerating pressure array...")
            pressure = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("Pressure array generated!\nGenerating temperature array...")
            temperature = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("Temperature array generated!\nGenerating gyro arrays...")
            gyro_x = np.zeros(int((np.ceil(resolution*flight_time)),))
            gyro_y = np.zeros(int((np.ceil(resolution*flight_time)),))
            gyro_z = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("Gyro arrays generated!\nGenerating magnotometer arrays...")
            magno_x = np.zeros(int((np.ceil(resolution*flight_time)),))
            magno_y = np.zeros(int((np.ceil(resolution*flight_time)),))
            magno_z = np.zeros(int((np.ceil(resolution*flight_time)),))
            print("Magnetometer arrays generated!\nZeros array generating complete!")
            # This is done


            # Generating time values
            print("Populating time array...")
            for i,_ in enumerate(time):
                time[i] = i/resolution
            print("Time array population complete!")
            # This is done


            # Generating high G values
            print("Populating high G arrays...")
            # Getting list of all high G acceleration data points
            high_G_points = 0
            for _,v in enumerate(data):
                if list(v['data'].keys()) == ['HighGAccelerometerData']:
                    high_G_points = high_G_points + 1
            high_G_x_raw = np.zeros((high_G_points),)
            high_G_y_raw = np.zeros((high_G_points),)
            high_G_z_raw = np.zeros((high_G_points),)
            high_G_time_raw = np.zeros((high_G_points),)
            high_G_points = 0
            for i,v in enumerate(data):
                if list(v['data'].keys()) == ['HighGAccelerometerData']:
                    high_G_x_raw[high_G_points] = v['data']['HighGAccelerometerData']['x']
                    high_G_y_raw[high_G_points] = v['data']['HighGAccelerometerData']['y']
                    high_G_z_raw[high_G_points] = v['data']['HighGAccelerometerData']['z']
                    high_G_time_raw[high_G_points] = time_raw[i]
                    high_G_points = high_G_points + 1
            print("Using linear interpolation to match high G to time array...")
            high_G_x = np.interp(time, high_G_time_raw, high_G_x_raw)
            high_G_y = np.interp(time, high_G_time_raw, high_G_y_raw)
            high_G_z = np.interp(time, high_G_time_raw, high_G_z_raw)
            print("High G arrays populated!")
            # This is done



            # Generating low G values
            print("Populating low G arrays...")
            print("Low G not implemented, setting equal to high G...")
            # Raw low G
            # Interpolated low G
            # Not implemented, setting all low G = high G
            low_G_x = high_G_x
            low_G_y = high_G_y
            low_G_z = high_G_z
            print("Low G arrays populated!")


            # Getting callibration constants
            print("Getting callibration constants...")
            for _,v in enumerate(data):
                if list(v['data'].keys()) == ['BarometerCalibration']:
                    pressure_sensitivity = v['data']['BarometerCalibration']['pressure_sensitivity']
                    pressure_offset = v['data']['BarometerCalibration']['pressure_offset']
                    temperature_coefficient_ps = v['data']['BarometerCalibration']['temperature_coefficient_ps']
                    temperature_coefficient_po = v['data']['BarometerCalibration']['temperature_coefficient_po']
                    reference_temperature = v['data']['BarometerCalibration']['reference_temperature']
                    temperature_coefficient_t = v['data']['BarometerCalibration']['temperature_coefficient_t']
            print("Obtained callibration constants!")


            # Generating pressure values
            print("Populating pressure array...")
            pressure_points = 0
            for _,v in enumerate(data):
                if list(v['data'].keys()) == ['BarometerData']:
                    pressure_points = pressure_points + 1
            pressure_raw = np.zeros((pressure_points),)
            pressure_time_raw = np.zeros((pressure_points),)
            pressure_points = 0
            for i,v in enumerate(data):
                if list(v['data'].keys()) == ['BarometerData']:
                    pressure_raw[pressure_points] = v['data']['BarometerData']['pressure']
                    pressure_time_raw[pressure_points] = time_raw[i]
                    pressure_points = pressure_points + 1
            print("Using linear interpolation to match pressure to time array...")
            pressure = np.interp(time, pressure_time_raw, pressure_raw)
            # TODO: Account for pressure callibration
            print("Note: If you are seeing this message it means that accounting for calibration has not been implemented")
            print("These pressure values are probably nonsense")
            print("Pressure array populated!")


            # Generating temperature values
            print("Populating temperature array...")
            temperature_points = 0
            for _,v in enumerate(data):
                if list(v['data'].keys()) == ['BarometerData']:
                    temperature_points = temperature_points + 1
            temperature_raw = np.zeros((temperature_points),)
            temperature_time_raw = np.zeros((temperature_points),)
            temperature_points = 0
            for i,v in enumerate(data):
                if list(v['data'].keys()) == ['BarometerData']:
                    temperature_raw[temperature_points] = v['data']['BarometerData']['temprature'] # *temprature*
                    temperature_time_raw[temperature_points] = time_raw[i]
                    v_points = temperature_points + 1
            print("Using linear interpolation to match pressure to time array...")
            pressure = np.interp(time, temperature_time_raw, temperature_raw)
            # TODO: Account for temperature callibration
            print("Note: If you are seeing this message it means that accounting for calibration has not been implemented")
            print("These temperature values are probably nonsense")
            print("Temperature array populated!")


            # Generating gyro values
            print("Populating gyro arrays...")
            print("This is not implemented yet, so all of these values are zeros")
            print("Gyro arrays populated!")


            # Generating magnetometer values
            print("Populating magnotometer arrays...")
            print("This is not implemented yet, so all of these values are zeros")
            print("Magnetometer arrays populated!")


            print("Closing JSON file...")
            f.close()

            print("\n\n\nData input process complete! Returning data to main program...")

            # t|axl|ayl|azl|axh|ayh|azh|wx|wy|wz|Ex|Ey|Ez|P |T
            # 0| 1 | 2 | 3 | 4 | 5 | 6 | 7| 8| 9|10|11|12|13|14

            data_out = np.zeros((len(time),15))
            for i,v in enumerate(time):
                data_out[i,0] = v
                data_out[i,1] = low_G_x[i]
                data_out[i,2] = low_G_y[i]
                data_out[i,3] = low_G_z[i]
                data_out[i,4] = high_G_x[i]
                data_out[i,5] = high_G_y[i]
                data_out[i,6] = high_G_z[i]
                data_out[i,7] = gyro_x[i]
                data_out[i,8] = gyro_y[i]
                data_out[i,9] = gyro_z[i]
                data_out[i,10] = magno_x[i]
                data_out[i,11] = magno_y[i]
                data_out[i,12] = magno_z[i]
                data_out[i,13] = pressure[i]
                data_out[i,14] = temperature[i]
            meta_out = None

            return (data_out, meta_out)
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

