import math
from display import *


  # IMPORTANT NOTE

  # Ambient light is represented by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The first index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(light[0])
    normalize(normal)
    normalize(view)
    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)
    i = [int(ambient[0] + diffuse[0] + specular[0]),
         int(ambient[1] + diffuse[1] + specular[1]),
         int(ambient[2] + diffuse[2] + specular [2])]
    limit_color(i)
    return i

def calculate_ambient(alight, areflect):
    ambient = [alight[0] * areflect[0],
               alight[1] * areflect[1],
               alight[2] * areflect[2]]
    return ambient

def calculate_diffuse(light, dreflect, normal):
    cos = dot_product(light[0], normal)
    if cos < 0:
        cos = 0
    p = light[1]
    diffuse = [p[0] * dreflect[0] * cos,
               p[1] * dreflect[1] * cos,
               p[2] * dreflect[2] * cos]
    return diffuse

def calculate_specular(light, sreflect, view, normal):
    dp = dot_product(normal, light[0])
    if dp < 0:
        dp = 0
    t = [normal[0] * dp,
         normal[1] * dp,
         normal[2] * dp]
    l = light[0]
    s = [t[0] - l[0],
         t[1] - l[1],
         t[2] - l[2]]
    r = [t[0] + s[0],
         t[1] + s[1],
         t[2] + s[2]]
    dp = dot_product(r, view)
    if dp < 0: 
        dp = 0
    cos = math.pow(dp, SPECULAR_EXP)
    p = light[1]
    specular = [p[0] * sreflect[0] * cos,
                p[1] * sreflect[1] * cos,
                p[2] * sreflect[2] * cos]
    return specular

def limit_color(color):
    for i in range(len(color)):
        if color[i] < 0:
            color[i] = 0
        if color[i] > 255:
            color[i] = 255

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
