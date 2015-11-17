from distutils.core import setup
setup(
    name='wamptest',
    packages=['wamptest'],
    version='0.3.3',
    description='This is a library designed to test WAMP Crossbar connections',
    author='Eric Chapman',
    license='MIT',
    author_email='eric@thehq.io',
    url='https://github.com/thehq/python-wamptest',
    keywords=['testing', 'wamp', 'crossbar'],
    install_requires=['crossbar'],
    classifiers=[],
)
