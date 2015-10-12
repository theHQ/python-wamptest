import unittest
import wamptest


class MainLifecycleTests(unittest.TestCase):

    class ExampleTestCase(wamptest.TestCase):

        _setup_class_count = 0
        _setup_count = 0
        _teardown_count = 0
        _teardown_class_count = 0

        # TEST OVERRIDE
        @classmethod
        def connect(cls, test_runner=None, *args, **kwargs):
            cls.test_runner = test_runner
            test_session = cls(None)
            test_session.onJoin(None)

        @classmethod
        def setUpClass(cls):
            cls._setup_class_count += 1

        @classmethod
        def tearDownClass(cls):
            cls._teardown_class_count += 1

        def setUp(self):
            self.__class__._setup_count += 1

        def tearDown(self):
            self.__class__._teardown_count += 1

        def test_1(self):
            self.assertTrue(True)

        def test_2(self):
            self.assertTrue(True)

        def test_3(self):
            self.assertTrue(False)

    def test_lifecycle(self):
        wamptest.TestCase.quiet = True
        wamptest.TestCase.test = True

        result = wamptest.main(
            test_cases=[self.ExampleTestCase, self.ExampleTestCase],
            url=u"test",
            realm=u"test",
            quiet=True,
            test=True
        )

        self.assertEqual(2, result)
        self.assertEqual(2, self.ExampleTestCase._setup_class_count)
        self.assertEqual(2, self.ExampleTestCase._teardown_class_count)
        self.assertEqual(6, self.ExampleTestCase._setup_count)
        self.assertEqual(6, self.ExampleTestCase._teardown_count)
