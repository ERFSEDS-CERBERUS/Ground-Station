import numpy as np

def calculate_mass(t, m_i, m_f, t_S, t_B):
    mass = (((m_f-m_i)/(t_B-t_S))*(t-t_B))+m_i
    return mass

def calculate_force(t, a, m_i, m_f, B, t_S=1):
    """
    Inputs:
        t ............... numpy array [t]
        a ............... numpy array [[x_accel],[y_accel],[z_accel]]
        m_i ............. float value for initial mass
        m_f ............. float value for final mass
        B ............... float value for burn time
        t_S ............. float value representing the time when acceleration increases rapidly
    Returns:
        numpy array [[x_force],[y_force],[z_force]]
    Raises:
        None
    """

    print("Calculating force...")

    t_B = t_S + B
    force_arr = np.array([np.zeros([len(t),1]),
                             np.zeros([len(t),1]),
                             np.zeros([len(t),1])])
    temp_arr = np.zeros([len(t),1])

    for index in range(len(a[0])):
        x_accel_arr = a[0]
        x_accel = x_accel_arr[index]
        mass = calculate_mass(t[index], m_i, m_f, t_S, t_B)
        temp_arr[index] = mass * x_accel
    force_arr[0] = temp_arr

    for index in range(len(a[1])):
        y_accel_arr = a[1]
        y_accel = y_accel_arr[index]
        mass = calculate_mass(t[index], m_i, m_f, t_S, t_B)
        temp_arr[index] = mass * y_accel
    force_arr[1] = temp_arr

    for index in range(len(a[2])):
        z_accel_arr = a[2]
        z_accel = z_accel_arr[index]
        mass = calculate_mass(t[index], m_i, m_f, t_S, t_B)
        temp_arr[index] = mass * z_accel
    force_arr[2] = temp_arr
    
    print("Force calculation complete!")

    return force_arr