from setuptools import setup, find_packages

setup(
    name='longtroll',
    version='1.0',
    license='MIT License',
    url='https://github.com/haldean/longtroll',
    long_description=open('README.rst').read(),

    author='Will Haldean Brown',
    author_email='will.h.brown@gmail.com',

    packages = find_packages(),
    scripts = ['longtroll/longtroll.py'],

    install_requires = [
      'argparse',
      ],

    package_data = {
      '': ['README.md', 'longtrollrc-sample'],
      }
    )
