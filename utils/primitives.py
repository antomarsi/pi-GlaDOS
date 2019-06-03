################## http://www.pygame.org/wiki/2DVectorClass ##################
import operator
import math
import abc
import numpy as np


class Vector2(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']

    def __init__(self, x_or_pair, y=None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vector2")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vector2")

    # String representaion (for debugging)
    def __repr__(self):
        return 'Vector2(%s, %s)' % (self.x, self.y)

    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True

    def __nonzero__(self):
        return bool(self.x or self.y)

    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vector2"
        if isinstance(other, Vector2):
            return Vector2(f(self.x, other.x),
                           f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vector2(f(self.x, other[0]),
                           f(self.y, other[1]))
        else:
            return Vector2(f(self.x, other),
                           f(self.y, other))

    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vector2"
        if (hasattr(other, "__getitem__")):
            return Vector2(f(other[0], self.x),
                           f(other[1], self.y))
        else:
            return Vector2(f(other, self.x),
                           f(other, self.y))

    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    # Addition
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            return Vector2(self.x + other, self.y + other)
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vector2(self.x - other[0], self.y - other[1])
        else:
            return Vector2(self.x - other, self.y - other)

    def __rsub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vector2(other[0] - self.x, other[1] - self.y)
        else:
            return Vector2(other - self.x, other - self.y)

    def __isub__(self, other):
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vector2(self.x*other[0], self.y*other[1])
        else:
            return Vector2(self.x*other, self.y*other)
    __rmul__ = __mul__

    def __imul__(self, other):
        if isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)

    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)

    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)

    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)

    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)

    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)

    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)

    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)

    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)

    def __divmod__(self, other):
        return self._o2(other, operator.divmod)

    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)

    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)

    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)

    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)

    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)

    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)

    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__

    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__

    # Unary operations
    def __neg__(self):
        return Vector2(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vector2(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vector2(self.x*-1, self.y*-1)

    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None,
                      "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y

    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vector2(x, y)

    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None,
                     "gets or sets the angle of a vector")

    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))

    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vector2(self)

    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length

    def perpendicular(self):
        return Vector2(self.y*-1, self.x)

    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vector2((self.y*-1)/length, self.x/length)
        return Vector2(self)

    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])

    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)

    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2

    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def cross(self, other):
        return self.x*other[1] - self.y*other[0]

    def interpolate_to(self, other, range):
        return Vector2(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)

    def convert_to_basis(self, x_vector, y_vector):
        return Vector2(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())

    def __getstate__(self):
        return [self.x, self.y]

    def __setstate__(self, dict):
        self.x, self.y = dict

# Classes for 3D objects


class Node(object):
    def __init__(self, x_or_xyz, y=None, z=None):
        if y == None:
            self.x = x_or_xyz[0]
            self.y = x_or_xyz[1]
            self.z = x_or_xyz[2]
        else:
            self.x = x_or_xyz
            self.y = y
            self.z = z


class Edge(object):
    def __init__(self, start: Node, stop: Node):
        self.start = start
        self.stop = stop


class Wireframe(metaclass=abc.ABCMeta):
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def addEdges(self, edgeList):
        self.edges += edgeList

    def center(self):
        """ Find the centre of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)

    def transform(self, matrix):
        self.nodes = np.dot(self.nodes, matrix)

    def translationMatrix(self, dx=0, dy=0, dz=0):
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [dx, dy, dz, 1]])

    def scaleMatrix(self, sx=0, sy=0, sz=0):
        """ Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """

        return np.array([[sx, 0,  0,  0],
                         [0,  sy, 0,  0],
                         [0,  0,  sz, 0],
                         [0,  0,  0,  1]])

    def rotateXMatrix(self, radians):
        """ Return matrix for rotating about the x-axis by 'radians' radians """

        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[1, 0, 0, 0],
                         [0, c, -s, 0],
                         [0, s, c, 0],
                         [0, 0, 0, 1]])

    def rotateYMatrix(self, radians):
        """ Return matrix for rotating about the y-axis by 'radians' radians """

        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c, 0, s, 0],
                         [0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [0, 0, 0, 1]])

    def rotateZMatrix(self, radians):
        """ Return matrix for rotating about the z-axis by 'radians' radians """

        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c, -s, 0, 0],
                         [s, c, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

    def translate(self, vector):
        """ Translate all wireframes along a given axis by d units. """
        matrix = self.translationMatrix(*vector)
        self.transform(matrix)

    def scale(self, vector):
        matrix = self.scaleMatrix(*vector)
        self.transform(matrix)

    def rotate(self, vector):
        self.transform(self.rotateXMatrix(vector[0]))
        self.transform(self.rotateYMatrix(vector[1]))
        self.transform(self.rotateZMatrix(vector[2]))

class Cube(Wireframe):
    def __init__(self, size_x=1, size_y=1, size_z=1):
        super().__init__()
        cube_nodes = [(x, y, z) for x in (0, size_x)
                      for y in (0, size_y) for z in (0, size_z)]
        self.addNodes(np.array(cube_nodes))
        self.addEdges([(n, n+4) for n in range(0, 4)])
        self.addEdges([(n, n+1) for n in range(0, 8, 2)])
        self.addEdges([(n, n+2) for n in (0, 1, 4, 5)])
        self.translate(((size_x/2)*-1, (size_y/2)*-1, (size_z/2)*-1))


class Line(Wireframe):
    def __init__(self, width=1):
        self.addNodes(np.array([(0, 0), (width, 0)]))
        self.addEdges([[0, 1]])
        self.line_radius = 2


class Cylinder(Wireframe):
    def __init__(self, height=1, radius=1, segments=6):
        super().__init__()
        theta = 2 * math.pi / segments
        tangetial_factor = math.tan(theta)
        radial_factor = math.cos(theta)
        x = radius
        y = 0
        base_nodes = []
        top_nodes = []
        for i in range(0, segments):
            tx = -y
            ty = x
            x += tx * tangetial_factor
            y += ty * tangetial_factor
            x *= radial_factor
            y *= radial_factor
            base_nodes.append([x, 0, y])
            top_nodes.append([x, height, y])

        self.addNodes(np.array(base_nodes))
        self.addNodes(np.array(top_nodes))
        base_edges = [(n, n+1) for n in range(0, segments-1)]
        base_edges.append((segments-1, 0))
        self.addEdges(base_edges)
        self.addEdges([(x+segments, y+segments) for (x, y) in base_edges])
        self.addEdges([(n, n+segments) for n in range(0, segments)])
        self.translate(((radius/4)*-1, (height/2)*-1, (radius/4)*-1))


class Sphere(Wireframe):
    def __init__(self, radius=1, segments=10):
        super().__init__()
        theta = 2 * math.pi / segments
        tangetial_factor = math.tan(theta)
        radial_factor = math.cos(theta)
        x = radius
        y = 0
        array_nodes = [[], [], []]
        for i in range(0, segments):
            tx = -y
            ty = x
            x += tx * tangetial_factor
            y += ty * tangetial_factor
            x *= radial_factor
            y *= radial_factor
            array_nodes[0].append([x, 0, y])
            array_nodes[1].append([x, y, 0])
            array_nodes[2].append([0, x, y])
        for n in array_nodes:
            self.addNodes(np.array(n))
        for idx, array in enumerate(array_nodes):
            start = segments * idx
            edges = [(n, n+1) for n in range(start, start+segments-1)]
            edges.append((start+segments-1, start))
            self.addEdges(edges)


class Pyramid(Wireframe):
    def __init__(self, size_x=1, size_y=1, size_z=1):
        super().__init__()
        cube_nodes = [(x, 0, z) for x in (0, size_x)
                      for z in (0, size_z)]
        cube_nodes.append((size_x/2, size_y, size_y/2))
        self.addNodes(np.array(cube_nodes))
        self.addEdges([(0,1), (1,3), (3,2), (2,0)])
        self.addEdges([(n, 4) for n in range(0, 4)])

        self.translate(((size_x/2)*-1, (size_y/2)*-1, (size_z/2)*-1))

class Plane(Wireframe):
    def __init__(self, size_x=1, size_z=1):
        super().__init__()
        cube_nodes = [(x, 0, z) for x in (0, size_x)
                      for z in (0, size_z)]
        self.addNodes(np.array(cube_nodes))
        self.addEdges([(0,1), (1,2), (1,3), (3,2), (2,0)])

        self.translate(((size_x/2)*-1, 0, (size_z/2)*-1))
