from setuptools import setup

setup(name='slack-activity-report',
      version='1.0.0',
      url='https://github.com/kcct-fujimotolab/slack-activity-report',
      packages=['activityreport'],
      entry_points={
          'console_scripts': [
              'slack-activity-report = activityreport.main:main'
          ],
      },
      install_requires=[
          'slackclient',
          'ArrayImage',
          'python-dateutil',
          'click',
      ],
      dependency_links=[
          'git+https://github.com/rysmarie/python-ArrayImage.git#egg=ArrayImage'
      ],
      )
