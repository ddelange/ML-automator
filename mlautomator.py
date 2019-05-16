#Standard Python libary imports
import time 
import numpy as np

#Local imports
from objective_functions import Classifiers, Regressors
from search_spaces import get_space
from main import get_data

#3rd party imports
from hyperopt import hp, fmin, tpe, rand, STATUS_OK, Trials



class MLAutomator:
    '''
    MLAutomator leverages the intelligent search properties of Hyperopt to reduce hyperparameter tuning times
    across large hyperparameter search spaces.  This extra time allows you to spot-check a larger cross section 
    of algorithms on your dataset.  

    MLAutomator does not perform predictions, its sole function is to find the optimal pre-processors, features, and 
    hyperparameters.

    Parameters:
    -----------
    x_train : numpy ndarray
        The training data that the models will be trained on.
    y_train : numpy ndarray
        The target variables for the model.
    algo_type : str, optional (default='classifier')
        Accepts 'classifier' or 'regressor'.  
    score_metric : str, optional (default='accuracy')  
        The scoring metric that Hyperopt will minimize on.  
    iterations : int, optional (default=25)
        The number of trials that Hyperopt will run on each algorithm candidate.
    num_cv_folds : int, optional (default=10)
        The number of folds to use in cross validation.
    repeats : int, optional (default=1)
        The number of passes to perform on cross validation.
    '''

    def __init__(
        self,
        x_train, 
        y_train,
        algo_type='classifier', 
        score_metric='accuracy',
        iterations=25, 
        num_cv_folds=10, 
        repeats=1,
    ):

        self.start_time=None
        self.count=0
        self.objective=None
        self.keys=None
        self.master_results=[]
        self.x_train=x_train
        self.y_train=y_train
        self.type=algo_type
        self.score_metric=score_metric
        self.iterations=iterations
        self.num_cv_folds=num_cv_folds
        self.repeats=repeats
        self.objective=None
        self._initialize_best()
        self.best_space=None
        self.best_algo=None
        self.found_best_on=None
        self.num_features=self.x_train.shape[1]
        self.num_samples=self.x_train.shape[0]


    def _initialize_best(self):
        '''
        Utility method for properly initializing the 'best' parameter.  After each iteration, the score will be checked
        against 'best' to see if the space used in that iteration was superior.  Depending on the scoring metric used, 'best'
        needs to be initialized to different values.
        '''
        initializer_dict={
            'accuracy': 0, 
            'neg_log_loss': 5,
        }
        self.best=initializer_dict[self.score_metric]
        

    def get_objective(self,obj):
        '''
        A dictionary look-up function that offers a clean way of looping through the objective 
        functions by key and returning the function call.  

        Parameters: 
        ----------
        obj - string
            key value representing the ojective function to call.
        '''
        if self.type=='classifier':
        
            objective_list= {        
                        '01': Classifiers.objective01,
                        '02': Classifiers.objective02,
                        '03': Classifiers.objective03,
                        '04': Classifiers.objective04,
                        '05': Classifiers.objective05,
                        '06': Classifiers.objective06,
                            }
        
        else:  

            objective_list= {        
                        '01': Regressors.objective01,
                        '02': Regressors.objective02,
                        '03': Regressors.objective03,
                        '04': Regressors.objective04,
                            }            

        return objective_list[obj]


    def f(self,space):
        '''
        This is the "function to be minimized" by hyperopt. This gets passed to the fmin function 
        within the method find_best_algorithm.

        Parameters: 
        -----------
        space : dictionary 
            subset of total search space selected by Hyperopt.
        '''
        iter_start=time.time()
        loss, algo = self.objective(self,space)
        self.count+=1

        #time methods for providing analytics on how each iteration is taking.
        iter_end=round((time.time()-iter_start)/60,3)
        total_time=round((time.time()-self.start_time)/60,3)
        avg_time=round((total_time/self.count),3)
        
        if loss < self.best:  
            self.best = loss
            self.best_space=space
            self.best_algo=algo
            self.found_best_on=self.count
            print('')
            print('new best score:', self.best)
            for key,values in space.items():
                print(str(key) +' : ' +str(values))
            print('')    
            
        else:  
            str1= 'Scanning '+algo+'.'
            str2=' No Improvement. Iter time: '+str(iter_end)+'.'
            str3=' Total Time Elapsed: '+str(total_time)+'.'
            str4=' AVG Time: '+str(avg_time)
            print(str1+str2+str3+str4) 

        self.master_results.append([loss,space])
        
        return {'loss': loss, 'status': STATUS_OK}


    def find_best_algorithm(self):   
        '''
        This is the main method call.  It loops through each objective function that is 
        provided in the array 'objectives' and passes it to the Hyperopt function fmin.  fmin 
        will intelligently search the search spaces for each algorithm and attempt to minimize (optimize) 
        the scoring function provided.
        '''
        self.start_time=time.time()
        objectives=['01','02','03','04','05','06']

        for obj in objectives:
            keys=obj
            self.objective=self.get_objective(obj)
            seed=np.random.seed(1985)
            space=obj  
            trials=Trials()
            best=fmin(
                fn=self.f,
                space=get_space(self, space),
                algo=tpe.suggest,
                max_evals=self.iterations,
                trials=trials,
            )    


    def print_best_space(self):
        '''
        Prints out a report with the best algorithm and its configuration.
        '''
        print('Best Algorithm Configuration:')
        print('    '+'Best algorithm: '+self.best_algo)
        print('    '+'Best '+self.score_metric+' : '+str(self.best))
        for key,val in self.best_space.items():
            print('    '+ str(key)+' : '+ str(val), end='\n')                                
        print('    '+'Found best solution on iteration '+str(self.found_best_on)+' of '+str(self.count)) 
        print('    '+'Validation used: '+str(self.num_cv_folds)+'-fold cross-validation')          


if __name__=='__main__':
    x,y=get_data('pima-indians-diabetes.csv')
    automator=MLAutomator(x,y,iterations=25)
    automator.find_best_algorithm()
    automator.print_best_space()
    
