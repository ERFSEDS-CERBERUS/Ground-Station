import numpy as np
import matplotlib.pyplot as plt


def plot_gen(time, omega):
    """
    Returns a plot object showing angular velocity with respect to time

    return = plot_gen(time,omega)
    time   : list-like type
    omegas : list-like type
    """

    # Checking to see if input is a list
    # if type(time) != 'list' or type(omega) != 'list':

    x_val = np.linspace(0, np.pi, 100)
    return plt.plot(x_val, np.sin(x_val))


fig, axis = plt.subplots(1, 2, figsize=(15, 5))

plotted = plot_gen(None, None)
plotted2 = plot_gen(None, None)

# axis[0].plot(plotted)
# axis[1].plot(plotted2)

fig.add_subplot(plotted)
