from robot import Robot
import time, math

robot = Robot()

# использование светодиодов
for i in range(3, 9):
    robot.led[i] = (100, 0, 255)
for i in range(3):
    robot.led[i] = (100, 0, 255)
robot.led.write()

# пищалка
# robot.beep(1)

# скорость моторов
# robot.set_motors(0, 0)

# датчик расстояния
# for i in range(1000):
    # print(robot.tof.read_range_single_millimeters())
    # time.sleep(1)

# датчик линии 
# for i in range(1000):
#     for i in range(4):
#         print(robot.get_line(i), end='')
#     print()
#     time.sleep(1)
