import serial
import time
import Gamepad



class PrinterController:
	def __init__(self, port="/dev/3dprinter", baud=115200):
        	print("Connecting and waiting for reboot...")
        	self.ser = serial.Serial(port, baud)
        	time.sleep(2)

	def send(self, gcode):
		print(f"Sending: {gcode}")
		self.ser.write(f"{gcode}\n".encode('ascii'))

def main():
	gamepadType = Gamepad.PS4
	extrude = 'CROSS'
	estop = 'CIRCLE'
	joystickRoll = 'LEFT-X'
	joystickPitch = 'LEFT-Y'
	pollInterval = 0.1
	home = '13'

	deadzone = 0.1
	maxDistance = 10
	if not Gamepad.available():
		print('Please connect your gamepad...')
		while not Gamepad.available():
        		time.sleep(1.0)

	gamepad = gamepadType()
	print('Gamepad connected')

	printer = PrinterController()
	gamepad.startBackgroundUpdates()
	time.sleep(3)
	#printer.send("G28")
	print("Heat for bed and extruder, is recomended to wait ~5 mins")
	printer.send("M140 S60")
	time.sleep(1)
	printer.send("M104 S200")
	time.sleep(1)
	printer.send("G91")
	time.sleep(1)
	try:
		while gamepad.isConnected():
	    	# Check for the exit button
			if gamepad.beenPressed(estop):
				print('E-STOP')
				printer.send("M112")
				break

			# Check if the beep button is held
			if gamepad.isPressed(extrude):
				print('Extruding...')
				printer.send("G1 E1 F100")
			if gamepad.beenPressed(home):
				print("Going home...")
				printer.send("G28")
		        # Update the joystick positions
		        # Speed control (inverted)
			leftRight = -gamepad.axis(joystickRoll)
		        # Steering control (not inverted)
			forwardBack = gamepad.axis(joystickPitch)
			if abs(leftRight) < deadzone:
				leftRight = 0.0

			if abs(forwardBack) < deadzone:
				forwardBack = 0.0
			xAxis = leftRight # * 100
			yAxis = forwardBack * -1 # * 100

			if xAxis != 0:
				if xAxis < 0:
					printer.send("G1 X" + str(maxDistance * xAxis) + " F6000")
				else:
					printer.send("G1 X" + str(maxDistance * xAxis)+" F6000")
			if yAxis != 0:
				if yAxis < 0:
					printer.send("G1 Y"+ str(maxDistance * yAxis)+ " F6000")
				else:
					printer.send("G1 Y" + str(maxDistance * yAxis) + " F6000")
		        # Sleep for our polling interval
			time.sleep(pollInterval)
	finally:
	   	# Ensure the background thread is always terminated when we are done
		gamepad.disconnect()


if __name__ == "__main__":
	main()
