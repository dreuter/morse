import GameLogic
import morse.helpers.actuator

class VWActuatorClass(morse.helpers.actuator.MorseActuatorClass):
	""" Motion controller using linear and angular speeds

	This class will read linear and angular speeds (V, W)
	as input from an external middleware, and then apply them
	to the parent robot.
	"""

	def __init__(self, obj, parent=None):
		print ('######## VW CONTROL INITIALIZATION ########')
		# Call the constructor of the parent class
		super(self.__class__,self).__init__(obj, parent)

		self.local_data['v'] = 0.0
		self.local_data['w'] = 0.0

		self.data_keys = ['v', 'w']

		# Initialise the copy of the data
		for variable in self.data_keys:
			self.modified_data.append(self.local_data[variable])


		print ('######## CONTROL INITIALIZED ########')



	def default_action(self):
		""" Apply (v, w) to the parent robot. """

		# Reset movement variables
		vx, vy, vz = 0.0, 0.0, 0.0
		rx, ry, rz = 0.0, 0.0, 0.0

		# Tick rate is the real measure of time in Blender.
		# By default it is set to 60, regardles of the FPS
		# If logic tick rate is 60, then: 1 second = 60 ticks
		ticks = GameLogic.getLogicTicRate()

		# Scale the speeds to the time used by Blender
		try:
			vx = self.local_data['v'] / ticks
			rz = self.local_data['w'] / ticks
		# For the moment ignoring the division by zero
		# It happens apparently when the simulation starts
		except ZeroDivisionError:
			pass

		# Get the Blender object of the parent robot
		parent = self.robot_parent.blender_obj

		# Give the movement instructions directly to the parent
		# The second parameter specifies a "local" movement
		parent.applyMovement([vx, vy, vz], True)
		parent.applyRotation([rx, ry, rz], True)
