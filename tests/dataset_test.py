# -*- coding: utf-8 -*-

import unittest
import context
from CIKM import *

filename = 'data/data_sample.txt'
indexfile = 'data/data_sample.index'
cikm = CIKM(filename, indexfile)

class TestSuite(unittest.TestCase):
    """TestSuite"""
    def getLine(self, filename, n):
        """Return the line n of the file `filename'. It uses an iterator
        (enumerate) so during the search it only loads into memory one 
        line at a time. Takes O(n)"""
        with open(filename) as f:
            for i, line in enumerate(f):
                if i == n:
                    return line

    def getMapData(self, filename, line):
        """Get map data as a list of integers (dbZ)"""
        rawmap =  self.getLine(filename, line).split(',')
        mapdata = [int(x) for x in rawmap[2].split()]
        return mapdata

    def flatten(self, cikm, radar):
        """Flatten the map data embedded in Radar object"""
        raw = []
        for s in radar.getAllStacks():
            for l in s.getAllLayers():
                for x in range(0, cikm.getMapDimension()):
                    for y in range(0, cikm.getMapDimension()):
                        raw.append(l.getValue(x, y))
        return raw
    
    def test_map0(self):
        """Test if we have mapped correctly the map 0 into the Radar 
        object"""
        self.maxDiff = None
        radar = cikm.getRadar(0)
        self.assertEqual(self.getMapData(filename, 0),
                         self.flatten(cikm, radar))

    def test_mapInter(self):
        """Test if we have mapped correctly a intermediate map into the 
        Radar object"""
        size = cikm.getSize()
        inter = int(size / 2)
        radar = cikm.getRadar(inter)
        self.assertEqual(self.getMapData(filename, inter),
                         self.flatten(cikm, radar))

    def test_mapLast(self):
        """Test if we have mapped correctly the last map into the Radar 
        object"""
        size = cikm.getSize()
        last = size - 1
        radar = cikm.getRadar(last)
        self.assertEqual(self.getMapData(filename, last),
                         self.flatten(cikm, radar))

if __name__ == '__main__':
    unittest.main()
