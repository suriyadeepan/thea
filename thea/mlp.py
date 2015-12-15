
# coding: utf-8

# In[1]:

### >> Multilayer Perceptron << ###
## http://deeplearning.net/tutorial/mlp.html ##

import os
import sys

import theano
import theano.tensor as T
import numpy as np

from logistic import load_data,LogisticRegression


# In[4]:

# Define the hidden layer class
class HiddenLayer(object):
    def __init__(self,rng,input,n_in,n_out,w=None,b=None):
        self.input = input
        if w is None:
            wval = np.asarray(rng.uniform(low=-np.sqrt(6. / (n_in + n_out)),
                    high=np.sqrt(6. / (n_in + n_out)),
                    size=(n_in, n_out)),
                              dtype = theano.config.floatX)
            w = theano.shared(wval,name='w',borrow=True)
        #bias
        if b is None:
            b = theano.shared(
                value = np.zeros( (n_out,),dtype=theano.config.floatX),
                name='b',
                borrow=True
            )
        
        #b_values = np.zeros((n_out,), dtype=theano.config.floatX)
        #b = theano.shared(value=b_values, name='b', borrow=True)
        
        self.w = w
        self.b = b
        self.output = T.tanh(T.dot(input,self.w)+self.b)
        self.params = [self.w,self.b]    
        
### Define MLP class ###
class MLP(object):
    def __init__(self,rng,input,n_in,n_h,n_out):
        self.hidden_layer = HiddenLayer(rng,input=input,n_in=n_in,n_out=n_h)
        self.output_layer = LogisticRegression(input=self.hidden_layer.output, n_in=n_h,n_out=n_out)
        #regularization
        self.L1 = abs(self.hidden_layer.w).sum() + abs(self.output_layer.w).sum()
        self.L2 = (self.hidden_layer.w**2).sum() + (self.output_layer.w**2).sum()
        # Negative Log Likelihood
        self.neg_log_likelihood = (self.output_layer.neg_log_likelihood)
        # errors function
        self.errors = (self.output_layer.errors)
        # params
        self.params = self.hidden_layer.params + self.output_layer.params
        
        self.input = input


