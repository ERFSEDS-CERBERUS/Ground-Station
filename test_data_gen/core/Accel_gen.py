"""
Acceleration Generator
Version: 1.0.0
Author(s): Jackson Sackrider

Description: This file generates a collection of acceleration values for the x, y, and z-axis based off the parameters 
contained in a csv file.
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
import os

def Generate_Acceleration(csv_name): 
    def import_data(csv_name):
        #Define which files should be imported from the test data
        col_list = ["z_pos", "y_pos", "x_pos", 'pressure',"time", "x_velocity", "y_velocity", "z_velocity"]
        #Define the name of the test data csv and import it
        TestData = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "local_data", "generated", csv_name), usecols=col_list)
        #Gather all the info from the columns
        time, z_vel, y_vel, x_vel = TestData["time"], TestData["z_velocity"], TestData["y_velocity"], TestData["x_velocity"]
        #Call the function get_Velocity 
        get_Acceleration(z_vel, time, y_vel, x_vel, TestData, csv_name)


    def get_Acceleration(z_vel, time, y_vel, x_vel, TestData, csv_name):
            #Create a new data frame with the to be calculated columns
            df = pd.DataFrame(columns=["x_acceleration", "y_acceleration", "z_acceleration"])
            #Loop for every amount of times there is a change in time (run as long as there is data)
            for n in range(0, np.size(time) - 1):
                #Find the difference in time (the delta of time)
                delta_t = time[n+1] - time[n]
                #Calculate the three accelerations by finding delta position divided by delta_t
                z_acceleration = (z_vel[n + 1] - z_vel[n]) / delta_t
                x_acceleration = (x_vel[n + 1] - x_vel[n]) / delta_t
                y_acceleration = (y_vel[n + 1] - y_vel[n]) / delta_t
                #Add the calculated values to the columns to create an array
                df = df.append(pd.Series([x_acceleration, y_acceleration, z_acceleration], index=df.columns), ignore_index = True)
            #Add the old imported columns to the new data frame
            df['x_pos'] = list(TestData['x_pos'][1:])
            df['y_pos'] = list(TestData['y_pos'][1:])
            df['z_pos'] = list(TestData['z_pos'][1:])
            df['time'] = list(TestData['time'][1:])
            df['x_velocity'] = list(TestData['x_velocity'][1:])
            df['y_velocity'] = list(TestData['y_velocity'][1:])
            df['z_velocity'] = list(TestData['z_velocity'][1:])
            df['pressure'] = list(TestData['pressure'][1:])
            #Rearrange all the columns to the desired pattern
            df = df.reindex(['time','x_pos','y_pos','z_pos','pressure','x_velocity','y_velocity','z_velocity', 'x_acceleration', 'y_acceleration', 'z_acceleration'], axis='columns')
            #Export the new data frame arrays into the old csv, replacing the old with the new
            df.to_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "local_data", "generated", csv_name), index = False)

    #Call the beginning fucntion
    import_data(csv_name)




        
    
    
