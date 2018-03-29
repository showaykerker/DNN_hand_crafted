from __future__ import absolute_import
import numpy as np

LAYER_TYPE = ['Input', 'Output', 'Dense', 'activation']
INITIALIZER_TYPE = ['normal', 'gaussian', 'zeros']

class node_:
	def __init__(self, type_='regular'):
		self.type = type_
		self.initialized = False
		pass

	def initialize(self, n_output, initializer='normal', mean=0, std=0.1):
		self.initialized = True
		if self.type == 'activation':
			self.neurons = np.zeros((1, n_output))
			self.value = 0
		else:
			if initializer not in INITIALIZER_TYPE : 
				raise ValueError('initializer %s not recognized.'%str(initializer))
			if initializer == 'normal' or initializer == 'gaussian':
				self.neurons = np.random.normal(mean, std, (1, n_output))
				self.value = 0
			elif initializer == 'zeros':
				self.neurons = np.zeros((1, n_output))
				self.value = 0
			if self.type == 'bias': self.value = 1
		


	def get_neurons(self):
		return self.neurons

	def __str__(self):
		if self.initialized:
			ret = '<Class node> initialized. type=%s, value=%f neurons='%(self.type, self.value) +str([i for i in self.neurons])
		else: ret = '<Class node> not initializer. type=%s'%self.type
		return ret


class layer:
	def __init__(self, n_nodes, layer_type):
		self.n_nodes = n_nodes
		self.initialized = False
		self.n_input = n_nodes
		self.layer_type = layer_type


	def __str__(self):
		if self.initialized:
			ret = '<Class layer> initialized. type=%s, n_nodes=%d, n_output=%d\n' % (self.layer_type,self.n_nodes, self.n_output) + str(self.matrix)
		else: ret = '<Class layer> not initializer. n_nodes=%d' % (n_nodes)
		return ret
		
	def initialize(self, n_output, initializer='normal', mean=0, std=0.1):
		self.initialized = True
		self.n_output = n_output
		
		if self.layer_type in ['Dense', 'Input', 'Output']:
			self.nodes = []
			for i in range(0, n_nodes):
				self.nodes.append(node_())

		if self.layer_type in ['Dense', 'Input']:
			self.nodes.append(node_(type_='bias'))
			self.n_nodes = len(self.nodes) # with bias

			

			for node in self.nodes:
				node.initialize(n_output, initializer=initializer, mean=mean, std=std)
				if not hasattr(self, 'matrix'): self.matrix = node.get_neurons()
				else: self.matrix = np.append(self.matrix, node.get_neurons(), axis=0)

		elif self.layer_type == 'activation':
			self.nodes = []
			for i in range(self.n_nodes):
				new_node = node_(type_='activation')
				new_node.initialize(n_output=self.n_nodes)
				self.nodes.append(new_node)

	def get_layer_type(self):
		return self.layer_type

	def is_init(self):
		return self.initialized


if __name__ == '__main__':
	a = layer(n_nodes = 2, layer_type='Dense')
	a.initialize(3)
	print(a)