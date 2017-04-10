# radarplot 

A library to read the CIKM AnalaytiCup 2017 dataset.

radarplot is a library intended to read efficiently the dataset released for the CIKM AnalytiCup 2017 competiton (`train.txt`) and map it to Python objects. The dataset `train.txt` is 17.1 GB long but this library takes `O(1)` to read any of the 600,000 radar maps in the dataset. The information of the different Stacks and Layers of each sequence are easily accesible in the Radar object (all the structure within Radar object can be visualized in a plot).

Installation
------------

This library is not published in the pip platform, so if you want to install you can do it manually following these steps:

```shell
git clone https://github.com/jpcano/radarplot.git
cd radarplot
pip3 install -e .
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

### Notes

The first time that the CIKM constructor is called it will take some time to generate the file `train.index`.
The next calls to that constructor will detect the index file and they will use it to speed up the random access to the images.

### More examples

You can have a look at the project [radarweb](https://github.com/jpcano/radarweb). It implements a client that uses this library to generate this [web](http://jesus.engineer/radarweb).

Tests
-----

There is a unitary test suite that can be run with the following command:

```shell
make test
```

TODO
----

- Autogenerate the API docummentation.
- Continuous Integration with Travis.
- Integrate codecov.io with Travis for automatic test coverage reports.

License
-------

GNU GPLv3, see [LICENSE](LICENSE)
