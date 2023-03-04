import path
import pickle
import sys
import unittest

folder = path.Path(__file__).abspath()
sys.path.append(folder.parent.parent)

from commands import Record, Name, Birthday, Phone


class TestRecord(unittest.TestCase):

      def setUp(self):
            self.record = Record(name=Name('Bob'))

      def test_no_dublicate_with_same_name(self):
            compared_1 = Record(name=Name('Bob'))
            compared_2 =Record(name=Name('Ben'))
            self.assertEqual(self.record, compared_1)
            self.assertIs(self.record, compared_1)
            self.assertNotEqual(self.record, compared_2)
            self.assertIsNot(self.record, compared_2)
      
      def test_phone_adding(self):
            phone_1 = Phone('0992968789')
            phone_2 = Phone('(065)5521122')
            Record(name=Name('Bob'), phones=[phone_1])
            Record(name=Name('Bob'), phones=[phone_2])
            self.assertTrue(phone_1 in self.record.phones)
            self.assertTrue(phone_2 in self.record.phones)
      
      def test_days_to_byrthday(self):
            birthday = Birthday('29.03.1995')
            Record(name=Name('Bob'), birthday=birthday)
            
        
        
if __name__ == '__main__':
      unittest.main()