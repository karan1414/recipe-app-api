""" Sample test """

from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):
    """ Test the calc module """

    def test_add_numbers(self):
        """ Adding numbers together """
        res = calc.add(5,6)

        self.assertEqual(res, 11)

    def subtract_numbers(self):
        """ Substract numbers together
        """
        res  = calc.substract(10, 15)

        self.assertEqual(res, 5)


        