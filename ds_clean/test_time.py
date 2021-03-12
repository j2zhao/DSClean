from logged_array import LoggedNDArray
import np



test = LoggedNDArray(np.zeros((10, 10)))
test_1 = LoggedNDArray(np.random((10, 10)))
test = test + test_1
np.sum(test)
