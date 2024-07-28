from setuptools import setup 
  
setup( 
    name='cloud', 
    version='1.0', 
    description='A module that can create cloud server.', 
    author='WTech', 
    author_email='wangtry3417@gmail.com', 
    packages=['wcloud'], 
    install_requires=[ 
        'docker'
    ], 
) 
