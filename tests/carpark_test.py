import unittest
import sys,os
from pathlib import Path
cwd = Path(os.path.dirname(__file__))
parent = str(cwd.parent)

sys.path.append(parent + "/smartpark")

#Change the line below to import your manager class
from smartpark.carpark import CarparkManager

class TestConfigParsing(unittest.TestCase):

    def test_fresh_carpark(self):
        # arrange
        # act
        carpark = CarparkManager()
        # assert
        self.assertEqual(1000,carpark.available_spaces)

if __name__=="__main__":
#    print("cwd: " + parent + "/smartpark")
    unittest.main()
