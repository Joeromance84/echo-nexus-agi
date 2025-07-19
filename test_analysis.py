
# Test file for autonomous analysis
import unused_module
import os

def duplicate_function(x):
    return x * 2

def duplicate_function_v2(x):
    return x * 2

# Large function that could be optimized
def large_function(a, b, c, d, e, f):
    result = a + b + c + d + e + f
    if result > 100:
        return result * 2
    else:
        return result / 2

class UnoptimizedClass:
    def __init__(self):
        pass
    
    def method1(self):
        pass
    
    def method2(self):
        pass
