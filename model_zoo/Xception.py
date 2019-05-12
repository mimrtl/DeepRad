'''
Copyright: Jinnian Zhang
Last Modified: 08/21/2018
'''

from keras import applications
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, Dense

def Xception(input_shape = (256, 256, 3), weights = 'imagenet', num_classes = 5):
	model_origin = applications.Xception(include_top = False, weights = weights, input_shape = input_shape)
	for layer in model_origin.layers:
		layer.trainable = True

	#layer_name = 'block13_sepconv2_bn'
	p = GlobalAveragePooling2D()(model_origin.output)
	o = Dense(num_classes, activation = 'softmax')(p)
	model = Model(inputs = model_origin.input, output = [o])
	return model
