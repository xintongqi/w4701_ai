Name: Amy Qi
UNI: xq2224



=====================================================================================
1. What is one-hot encoding? 
   Why is this important and how do you implement it in keras?

One-hot encoding is a method we use to transform catagorical data into numerical data.
It is important because it allows us to work with catagorical data such as images and
strings on neural networks. Otherwise we won't be able to feed the data into neural
networks and we will have to use something like a decision tree.
To implement it in keras, use keras.util.to_categorical()

2. What is dropout and how does it help overfitting?
Dropout is a regularization method used in neural networks.
It works by dropping out some neurons in some hidden layers, which helps prevent
overfitting by reducing model complexity, such that the next layer generalize better
to unseen data.

3. How does ReLU differ from the sigmoid activation function?
ReLU = max(0,a)
sigmoid = 1/(1+exp(-x))
ReLU avoids the vanishing gradient problem since it has a constant gradient of 1
for all the positive inputs. Also, ReLU makes the training process more efficient
because it is easier to calculate the ReLU values than the sigmoid values.

4. Why is the softmax function necessary in the output layer?
It transform the values in the neural networks into probabilities over all classes
so that we can choose argmax which maximizes the likelihood for us to see a certain
sample, and that argmax value is the class we are looking for.

5. This is a more practical calculation. Consider the following convolution network:
(a) Input image dimensions = 100x100x1
(b) Convolution layer with filters=16 and kernel size=(5,5)
(c) MaxPooling layer with pool size = (2,2) 
    What are the dimensions of the outputs of the convolution and max pooling layers?

Implement this model and the model summary is given below.
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 100, 100, 16)      416       
                                                                 
 max_pooling2d (MaxPooling2  (None, 50, 50, 16)        0         
 D)

The dimension of the outputs of the convolution layer is (100, 100, 16) and
(50, 50, 16) respectively.



=====================================================================================
A very brief explanation of your architecture choices, 
workflow or any relevant information about your model.

I have chosen to use a sequential model with 4 Conv2D layers, 3 MaxPooling2D layer,
two Dense layers and one Dropout layer.
I am not using a lot of layers here since the dimension of the images is only
28*28 so it makes sense to use a small number of hidden layers.
In my implementation, each Conv2D layer is followed by a MaxPooling2D layer except
the last layer. This is to perform some level of downsampling. Similarly, the
Dropout layer that I added is used to prevent overfitting as well.
For the model parameters, I am just mostly following some standard values, e.g.,
the dropout rate=0.2. 
The only parameter that I want to mention is the last Dense layer, I set units=25.
This is because I know there are in total 25 classes in the sign language dataset.
I checked using pandas, that the min value in the label column is 0 and the max
value is 24, so this value has to be 25.
One additional thing: the cross validation split is 0.2. Again this is just a
standard thing to do.
