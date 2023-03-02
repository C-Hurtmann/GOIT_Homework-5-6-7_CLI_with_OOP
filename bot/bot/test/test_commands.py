import unittest

from bot.commands import Record, Name, Birthday, Phone


class TestRecord(unittest.TestCase):
    
    def setUp(self):
        self.record = Record(Name('Bob'))
        
    def test_no_same_name_dublicate(self):
        compared = Record(Name('Ben'))
        self.assertEqual(self.record, compared)