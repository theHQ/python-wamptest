from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


class TestSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def add(x, y):
            print "Add was called"
            return x + y

        self.register(add, "test.add")
        print "Registered Add"

        def trigger():
            print "Trigger was called"
            self.publish("test.trigger.update", update="test")

        self.register(trigger, "test.trigger")
        print "Registered Trigger"

        while True:
            yield sleep(1)
