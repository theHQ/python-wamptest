from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth


class TestSession(ApplicationSession):

    def onConnect(self):
        if self.config.realm == "realm2":
            self.join(self.config.realm, [u"wampcra"], u"user")
        else:
            super(TestSession, self).onConnect()

    def onChallenge(self, challenge):
        if challenge.method == u"wampcra":
            signature = auth.compute_wcs(
                u"secret".encode('utf8'),
                challenge.extra['challenge'].encode('utf8')
            )
            return signature.decode('ascii')
        else:
            raise Exception("don't know how to handle authmethod {}".format(challenge.method))

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

        def trigger_error():
            raise Exception("This happened")

        self.register(trigger_error, "test.trigger.error")
        print "Registered Trigger Error"
