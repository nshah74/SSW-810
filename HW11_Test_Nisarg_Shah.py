from HW11_Nisarg_Shah import Repository

import unittest

class TestStudent(unittest.TestCase):

    def test_Student(self):
        """Testing the Student Class"""
        stevens = Repository('C:\Stevens\Fall2019\SSW-810\Stevens')
        self.assertEqual(stevens.students['10115'].name, 'Bezos, J')
    
    def test_Major(self):
        """Testing the Major Class"""
        stevens = Repository('C:\Stevens\Fall2019\SSW-810\Stevens')
        self.assertEqual(stevens.majors['CS'].required, {'CS 546', 'CS 570'})
    
    def test_Instructor(self):
        """Testing the Instructor Class"""
        stevens = Repository('C:\Stevens\Fall2019\SSW-810\Stevens')
        self.assertEqual(stevens.instructors['98763'].courses, {'SSW 810': 4, 'SSW 555': 1})
    
class DBTest(unittest.TestCase):

    def test_Instructor_table_db(self):
        stevens = Repository("C:\Stevens\Fall2019\SSW-810\Stevens")
        self.assertEqual(stevens.instructor_table_db('810_startup.db'),[('98764', 'Cohen, R', 'SFEN', 'CS 546', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1), ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4), ('98762', 'Hawking, S', 'CS', 'CS 501', 1), ('98762', 'Hawking, S', 'CS', 'CS 546', 1), ('98762', 
                                                                        'Hawking, S', 'CS', 'CS 570', 1)])

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
 
