from distutils.core import setup
setup(
    name='wamptest',
    packages=['wamptest'],
    version='0.2',
    description='This is a library designed to test WAMP Crossbar connections',
    author='Eric Chapman',
    author_email='eric@headquartershq.com',
    url='https://github.com/headquartershq/python-wamptest',
    download_url='https://github.com/headquartershq/python-wamptest/tarball/0.2',
    keywords=['testing', 'wamp', 'crossbar'],
    install_requires=['crossbar'],
    classifiers=[],
)
