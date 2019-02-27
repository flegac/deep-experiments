# Notes

## Loss function & optimizer
The loss function mesures how far the prediction is from the ground truth.

The optimizer updates the weights based on the loss function result.

https://keras.io/losses/
https://keras.io/optimizers/

### Loss functions
* categorical crossentropy (sparse, binary)

* mean squared error (absolute | absolute percentage | squared logarithmic)
* hinge (squared | categorical)
* kullback leibler divergence
* poisson
* cosine proximity

### Optimizer
https://en.wikipedia.org/wiki/Stochastic_gradient_descent


* sgd : Stochastic gradient descent
* RMSprop : usually a good choice for recurrent neural networks.

* Adagrad
* Adadelta : more robust extension of Adagrad 
* Adam
* Adamax
* Nadam

## Metrics
Metrics are used to evaluate the model performances.
Same as loss functions.


## Activation function

* softmax : normalize data to values between 0 and 1
https://en.wikipedia.org/wiki/Softmax_function

* relu : drop negative values to zero ()
https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
--> use BatchNormalization() between (Conv2D, Activation)