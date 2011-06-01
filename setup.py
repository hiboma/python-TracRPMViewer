from setuptools import setup

PACKAGE = 'TracRPMViewer'
VERSION = '0.1'

setup(name=PACKAGE,
      version=VERSION,
      packages=['rpmviewer'],
      entry_points={'trac.plugins': '%s = rpmviewer' % PACKAGE},
)
