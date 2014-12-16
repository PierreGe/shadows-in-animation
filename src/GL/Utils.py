import numpy

def lookAt(eye, center, up):
    ret = numpy.eye(4, dtype=numpy.float32)

    Z = numpy.array(eye, numpy.float32) - numpy.array(center, numpy.float32)
    Z = normalize(Z)
    Y = numpy.array(up, numpy.float32)
    X = numpy.cross(Y, Z)
    Y = numpy.cross(Z, X)

    X = normalize(X)
    Y = normalize(Y)

    ret[0][0] = X[0]
    ret[1][0] = X[1]
    ret[2][0] = X[2]
    ret[3][0] = -numpy.dot(X, eye)
    ret[0][1] = Y[0]
    ret[1][1] = Y[1]
    ret[2][1] = Y[2]
    ret[3][1] = -numpy.dot(Y, eye)
    ret[0][2] = Z[0]
    ret[1][2] = Z[1]
    ret[2][2] = Z[2]
    ret[3][2] = -numpy.dot(Z, eye)
    ret[0][3] = 0
    ret[1][3] = 0
    ret[2][3] = 0
    ret[3][3] = 1.0
    return ret

def normalize(v):
    norm=numpy.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm

def translateMesh(vertices, position):
    return [[vertex[i]+position[i] for i in range(3)] for vertex in vertices]