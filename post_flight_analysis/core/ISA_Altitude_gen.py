"""
ISA Altitude Analysis
Version: 1.0.0
Author(s): Alijah McDonald, Eric Yoerg

Description: This file imports generated barometric pressure data from numpy array and converts
pressure to pressure altitude, returning the data to pressure_alt.
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
import os

def ISA_altitude(pressure):

    #Define
    T_o = 288.15 #Mean sea level temperature rankine
    B = 0.0065 #lapse rate
    P_o = 101325 #Mean Sea level pressure
    R = 287.1
    g = 9.81
    alt = np.zeros((len(pressure),))
    print(str(alt))

    #Convert pressure to pressure altitude and store inside Pressure_alt
    for x in range(len(pressure)):
        alt[x] = (T_o/B)*(1-((pressure[x]/P_o)**((R*B)/g)))
        #print(str(pressure))
        
    return alt







    




