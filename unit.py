from UIT.task import GoldSeem

__author__ = 'Тищенко Данило КН-45'

import unittest


class MyTestCase(unittest.TestCase):
    def test_goldseemX(self):
        gs = GoldSeem(-2, 2, 0.1, "1/x+5")
        gs.calc_func()
        # тестування ториманого значення по X
        self.assertEqual(181.31950780985727, gs.X)

    def test_goldseemY(self):
        gs = GoldSeem(-2, 2, 0.1, "1/x+5")
        gs.calc_func()
        # тестування ториманого значення по Y
        self.assertEqual(66.6424398095538, gs.Y)

if __name__ == '__main__':
    unittest.main()
