import logging

class Car(object):

    def factory(type, num):
        if type == "Racecar":
            return Racecar(num)
        if type == "Van":
            return Van(num)
        assert 0, "Bad car creation: " + type

    factory = staticmethod(factory)

class Racecar(Car):
    def __init__(self, num):
        print "you selected ", num, " racecar"
    def drive(self): print("Racecar driving.")
    def drive2(self): print("Reac")

class Van(Car):
        def __init__(self, num):
            print "you selected ", num , " Van"
        def drive(self): print("Van driving.")
        def drive2(self): print("vanc")

# Create object using factory.
obj = Car.factory("Racecar", 15)

#obj.drive()
#obj.drive2()
#logging.warning('Im seeng you')
