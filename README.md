#WAMPTEST

**wamptest** is a library created for testing WAMP services that is based on "unittest".  The Twisted library uses a
method called "defers" with a reactor which is not friendly to the unittest library.  I tried using "Trial" but it was
also not suiting my needs since it needs to run a reactor.  I wanted something that allowed test suites to be created
for connecting to an actual router.

The library creates a class called "wamptest.TestCase" that subclasses from "autobahn.twisted.wamp.ApplicationSession" 
which will allow it to connect to a router.  When you call "main" it will iterate through an array of test cases
that will do the following

  - For each test case in the test cases
    - Connect to the router using an ApplicationRunner
    - Iterate through the tests (any method that start with "test_")
    - Gather pass/fail information
    - Stop the reactor
  - Print Pass/Fail summary.
  
The test is run by calling "main".  Here is an example

    code = wamptest.main(
        test_cases=[ExampleTestCase1, ExampleTestCase2],
        url=u"ws://router:8080/ws",
        realm=u"realm1"
    )
    
It supports the following "unittest" like life cycle callbacks

  - setUpClass(cls): Called once at the start of the Test Case
  - setUp(self): Called once before each test
  - tearDown(self): Called once after each test
  - tearDownClass(cls): Called once at the end of the Test Case
    
It supports the following "unittest" like asserts

  - assertEqual(a, b)
  - assertNotEqual(a, b)
  - assertIsNone(a)
  - assertIsNotNone(a)
  - assertTrue(a)
  - assertFalse(a)
  - assertGreater(a, b)
  - assertGreaterEqual(a, b)
  - assertLess(a, b)
  - assertLessEqual(a, b)
  
Writing tests must use inlineCallbacks to halt the test until completion.  An example is as follows

    class ExampleTestCase(wamptest.wamptest.TestCase):
    
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

At the completion of a test, a summary will be printed to the screen that looks something like the following

    Connecting to the url: 'ws://router:8080/ws', realm: 'realm1'

    Result: PASSED
        Tests: 2
        Passes: 2
        Failures: 0
        Errors: 0

Results are defined as follows

  - UNKNOWN: No passes, no failures, no errors
  - PASSED: At least 1 pass, no failures, no errors
  - FAILED: At least 1 failure or error

#Contributing
To contribute, fork the repo and submit a pull request.  I have the following known "TODO"s.

##TODOs

  - Implement authenticated connections
  - Make library discover test cases so you don't need to pass them in
  - Exit on Exceptions (deferred library catches them on callbacks)
  - When a failure is sensed in a test, the test still continues but the remaining errors are suppressed.  Will need
    to figure out how to end the tests

#Testing
The unit tests can be run with

    %> python /tests/run_tests.py
    
This will test basic functionality.  The overall system test (which will also run the unit tests) can be run by using
Docker Compose.  Connect to a docker host and type

    %> docker-compose build
    %> docker-compose up
    
This will run the unit tests as well as the system level tests.  The service "wamptest_test_1" will return a 0 value
if the tests were successful and non zero otherwise.  To get the pass/fail results from a command line, do the following

    #!/usr/bin/env bash
    
    docker-compose build
    docker-compose up
    
    exit $(docker-compose ps -q | xargs docker inspect -f '{{ .Name }} exited with status {{ .State.ExitCode }}' | grep test_1 | cut -f5 -d ' ')

This is a little hacky (and hopefully Docker will fix it) but it will do the trick for now.

The Docker Compose file creates a generic router with an example service connected to it and then creates a test suite 
using "wamptest" to test the service.

#License
MIT
