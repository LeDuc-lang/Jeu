class Timer:
    time = 0

    def __init__(self, frame: int):
        self.frame = frame
        self.time_stamp = self.time

    @property
    def frame_interval(self):
        return self.frame - self.time_stamp

    @frame_interval.setter
    def frame_interval(self, frame):
        self.frame = frame

    def event(self) -> bool:
        if self.time - self.time_stamp >= self.frame:
            self.time_stamp = self.time
            return True
        return False

    @classmethod
    def time_update(cls):
        cls.time += 1


if __name__ == '__main__':
    poison = Timer(3)
    burn = Timer(4)
    sleep = Timer(5)
    for iter in range(10):
        print(f'---------------{iter}----------------')
        if poison.event():
            print(iter, "Je prend des dégats de poison")
        if burn.event():
            print(iter, "Je prend des dégats de burn")
        sleep.event()
        print(f'sleep : {sleep.time - sleep.time_stamp}')

        Timer.time_update()
