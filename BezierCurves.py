# Credits to Yusef Simsek for this code

VECTOR_STRENGTH = 1.2 - 1 # The -1 is to make editing more intuitive. At a first value of 1, they're at 100%, 0.5 at 50% etc.

# Returns the point on a bezier curve defined by the four points on location 0<=t<1.
def getBezierPoint(t: float, p0: list, p1: list, p2: list, p3: list) -> list:

    p1[0] += p0[0] + p1[0] * VECTOR_STRENGTH
    p1[1] += p0[1] + p1[1] * VECTOR_STRENGTH
    p2[0] += p3[0] + p2[0] * VECTOR_STRENGTH
    p2[1] += p3[1] + p2[1] * VECTOR_STRENGTH

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


# returns the derivative on a bezier curve defined by the four points on location 0<=t<1
def getBezierGradient(t: float, p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> list:

    inv_t = 1-t

    p1[0] += p0[0] + p1[0] * VECTOR_STRENGTH
    p1[1] += p0[1] + p1[1] * VECTOR_STRENGTH
    p2[0] += p3[0] + p2[0] * VECTOR_STRENGTH
    p2[1] += p3[1] + p2[1] * VECTOR_STRENGTH

    xs = [p1[0] - p0[0], p2[0] - p1[0], p3[0] - p2[0]]
    ys = [p1[1] - p0[1], p2[1] - p1[1], p3[1] - p2[1]]

    coefs = [3 * inv_t ** 2,
             6 * inv_t * t,
             3 * t ** 2]

    tx = coefs[0] * xs[0] + coefs[1] * xs[1] + coefs[2] * xs[2]
    ty = coefs[0] * ys[0] + coefs[1] * ys[1] + coefs[2] * ys[2]

    return [tx, ty]
