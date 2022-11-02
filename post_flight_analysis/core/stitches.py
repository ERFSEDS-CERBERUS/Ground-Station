"""
TODO: Docstring
"""
import numpy as np
def stitch(time,low,high,threshold):
    """
    Inputs:
        time .................. numpy array [x]
        low ................... numpy array [[y_1],[y_2],[y_3]]
        high .................. numpy array [[y_1],[y_2],[y_3]]
        threshold ............. float value where low values will be replaced
        dim (opt, defalt=3) ... number of dependant variables (y-values)
    Returns:
        numpy array [[y_1],[y_2],[y_3]]
    Raises:
        None
    """
    # 1x3
    # row x col
    # n x 1
    temp_arr = np.zeros([len(time),1])
    
    stitch_arr = np.array([np.zeros([len(time),1]),
                             np.zeros([len(time),1]),
                             np.zeros([len(time),1])])
    
    for index in range(len(low[0])):
        lowxs = low[0]
        low_x = lowxs[index]
        high_x = high[0][index]

        if(low_x>=threshold):
            temp_arr[index]=high_x
        else:
            temp_arr[index]=low_x

    stitch_arr[0] = temp_arr

    for index in range(len(low[1])):
        lowys = low[1]
        low_y = lowys[index]
        high_y = high[1][index]

        if(low_y>=threshold):
            temp_arr[index]=high_y
        else:
            temp_arr[index]=low_y

    stitch_arr[1] = temp_arr

    for index in range(len(low[2])):
        lowzs = low[2]
        low_z = lowzs[index]
        high_z = high[2][index]

        if(low_z>=threshold):
            temp_arr[index]=high_z
        else:
            temp_arr[index]=low_z

    stitch_arr[2] = temp_arr
    
    return stitch_arr