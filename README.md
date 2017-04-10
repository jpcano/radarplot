# radarplot 

A library to read the CIKM AnalaytiCup 2017 dataset.

radarplot is a library intended to read efficiently the dataset released for the CIKM AnalytiCup 2017 competiton (`train.txt`) and map it to Python objects. The dataset `train.txt` is 17.1 GB but this library takes `O(1)` to read any of the 10000 radar sequences in the dataset. The information of the different Stacks and Layers of each sequence are easyly accesible from the Radar object (and plotable).

Installation
------------

This library is not published in pip platform so if you want to install it in you own system you can do the following:

```shell
git clone https://github.com/jpcano/radarplot.git
cd radarplot
pip pip3 install .
```

Quick Guide
-----------

Plot the 2nd layer of the 7th stack of the location number 134 in the dataset:

```python
from radarplot.CIKM import *
cikm = CIKM('train.txt', 'train.index')
cikm.getRadars(134).getStack(6).getLayer(1).plot()
```

You can save it as a png file in the current directory:

```python
from radarplot.CIKM import *
cikm = CIKM('train.txt', 'train.index')
cikm.getRadars(134).getStack(6).getLayer(1).plot('great_image')
```

Shows an animated radar map from the radar location 3 in the dataset:

```python
from radarplot.CIKM import *
cikm = CIKM('train.txt', 'train.index')
cikm.getRadar(3).plot()
```

This saves all the radar maps (as mp4 sequences) in the directory 'vid':

```python
from radarplot.CIKM import *
cikm = CIKM('train.txt', 'train.index')
for radar in cikm.getAllRadars():
	radar.plot('vid/' + radar.getID() + '.mp4')`
```

It is possible to save the images in reversed sorted order of the labels:

```python
from radarplot.CIKM import *
cikm = CIKM('train.txt', 'train.index')
for radar in cikm.getAllRadars(sorted=True, reversed=True):
	radar.plot('vid/' + radar.getID() + '.mp4')
```

Notes
-----

The first time that tyhe CIKM constructor is executed will take some time to generate the index file train.index.
The next calls to that constructor will detect the index file and it will use it to speed up the random access to the images.

Tests
-----

There is a unitary test suite that can be run with the following command:

```shell
make test
```

TODO
----

- Continuous Integration with Travis.
- Integrate codecov.io with Travis for automatic test coverage reports.
- Autogenerate the API docummentation.

License
-------

GNU GPLv3, see [LICENSE](LICENSE)
