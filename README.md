# Thea

[![Join the chat at https://gitter.im/suriyadeepan/thea](https://badges.gitter.im/suriyadeepan/thea.svg)](https://gitter.im/suriyadeepan/thea?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

*theano --> thea*

This project attempts to incorporate deep architectures and deep learning methods in robotics. 

## Experiment #00

Inspired by [1](http://www.cs.nyu.edu/~yann/research/lagr/), Convolutional Neural Networks are applied for vision : image understanding and decision making(steering), to achieve the following high level goals:

* Autonomous Off-road navigation
* Obstacle Avoidance
* Map Building
* Finding traversable regions

In #00, we make use of a simple mobile robot, without additional sensors or actuators for controlling the orientation or position of the bot. Pulse Width modulation(PWM) is used for controlling the motors individually, to achieve precise (precise enough) control over the orientation of the bot. An android smartphone is mounted on the bot, which streams video at a rate of *x* frames per second, with resolution of *y x z*. A raspberry mounted on the bot takes low level control of the motors (through the motor driver IC : 293d). The RPi is responsible for managing the orientation of the bot, through PWM on its GPIO pins. 

*Insert image of bot below*

The actual processing of data and issuing of high level (steering angle) commands are taken care of, by a PC with a powerful GPU, connected to the same network. This is where, a convolnet of 6 layers is implemented in theano. The images are acquired from the smartphone, which is connected to the same network through WIFI. Each input to the convolnet is a collection of 5 (*change this number*) consecutive grayscale images,  each passed through low pass and high pass filters to obtain 10 images, cascaded across depth dimension. If the image is of size 480x270, input to convolnet becomes 480x270x10. 

*Insert convolnet architecture image below*

This input is propagated through 4 layers of convolution and pooling, followed by a layer of 1000 neurons fully connected to the logical regression layer. The output of the logical regression layer can be of two types:

1. 2 neurons : PWM frequency of left and right motors
2. *m x m* neurons : Each element is a combination of PWM frequency of left and right motors