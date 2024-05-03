import math
class myVector:
    """My Vector"""

    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def dot(self, v2):
        if not isinstance(v2, myVector):
            raise TypeError("Dot product is only defined between to vector objects")
        return self.x * v2.x + self.y * v2.y

    def __matmul__(self, v2):
        return self.dot(v2)
    
    def __sub__(self, v2):
        return myVector(self.x-v2.x,self.y-v2.y)
    
    def __add__(self, v2):
        return myVector(self.x + v2.x, self.y + v2.y)
    
    def __mul__(self, scale):
        if isinstance(scale, int) or isinstance(scale, float):
            return myVector(scale * self.x, scale * self.y)
        
        raise TypeError("Scalar must be int or float")
    
    def __neg__(self):
        return myVector(-self.x, -self.y)
    
    def __rmul__(self, scale):
        return self.__mul__(scale)
    
    def __truediv__(self, scale):
        return myVector(self.x/scale,self.y/scale)
    
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def __eq__(self, v2) -> bool:
        return self.x == v2.x and self.y == v2.y
    
    def toTuple(self):
        return tuple((self.x,self.y))
    
    def toLength(self, length):
        return length/abs(self) * self