""" Unit test for FinalAssignment.py. """

import unittest
import FinalAssignment as fA


class TestFinal(unittest.TestCase):
    """ Unit test object with methods to test FinalAssignment.py. """
    def test_complete_data(self):
        test_dataset = fA.DataSet()
        test_dataset.load_file()
        self.assertEqual(6147, len(test_dataset._data))


if __name__ == '__main__':
    unittest.main()
