import numpy as np

import pandas as pd
#from FM import FMClassifier
from pyfm import pylibfm
from FM3 import FMClassifier
from FmUtil import *
X_train,y_train,X_test,y_test=classification_data()
y_test=y_test[:,np.newaxis]

"""
"""
print("  mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm  ")
for i in range(1):
    #fm=FMClassifier(num_factors=2, num_iter=10, verbose=False, init_stdev=1,task="classification", initial_learning_rate=0.0001, learning_rate_schedule="optimal")
    fm=FMClassifier(num_factors=2, num_iter=30)

    print(".................................")
    fm.fit(X_train,y_train)
    fm.param_print()
    y_test_p=fm.predict(X_test)
    y_test_p2=np.around(y_test_p,0)
    print(1-np.sum(y_test!=y_test_p2)*1.0/len(y_test))
#print(np.concatenate([y_test,y_test_p],axis=1))


