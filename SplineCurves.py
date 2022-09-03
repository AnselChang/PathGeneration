"""Code generously provided by Yusef Simsek"""

# Return position at t, 0 < t < 1
def getSplinePoint(t, p1, p2, p3, p4):
    tt = t * t
    ttt = tt * t

    q1 = -ttt+ 2 * tt - t
    q2 =  3 * ttt - 5* tt + 2
    q3 = -3 * ttt + 4 * tt + t
    q4 = ttt - tt

    tx = 0.5 * (p1[0] * q1 + p2[0] * q2 + p3[0] * q3 + p4[0] * q4)
    ty = 0.5 * (p1[1] * q1 + p2[1] * q2 + p3[1] * q3 + p4[1] * q4)

    return [tx, ty]

# Return position at t, 0 < t < 1
def getSplineGradient(t, p1, p2, p3, p4):
    tt = t * t
    ttt = tt * t

    q1 = -3 * tt + 4 * t - 1
    q2 =  9 * tt - 10 * t
    q3 = -9 * tt + 8 * t + 1
    q4 = 3 * tt - 2 * t

    tx = 0.5 * (p1[0] * q1 + p2[0] * q2 + p3[0] * q3 + p4[0] * q4)
    ty = 0.5 * (p1[1] * q1 + p2[1] * q2 + p3[1] * q3 + p4[1] * q4)

    return [tx, ty]
