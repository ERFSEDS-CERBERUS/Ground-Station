"""
Installs nonstandard module dependancies
Version: 1.0.0
Author(s): Paul Conway

Description: Installs required modules not in the standard library.
Pulls the list of non standrd libraries from requirements.txt
"""

import subprocess
import sys
import importlib
import os


def install(module):
    # Creates a subprocess to install module
    # Essentially running the command "python3 -m pip install <module_name>"
    subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    return None


def check_module(package):
    # Checks to see if the specified module is installed
    if importlib.util.find_spec(package) == None:
        return False
    else:
        return True


def setup():
    # Opens requirements file and finds list of required non standard modules
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt'),
        'r',
    ) as req_file:
        req_list = []  # Will be populated in the loop
        reqed = False  # Marks when the required module section starts and ends
        text_lines = req_file.readlines()
        for line in text_lines:
            if line.rstrip('\n') == '# Start of dependancy list':
                reqed = True
            elif line.rstrip('\n') == '# End of dependancy list':
                reqed = False
            if reqed == True:
                req_list.append(line.rstrip('\n'))
        for list_index in range(len(req_list)):
            if req_list[list_index] != '# Start of dependancy list':
                if (
                    check_module(req_list[list_index]) == False
                ):  # Checks to see if module is already installed
                    install(req_list[list_index])


if __name__ == '__main__':
    setup()
# df1 = df1.assign(e=pd.Series(np.random.randn(sLength)).values)
# df = df.assign('column_name'=column_data)
