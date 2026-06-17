from robot import Robot
import time

robot = Robot()

for i in range(4):
    robot.set_motors(100, 100)
    time.sleep(1)
    robot.set_motors(0, 100)
    time.sleep(0.5)

robot.stop()