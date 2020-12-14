
import os
import setuptools
from version import version as this_version

this_directory =  os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(this_directory, 'ArtSciColor', '_version.py')
with open(version_path, 'wt') as fversion:
    fversion.write('__version__ = "'+this_version+'"')


REQUIRED_PACKAGES=[
    'matplotlib>=3.3.2', 'plotly>=4.13.0',
    'colour>=0.1.5'
]


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="ArtSciColor",                                                
    install_requires=REQUIRED_PACKAGES,                         
    version=this_version,                                      
    author="chipdelmal",                                        
    scripts=[],                                                 
    author_email="chipdelmal@gmail.com",                        
    description="Color palettes for scientific purposes",       
    long_description=long_description,                          
    long_description_content_type="text/markdown",              
    url="https://github.com/Chipdelmal/ArtSciColor",                   
    packages=setuptools.find_packages(),                        
    classifiers=[                                               
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',                                    # python version requirement
)