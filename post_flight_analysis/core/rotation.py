import numpy as np
from scipy.spatial.transform import Rotation as R


def rotate(omega, step, R_frame):
    """
    Expresses R_frame in terms of an inertial frame based on an angular velocity vector.
    Parameters:
        omega:
            Type: 3 element list
            Description: Each element contains a numpy array expressing angular velocity around a body fixed axis
            Units: rad/sec
        step:
            Type: list
            Description: Time at each point
            Units: sec
            TODO: Make this use an numpy array
        R_frame:
            Type: 3 element list
            Description: 0,1,2 elements contain the x,y,z components of a time varing vector in a body fixed frame
        nose_axis (optional):
            Type: string
            Values: 'x', 'y', 'z'
            Expressed which axis is pointing towards the nose.
            The remaining two axis will be oriented such that the frame is right-handed
    Outputs:
        Type: 3 element list
        Description: 0,1,2 elements contains the x,y,z components of the time varying vector in an inertial frame
    Raises:
        NotImplementedError:
            Cause: nose_axis was set to something other than "z"
    """

    print("Rotating coordinate frame...")

    out_frame = np.zeros((len(step),))
    RR_x = np.zeros((len(step),))
    RR_y = np.zeros((len(step),))
    RR_z = np.zeros((len(step),))

    delta_t = step[1] - step[0]

    # These are not really Euler angles (unless it's a special case where they happen to be)
    for n, s in enumerate(step):

        """
        alpha = omega[0][n] * delta_t
        beta = omega[1][n] * delta_t
        gamma = omega[2][n] * delta_t

        # roted = np.sqrt(alpha**2 + beta**2 + gamma**2) * deta_t

        # It's faster to do this once rather than compute these trig functions 12 times
        c_alpha = np.cos(alpha)
        s_alpha = np.sin(alpha)
        c_beta = np.cos(beta)
        s_beta = np.sin(beta)
        c_gamma = np.cos(gamma)
        s_gamma = np.sin(gamma)

        # Rotation matricies
        # Don't ask how I got these its fucking magic or something, or linear algebra...
        Q_1 = np.array([[1, 0, 0], [0, c_alpha, -s_alpha], [0, s_alpha, c_alpha]])
        Q_2 = np.array([[c_beta, 0, s_beta], [0, 1, 0], [-s_beta, 0, c_beta]])
        Q_3 = np.array([[c_gamma, -s_gamma, 0], [s_gamma, c_gamma, 0], [0, 0, 1]])
        # This matrix combines all rotations
        Q = np.matmul(np.matmul(Q_1, Q_2), Q_3)

        # quat = R.as_quat()

        """

        # I was debugging the rotation logic. This works too but I think it is slower

        in_frame = np.array(
            [float(R_frame[0][n]), float(R_frame[1][n]), float(R_frame[2][n])]
        )
        rot_vec = R.from_rotvec([omega[0][n], omega[1][n], omega[2][n]])
        in_frame = rot_vec.apply(in_frame)
        RR_x[n] = in_frame[0]
        RR_y[n] = in_frame[1]
        RR_z[n] = in_frame[2]

        """
        # Rotated vector
        raw_vec = [R_frame[0][n], R_frame[1][n], R_frame[2][n]]
        rot_vec = np.matmul(np.transpose(Q), raw_vec)
        RR_x[n] = rot_vec[0]
        RR_y[n] = rot_vec[1]
        RR_z[n] = rot_vec[2]
        """

    print("Coordinate frame rotation complete!")

    return [RR_x, RR_y, RR_z]
