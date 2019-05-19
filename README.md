# ML Automator
#### Author: Kevin Vecmanis

Machine Learning Automator ('ML Automator' for short) is an automation project that integrates the Hyperopt asynchronous optimization engine with the main learning algorithms from Python's Sci-kit Learn to generate a really fast, automated tool for tuning machine learning algorithms.  [Read more about Hyperopt here](http://hyperopt.github.io/hyperopt/)

## Key features:

* Optimizes across data pre-processing and feature selection __in addition__ to hyperparameters.
* Fast, intelligent scan of parameter space using __Hyperopt__. 
* Optimized parameter search permits scanning a larger cross section of algorithms in the same period of time.  
* An exceptional spot-checking algorithm.

## Usage 

__MLAutomator__ accepts a training dataset X, and a target Y.  The user can define their own functions for how these datasets are produced.  Note that MLAutomator is designed to be a highly optimized spot-checking algorithm - you should take care to make sure you data is free from errors, and any missing values have been dealth with.   

MLAutomator will find ways of transforming and pre-processing your data to produce a superior model.  Feel free to make your own transformations before passing the data to MLAutomator.  

### Optional data utilities

I'm building a suite of data utility functions which can prepare most classification and regression datasets.  These, however, are optional - __MLAutomator__ only requires __X and Y__ inputs in the form of a numpy ndarray.

```Python
from data.utilities import clf_prep

x,y=clf_prep('pima-indians-diabetes.csv')
```

Once you have training and target data, this is the main call to use MLAutomator...

### Classification Example: 2-class

```Python
from mlautomator.mlautomator import MLAutomator

automator=MLAutomator(x,y,iterations=25)
automator.find_best_algorithm()
automator.print_best_space()
```

MLAutomator can typically find a ~98th percentile solution in a fraction of the time of Gridsearch of Randomized search.  Here it did a comprehensive scan across all hyperparameters for 6 common machine learning algorithms and produced exceptional model performance for the classic Pima Indians Diabetes dataset.

```
Best Algorithm Configuration:
    Best algorithm: Logistic Regression
    Best accuracy : 77.73239917976761%
    C : 0.02341
    k_best : 6
    penalty : l2
    scaler : RobustScaler(
        copy=True, 
        quantile_range=(25.0, 75.0), 
        with_centering=True,
        with_scaling=True)
    solver : lbfgs
    Found best solution on iteration 132 of 150
    Validation used: 10-fold cross-validation
```

### Classification Example: Multi-class

Here are the results from the classic iris dataset, a multi-class classification problem with three classes

```Python
from data.utilities import from_sklearn
from mlautomator.mlautomator import MLAutomator

x,y=from_sklearn('iris')
automator=MLAutomator(x,y,iterations=30,algo_type='classifier',score_metric='accuracy')
automator.find_best_algorithm()
automator.print_best_space()
```

```
Best Algorithm Configuration:
    Best algorithm: Support Vector Machine Classifier
    Best accuracy : 96.67%
    C : 0.7064
    degree : 2
    gamma : auto
    k_best : 2
    kernel : rbf
    n_estimators : 9
    probability : True
    scaler : None
    Found best solution on iteration 3 of 30
    Validation used: 10-fold cross-validation
```



### Regression Example

ML Automator supports regression problems as well. In this example we call the Boston Housing dataset from __sklearn.datasets__ using one of our utility functions.

```Python
from data.utilities import from_sklearn

x,y=from_sklearn('boston')
```

```Python
from mlautomator.mlautomator import MLAutomator

automator=MLAutomator(x,y,iterations=30,algo_type='regressor',score_metric='neg_mean_squared_error')
automator.find_best_algorithm()
automator.print_best_space()
```

```
Best Algorithm Configuration:
    Best algorithm: K-Neighbor Regressor
    Best neg_mean_squared_error : 10.41395782834094
    algorithm : kd_tree
    k_best : 11
    n_neighbors : 2
    scaler : StandardScaler(copy=True, with_mean=True, with_std=True)
    weights : distance
    Found best solution on iteration 24 of 30
    Validation used: 10-fold cross-validation
```