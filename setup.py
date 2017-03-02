from setuptools import setup

setup(name='slack-activity-report',
      version='1.0.0',
      url='https://github.com/kcct-fujimotolab/slack-activity-report',
      packages=['activityreport', 'activityreport.slackbot'],
      entry_points={
          'console_scripts': [
              'slack-activity-report = activityreport.main:main'
          ],
      },
      install_requires=[
          'slackclient',
          'ArrayImage'
      ],
      dependency_links=[
          'git+https://github.com/rysmarie/python-ArrayImage.git#egg=ArrayImage'
          ],
      )
