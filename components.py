import random

class Tank:
	def __init__(self,hh,high,low, level):
		'''
		Initialise Tank object with low, high and init level
		'''
		self.high = high
		self.low = low
		self.level = level
		self.hh = hh
		self.state = None
		self.current_level = self.level
		
	def water_input(self, water_in):

		r = random.uniform(-0.01,0.01)
		self.current_level += water_in + r # Added uniform noise to better simulate the plant
		print('Water in',water_in + r )
		return self.current_level

	def _get_state(self):
		
		if self.current_level < self.low:
			self.state = 'L'

		elif self.current_level > self.high and self.current_level < self.hh:
			self.state = 'H'
			
		elif self.current_level > self.hh:
			self.state = 'HH'

		else:
			self.state = 'N'
			
		return self.state, self.current_level

	def get_tank_state(self):
		return self._get_state()

class Pump1:
	def __init__(self):
		self.state = 0
		
	def run(self):
		self.state = 1
		return self.state
	
	def stop(self):
		self.state = 0
		return self.state

class Pump2:
	def __init__(self):
		self.state = 0

	def run(self):
		self.state = 1
		return self.state

	def stop(self):
		self.state = 0
		return self.state
	
class Valve:
	def __init__(self):
		self.state = 0

	def open(self):
		self.state = 1
		return self.state

	def close(self):
		self.state = 0
		return self.state
	
class Pressure:
	def __init__(self):
		self.state = 0

	def flow(self):
		self.state = 1.5
		return self.state

	def half_flow(self):
		self.state = 0.75
		return self.state
	
	def valve_flow(self):
		self.state = 1
		return self.state

	def noflow(self):
		self.state = 0
		return self.state
