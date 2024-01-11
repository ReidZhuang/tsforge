from setuptools import setup, find_packages
setup(name='TSEngine',
      version='1.0',
      description='A tool to read in time serie data and produce feature-fashion data which is modelling ready.',
      author='ReidZ',
      author_email='reid.zhuang@icloud.com',
      requires= ['numpy','scipy'], 
      packages=find_packages(),
      package_data={"TSEngine": ["demo.ipynb"], "TSEngine": ["README.md"], "TSEngine":["LICENSE"], "TSEngine":["NOTICE"]},
      license="Apache License 2.0",
      install_requires=['numpy','scipy']
      )