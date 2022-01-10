import pygame
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

Forward = 0x20
Backward = 0x1E
Up = 0x39
Down = 0x1F

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
    ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def OneFrame(frames_to_wait):
    frame = 1 / 60
    frame = frame * frames_to_wait
    time.sleep(frame)


class PS4Controller(object):

    controller = None
    axis_data = None

    def init(self):
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        global Forward, Backward
        if not self.axis_data:
            self.axis_data = {
                0: 0.00,
                1: 0.00,
                2: 0.00,
                3: 0.00,
            }

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)

                    #Korean Back Dash
                if self.axis_data[0] < -0.50:
                        PressKey(Backward)
                        OneFrame(1)
                        ReleaseKey(Backward)
                        OneFrame(5)
                        PressKey(Backward)
                        PressKey(Down)
                        OneFrame(1)
                        ReleaseKey(Down)
                        OneFrame(1)
                        ReleaseKey(Backward)
                        OneFrame(1)
                        PressKey(Backward)
                        OneFrame(1)
                        ReleaseKey(Backward)
                        self.axis_data[0] = -0.50
                 
                    #Mishima Wavedash
                elif self.axis_data[0] > 0.50:
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Forward)
                        OneFrame(1)
                        PressKey(Down)
                        OneFrame(1)
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Down)
                        OneFrame(1)
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Forward)
                        OneFrame(1)
                        self.axis_data[0] = -0.50
                        
                    #Euro Step Background
                elif self.axis_data[1] < -0.50:
                        PressKey(Backward)
                        OneFrame(1)
                        PressKey(Up)
                        OneFrame(1)
                        ReleaseKey(Backward)
                        OneFrame(1)
                        ReleaseKey(Up)
                        OneFrame(7)
                        self.axis_data[1] < -0.50

                    #Euro Step Foreground
                elif self.axis_data[1] > 0.50:
                        PressKey(Backward)
                        OneFrame(1)
                        PressKey(Down)
                        OneFrame(1)
                        ReleaseKey(Backward)
                        OneFrame(1)
                        ReleaseKey(Down)
                        OneFrame(7)
                        self.axis_data[1] = -0.50

                    #Side Switch
                elif self.axis_data[2] < -0.50:
                        Forward, Backward = Backward, Forward
                    #Side Switch
                elif self.axis_data[2] > 0.50:
                        Backward, Forward = Forward, Backward

                    #Instant Shining Wizard
                elif self.axis_data[3] < -0.50:
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Forward)
                        OneFrame(5)
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Forward)
                        OneFrame(1)
                        PressKey(Forward)
                        OneFrame(1)
                        PressKey(0x17)
                        PressKey(0x18)
                        OneFrame(1)
                        ReleaseKey(0x17)
                        ReleaseKey(0x18)
                        OneFrame(1)
                        ReleaseKey(Forward)

                    #EWGF
                elif self.axis_data[3] > 0.50:
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Forward)
                        OneFrame(1)
                        PressKey(Down)
                        OneFrame(1)
                        PressKey(Forward)
                        PressKey(0x17)
                        OneFrame(1)
                        ReleaseKey(0x17)
                        ReleaseKey(Down)
                        OneFrame(1)
                        PressKey(Forward)
                        OneFrame(1)
                        ReleaseKey(Forward)
                        OneFrame(35)


                elif self.axis_data[0] > -0.25 or self.axis_data[0] < -0.25 or self.axis_data[1] > -0.25 or self.axis_data[1] < -0.25 or self.axis_data[2] > -0.25 or self.axis_data[2] < -0.25 or self.axis_data[3] > -0.25 or self.axis_data[3] < -0.25:
                    continue



if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
