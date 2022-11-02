import json
import os
import random
import pandas as pd

def EpicMoment(json_path, data_file_name, col_names):
    #pure_data has no random variations applied
    #col_name is a list of strings
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        alpha = json_data("noise_level")
    #import csv
    pure_data = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "local_data", "generated", data_file_name), usecols=col_list)
    for column in range(len(col_names)):
        column_name = col_names[column]
        #loop for each row in column (no head)
            #grab height
            #height = height + ((height * alpha * random.random()) - 0.5)
            #rewrite to the cell


