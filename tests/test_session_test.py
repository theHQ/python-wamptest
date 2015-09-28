import wamptest
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


class ExampleTestCase(wamptest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ExampleTestCase, self).__init__(*args, **kwargs)
        self.update = None

    @inlineCallbacks
    def test_1(self):
        result = yield self.call("test.add", 1, 2)
        self.assertEqual(3, result)

    def receive_update(self, update=None):
        self.update = update

    @inlineCallbacks
    def test_2(self):
        self.subscribe(self.receive_update, topic="test.trigger.update")

        yield self.call("test.trigger")

        yield sleep(2)

        self.assertEqual("test", self.update)


if __name__ == '__main__':
    code = wamptest.wamptest.main(
        test_cases=[ExampleTestCase],
        url=u"ws://router:8080/ws",
        realm=u"realm1"
    )

    exit(code)
