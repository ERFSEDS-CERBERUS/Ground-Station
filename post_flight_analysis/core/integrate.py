"""
Author: Paul Conway

Performs various numeric integrations

TODO: Finish this dosstring
"""
import numpy as np

def left_sum(x,y):
    """
    Inputs:
        x, list-like type
        y, list-like type
    Return:
        list type
    Raises:
        IndexError if x and y have different sizes
    """

    print("Integrating data...")

    col_width = len(x)
    row_width = len(y)
    num_output = np.zeros([row_width,1])
    # TODO: dont require list type
    #if type(x) != 'list':
    #    x = list(x)
   # if type(y) != 'list':
       # y = list(y)

    if len(x) == len(y):
        num_sum = 0
        for n in range(row_width - 1):
            # Will handle changes in data timing
            delta = x[n+1] - x[n]
            num_sum = num_sum + (delta * y[n])
            num_output[n]= num_sum
        num_output[col_width - 1] = num_output[col_width - 2]
        print("Data integration complete!")
        return num_output
    else:
        raise IndexError("Array sizes must match")
