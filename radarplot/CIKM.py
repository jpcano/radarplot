# -*- coding: utf-8 -*-

"""
Module to read the dataset and map the data to objects
"""

from radarplot.radartypes import *
import json
import os.path
import numpy as np

class CIKM (object):
    """Abstract class for reading the dataset and mapping to objets"""

    def __init__(self, filename, indexfile, nlayers=4, nticks=15, mapdim=101):
        self.filename = filename
        self.nlayers = nlayers
        self.nticks = nticks
        self.mapdim = mapdim
        self.radarslots = self.mapdim**2
        # index.dump
        if (os.path.isfile(indexfile)):
            self.index = self._loadIndex(indexfile)
        else:
            # print("Generating {}...".format(indexfile))
            self.index = list(self._line_ind(self.filename))
            self._writeIndex(indexfile, self.index)
            # print('done')
        # sorted_index.dump
        self.sorted_index = sorted(self.index, key=lambda x: x[0])
        self.size = len(self.index)

    def _loadIndex(self, filename):
        """Load an index file from disc"""
        with open(filename) as f:
            return json.loads(f.read())

    def _writeIndex(self, filename, data):
        """Writes an index file to disc"""
        with open(filename,'w') as f:
            f.write(json.dumps(data))

    def _line_ind(self, filename):
        """Yield succesive labels and positions (in bytes) of the lines in 
        the file."""
        p = 0
        with open(filename) as fileobj:
            for line in fileobj:
                label = line.split(',')[1]
                yield [float(label), p]
                p += len(line)

    def __getFirst64(self, n, sorted, reversed):
        """Return the first 64 charaters of the line n of the file `filename'."""
        with open(self.filename) as f:
            index = self.getSize()-n-1 if reversed else n
            if(sorted):
                    f.seek(self.sorted_index[index][1])
            else:
                f.seek(self.index[index][1])
            return f.read(64)
        
    def __getLine(self, n, sorted, reversed):
        """Return the line n of the file `filename'. It uses an iterator
        (enumerate) so during the search it only loads into memory one 
        line at a time. Takes O(n)"""
        with open(self.filename) as f:
            index = self.getSize()-n-1 if reversed else n
            if(sorted):
                    f.seek(self.sorted_index[index][1])
            else:
                f.seek(self.index[index][1])
            return f.readline()

    def __getIdLabel(self, n, sorted, reversed):
        """Returns a tuple with the information: (id, label)
        where radarmap is a list of numbers in the format define of the spec"""
        rawmap =  self.__getFirst64(n, sorted, reversed).split(',')
        return (rawmap[0], float(rawmap[1]))

    def __getRawMap(self, n, sorted, reversed):
        """Returns a tuple with the map information: (id, label, radarmap)
        where radarmap is a list of numbers in the format define of the spec"""
        rawmap =  self.__getLine(n, sorted, reversed).split(',')
        dbz = [int(x) for x in rawmap[2].split()]
        return (rawmap[0], float(rawmap[1]), dbz)

    def _getLayerData(self, rawlayer):
        """Returns 2D array ([[row0], [row1], ..., [rowN]] from rawlayer 
        which has the format [row0row1...rowN]."""
        return rawlayer.reshape(-1, self.mapdim)

    def getSize(self):
        """Returns the number of target maps in the dataset"""
        return self.size

    def getMapDimension(self):
        return self.mapdim

    def getIdLabelRange(self, ini, end, sorted=False, reversed=False):
        """Yields a tuple (idmap, label) sucessively between ini and end."""
        for idx in range(ini, end):
            (idmap, label) = self.__getIdLabel(idx, sorted, reversed)
            yield (idmap, label)

    def getIdLabel(self, idx, sorted=False, reversed=False):
        """Returns a tuple (idmap. label) in the index idx positon in the 
        dataset"""
        return list(self.getRadarRange(idx, idx + 1, sorted, reversed))[0]

    def getAllIdLabels(self, sorted=False, reversed=False):
        """Yield sucessively all the tuples (idmap, label) objects in the 
        dataset"""
        for radar in self.getRadarRange(0, self.getSize(), sorted, reversed):
            yield radar
    
    def getRadarRange(self, ini, end, sorted=False, reversed=False):
        """Yields a Radar object sucessively between ini and end."""
        for idx in range(ini, end):
            (idmap, label, radardata) = self.__getRawMap(idx, sorted, reversed)
            radar = Radar(idmap, label)
            stackn = 0
            stack = RadarStack(radar, stackn)
            for i, l in enumerate(np.uint8(radardata).reshape(-1, self.radarslots)):
                layern = i % self.nlayers
                layer = RadarLayer(self._getLayerData(l), radar, stackn, layern)
                stack.addLayer(layer)
                if (layern == self.nlayers - 1):
                    radar.addStack(stack)
                    stackn += 1
                    stack = RadarStack(radar, stackn)
            yield radar

    def getRadar(self, idx, sorted=False, reversed=False):
        """Returns a Radar object in the index idx positon in the dataset"""
        return list(self.getRadarRange(idx, idx + 1, sorted, reversed))[0]

    def getAllRadars(self, sorted=False, reversed=False):
        """Yield sucessively all the Radars objects in the dataset"""
        for radar in self.getRadarRange(0, self.getSize(), sorted, reversed):
            yield radar
