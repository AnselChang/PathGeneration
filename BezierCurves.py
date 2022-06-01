# Return position at t, 0 < t < 1
def getBezierPoint(t: float, p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> list:
    """Returns the point on a bezier curve defined by the four points on location 0<=t<1."""
    inv_t = 1-t
    coefs = [inv_t ** 3, 
             3 * t * inv_t ** 2, 
             3 * inv_t * t ** 2, 
             t ** 3]

    tx = coefs[0] * p0[0] + coefs[1] * p1[0] + \
        coefs[2] * p2[0] + coefs[3] * p3[0]
    ty = coefs[0] * p0[1] + coefs[1] * p1[1] + \
        coefs[2] * p2[1] + coefs[3] * p3[1]

    return [tx, ty]

# Return position at t, 0 < t < 1


def getBezierGadient(t: float, p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> list:
    """Returns the derivative on a bezier curve defined by the four points on location 0<=t<1."""
    inv_t = 1-t
    xs = [p1[0] - p0[0], p2[0] - p1[0], p3[0] - p2[0]]
    ys = [p1[1] - p0[1], p2[1] - p1[1], p3[1] - p2[1]]

    coefs = [3 * inv_t ** 2,
             6 * inv_t * t,
             3 * t ** 2]

    tx = coefs[0] * xs[0] + coefs[1] * xs[1] + coefs[2] * xs[2]
    ty = coefs[0] * ys[0] + coefs[1] * ys[1] + coefs[2] * ys[2]

    return [tx, ty]
