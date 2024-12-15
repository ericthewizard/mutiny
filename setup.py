#Uploading new versions to pypi:
#
#python setup.py sdist
#twine upload dist/*
#Username MAVENSDC


#################################
#Uploading new versions to conda:
##################################

#Note: You'll need to make sure cdflib is up to date on conda as well

#Run: conda skeleton pypi mutinyplot
#This should generate a meta.yaml file
#Edit the YAML file so that the requirements/about/extra look like this:


'''
requirements:
  build:
    - setuptools
    - twine
    - python
    - pip
  run:
    - python
    - numpy
    - bokeh
    - pandas
    - matplotlib
    - scipy
    - xarray
    - pyqtgraph
    - cdflib

about:
  home: "https://github.com/MAVENSDC/mutinyplot"
  license: "MIT"
  summary: "mutinyplot is an effort to replicate the functionality IDL tplot library in python"
  doc_url: "https://github.com/MAVENSDC/mutinyplot"
  dev_url: "https://github.com/MAVENSDC/pyptlot"

extra:
  recipe-maintainers:
    - MAVENSDC
'''



#conda-build mutinyplot
#conda-build --python 3.6 mutinyplot
#conda-build --python 3.5 mutinyplot
#This should put stuff in C:/Anaconda/conda-bld
#conda convert -f --platform all /path/to/created/bundles/file.tar.bz2 -o /path/to/place/converted/files
#anaconda upload /path/to/created/or/converted/bundles/file.tar.bz2
#Username MAVENSDC

from setuptools import setup
setup()
