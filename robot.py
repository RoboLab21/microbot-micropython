from machine import Pin, PWM, I2C
from neopixel import NeoPixel
import time

class Robot:
    def __init__(self):
        try:
            # Моторы
            self.motor1_dir = Pin(10, Pin.OUT)
            self.motor1_pwm = PWM(Pin(12, Pin.OUT), freq=20000, duty=0)
            
            self.motor2_dir = Pin(11, Pin.OUT)
            self.motor2_pwm = PWM(Pin(13, Pin.OUT), freq=20000, duty=0)
            
            # Датчики линии
            self.line_pins = [
                Pin(38, Pin.IN),
                Pin(39, Pin.IN),
                Pin(40, Pin.IN),
                Pin(41, Pin.IN)
            ]

            # Баззер
            self.buzzer = PWM(Pin(45, Pin.OUT), freq=500)
            self.buzzer.duty(0)

            # Датчик расстояния (VL53L0X по I2C)
            self.i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
            self.tof = None
            
            try:
                import vl53l0x
                if 0x29 in self.i2c.scan():
                    self.tof = vl53l0x.VL53L0X(self.i2c)
            except Exception as e:
                print("VL53L0X не найден или драйвер отсутствует:", e)

            self.led = NeoPixel(Pin(3), 9)
            
        except Exception as e:
            print("Ошибка инициализации железа робота:", e)

    def set_motors(self, left_speed, right_speed):
        """Установка скорости моторов"""
        left_speed = max(-100, min(100, left_speed))
        right_speed = max(-100, min(100, right_speed))
        
        if left_speed == 0:
            self.motor1_pwm.duty(0)
            self.motor1_dir.value(0)
        elif left_speed > 0:
            self.motor1_dir.value(1)
            self.motor1_pwm.duty(int(left_speed * 10.23))
        else:
            self.motor1_dir.value(0)
            self.motor1_pwm.duty(int(-left_speed * 10.23))
        
        internal_r = -right_speed
        if internal_r == 0:
            self.motor2_pwm.duty(0)
            self.motor2_dir.value(0)
        elif internal_r > 0:
            self.motor2_dir.value(1)
            self.motor2_pwm.duty(int(internal_r * 10.23))
        else:
            self.motor2_dir.value(0)
            self.motor2_pwm.duty(int(-internal_r * 10.23))

    def stop(self):
        """Остановить робота"""
        self.set_motors(0, 0)

    def get_line(self, index):
        """Возвращает 1 (или True) если видит линию, 0 — если не видит"""
        if 0 <= index <= 3:
            return self.line_pins[index].value()
        return 0

    def get_distance(self):
        """Возвращает дистанцию в мм. Возвращает 9999 если недоступно."""
        if self.tof:
            try:
                return self.tof.read_range_single_millimeters()
            except:
                return 9999
        return 9999

    def beep(self, sec):
        """Издать звук"""
        self.buzzer.duty(100)
        time.sleep(sec)
        self.buzzer.duty(0)

    def color(self, red, green, blue):
        """Поменять цвет"""
        for i in range(9):
            self.led[i] = (red, green, blue)
        self.led.write()
