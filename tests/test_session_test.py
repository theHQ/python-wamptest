import wamptest
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep


class ExampleTestCase1(wamptest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ExampleTestCase1, self).__init__(*args, **kwargs)
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


class ExampleTestCase2(wamptest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ExampleTestCase2, self).__init__(*args, **kwargs)
        self.update = None

    @inlineCallbacks
    def test_1(self):
        result = yield self.call("test.add", 1, 2)
        self.assertEqual(3, result)


if __name__ == '__main__':
    code = wamptest.wamptest.main(
        test_cases=[ExampleTestCase1, ExampleTestCase2],
        url=u"ws://router:8080/ws",
        realm=u"realm1"
    )

    exit(code)
