#!/usr/bin/env python
# coding: utf-8

import unittest
from MapPosition import MapPosition

class MapPositionTests(unittest.TestCase):

    def test_fromNormalized_center(self):
        result = MapPosition.fromNormalized(0.5,0.5)        
        self.assertAlmostEqual(0, result.longitude)
        self.assertAlmostEqual(0, result.latitude)

    def test_fromNormalized_topRight(self):
        result = MapPosition.fromNormalized(1,1)
        self.assertAlmostEqual(180, result.longitude)
        self.assertAlmostEqual(90, result.latitude)

    def test_fromNormalized_bottomLeft(self):
        result = MapPosition.fromNormalized(0,0)
        self.assertAlmostEqual(-180, result.longitude)
        self.assertAlmostEqual(-90, result.latitude)



    def test_getTileIndices_center_zoomZero(self):
        position = MapPosition.fromNormalized(0,0)
        result = position.getTileIndicesGoogle(0)
        self.assertEqual(0, result[0])
        self.assertEqual(0, result[1])

    def test_getTileIndices_lowerLeft_zoomOne(self):        
        position = MapPosition.fromNormalized(0.25, 0.25)
        result = position.getTileIndicesGoogle(1)
        self.assertEqual(0,result[0])
        self.assertEqual(1,result[1])

    def test_getTileIndices_upperRight_zoomOne(self):
        position = MapPosition.fromNormalized(0.75, 0.75)
        result = position.getTileIndicesGoogle(1)
        self.assertEqual(1, result[0])
        self.assertEqual(0, result[1])

    def test_getTileIndices_lowerLeft_zoomTwo(self):        
        position = MapPosition.fromNormalized(0.125, 0.125)
        result = position.getTileIndicesGoogle(2)
        self.assertEqual(0,result[0])
        self.assertEqual(3,result[1])

    # def test_true(self):
    #     self.assertTrue(True)

    # def test_raises(self):
    #     with self.assertRaises(Exception):
    #         raise Exception


if __name__ == '__main__':
    unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(MapPositionTests)
unittest.TextTestRunner(verbosity=2).run(suite)