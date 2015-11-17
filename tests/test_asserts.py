import unittest
import wamptest
from autobahn.wamp.exception import ApplicationError


class BaseTestCaseTests(unittest.TestCase):

    def setUp(self):
        self.klass = wamptest.TestCase
        self.klass.quiet = True
        self.wamptest = self.klass(None)
        self.wamptest.reset()

    def check_counters(self, passes, fails, errors):
        self.assertEqual(passes, self.wamptest.passes)
        self.assertEqual(fails, self.wamptest.failures)
        self.assertEqual(errors, self.wamptest.errors)

    def check_pass(self):
        self.check_counters(1, 0, 0)

    def check_fail(self):
        self.check_counters(0, 1, 0)

    def check_error(self):
        self.check_counters(0, 0, 1)

class TestCaseAssertTests(BaseTestCaseTests):

    def test_equal_pass(self):
        result = self.wamptest.assertEqual(1, 1)
        self.assertTrue(result)
        self.check_pass()

    def test_equal_fail(self):
        result = self.wamptest.assertEqual(1, 2)
        self.assertFalse(result)
        self.check_fail()

    def test_not_equal_pass(self):
        result = self.wamptest.assertNotEqual(1, 2)
        self.assertTrue(result)
        self.check_pass()

    def test_not_equal_fail(self):
        result = self.wamptest.assertNotEqual(1, 1)
        self.assertFalse(result)
        self.check_fail()

    def test_is_none_pass(self):
        result = self.wamptest.assertIsNone(None)
        self.assertTrue(result)
        self.check_pass()

    def test_is_none_fail(self):
        result = self.wamptest.assertIsNone("")
        self.assertFalse(result)
        self.check_fail()

    def test_is_not_none_pass(self):
        result = self.wamptest.assertIsNotNone("")
        self.assertTrue(result)
        self.check_pass()

    def test_is_not_none_fail(self):
        result = self.wamptest.assertIsNotNone(None)
        self.assertFalse(result)
        self.check_fail()

    def test_is_true_pass(self):
        result = self.wamptest.assertTrue(True)
        self.assertTrue(result)
        self.check_pass()

    def test_is_true_fail(self):
        result = self.wamptest.assertTrue(False)
        self.assertFalse(result)
        self.check_fail()

    def test_is_false_pass(self):
        result = self.wamptest.assertFalse(False)
        self.assertTrue(result)
        self.check_pass()

    def test_is_false_fail(self):
        result = self.wamptest.assertFalse(True)
        self.assertFalse(result)
        self.check_fail()

    def test_greater_pass(self):
        result = self.wamptest.assertGreater(3, 2)
        self.assertTrue(result)
        self.check_pass()

    def test_greater_fail_equal(self):
        result = self.wamptest.assertGreater(3, 3)
        self.assertFalse(result)
        self.check_fail()

    def test_greater_fail_less(self):
        result = self.wamptest.assertGreater(2, 3)
        self.assertFalse(result)
        self.check_fail()

    def test_greater_equal_pass(self):
        result = self.wamptest.assertGreaterEqual(3, 2)
        self.assertTrue(result)
        self.check_pass()

    def test_greater_equal_pass_equal(self):
        result = self.wamptest.assertGreaterEqual(3, 3)
        self.assertTrue(result)
        self.check_pass()

    def test_greater_equal_fail_less(self):
        result = self.wamptest.assertGreaterEqual(2, 3)
        self.assertFalse(result)
        self.check_fail()

    def test_less_pass(self):
        result = self.wamptest.assertLess(2, 3)
        self.assertTrue(result)
        self.check_pass()

    def test_less_fail_equal(self):
        result = self.wamptest.assertLess(3, 3)
        self.assertFalse(result)
        self.check_fail()

    def test_less_fail_less(self):
        result = self.wamptest.assertLess(3, 2)
        self.assertFalse(result)
        self.check_fail()

    def test_less_equal_pass(self):
        result = self.wamptest.assertLessEqual(2, 3)
        self.assertTrue(result)
        self.check_pass()

    def test_less_equal_pass_equal(self):
        result = self.wamptest.assertLessEqual(3, 3)
        self.assertTrue(result)
        self.check_pass()

    def test_less_equal_fail_less(self):
        result = self.wamptest.assertLessEqual(3, 2)
        self.assertFalse(result)
        self.check_fail()

    def test_raise_exception_pass(self):
        with self.wamptest.assertRaises(BaseException) as context:
            raise Exception("This was raised")
        self.check_pass()

    def test_raise_exception_fail(self):
        with self.wamptest.assertRaises(ApplicationError) as context:
            raise BaseException("This was raised")
        self.check_fail()

    def test_raise_exception_pass_runtime(self):
        with self.wamptest.assertRaises(RuntimeError) as context:
            raise ApplicationError(u"This was raised")
        self.check_pass()

    def test_raise_exception_fail_runtime(self):
        with self.wamptest.assertRaises(ApplicationError) as context:
            raise BaseException("This was raised")
        self.check_fail()

class TestMultiFail(BaseTestCaseTests):

    def test_back_to_back_fails(self):
        result = self.wamptest.assertTrue(False)
        self.assertFalse(result)
        result = self.wamptest.assertTrue(False)
        self.assertFalse(result)
        self.check_fail()  # Should only be 1 recorded failure