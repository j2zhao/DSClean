import inspect
import numpy as np
from numpy import testing
# def PrintFrame():
#   callerframerecord = inspect.stack() #[1]    # 0 represents this line
#   print(callerframerecord[1])                                          # 1 represents line at caller
#   frame = callerframerecord[1][0]
#   print(frame)
#   info = inspect.getframeinfo(frame)
#   print(info.filename)                      # __FILE__     -> Test.py
#   print(info.function)                      # __FUNCTION__ -> Main
#   print(info.lineno)                        # __LINE__     -> 13

# def Main():
#   PrintFrame()                              # for this line

# Main()

class Test(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        obj.cat = 1
        return obj
    
    def __array_finalize__(self, obj):
        self.cat = getattr(obj, 'cat', 1)

    def _cat(self):
        self.cat = 0
test = Test(np.random.rand(2, 2))
print(id(test))
test._cat()
test_ = test.view(np.ndarray)
print(id(test_))
#test = test_.view(Test)
print(test.cat)
