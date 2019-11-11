from HW09_Nisarg_Shah import Repository

import unittest
import os
class TestRepository(unittest.TestCase):
    
    def test_stevens_info(self):

            stevens = Repository('C:\Stevens\Fall2019\SSW-810\Stevens')
        
            students_info = {'10103': ['10103', 'Baldwin, C', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'A-', 'SSW 687': 'B', 'CS 501': 'B'}],
                         '10115': ['10115', 'Wyatt, X', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'B+', 'SSW 687': 'A', 'CS 545': 'A'}],
                         '10172': ['10172', 'Forbes, I', 'SFEN', {'SSW 555': 'A', 'SSW 567': 'A-'}],
                         '10175': ['10175', 'Erickson, D', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'A', 'SSW 687': 'B-'}],
                         '10183': ['10183', 'Chapman, O', 'SFEN', {'SSW 689': 'A'}],
                         '11399': ['11399', 'Cordova, I', 'SYEN', {'SSW 540': 'B'}],
                         '11461': ['11461', 'Wright, U', 'SYEN', {'SYS 800': 'A', 'SYS 750': 'A-', 'SYS 611': 'A'}],
                         '11658': ['11658', 'Kelly, P', 'SYEN', {'SSW 540': 'F'}],
                         '11714': ['11714', 'Morton, A', 'SYEN', {'SYS 611': 'A', 'SYS 645': 'C'}],
                         '11788': ['11788', 'Fuller, E', 'SYEN', {'SSW 540': 'A'}]}
       
            instructors_info = {'98765': ['98765', 'Einstein, A', 'SFEN', {'SSW 567': 4, 'SSW 540': 3}], 
                            '98764': ['98764', 'Feynman, R', 'SFEN', {'SSW 564': 3, 'SSW 687': 3, 'CS 501': 1, 'CS 545': 1}], 
                            '98763': ['98763', 'Newton, I', 'SFEN', {'SSW 555': 1, 'SSW 689': 1}], 
                            '98762': ['98762', 'Hawking, S', 'SYEN', {}], 
                            '98761': ['98761', 'Edison, A', 'SYEN', {}], 
                            '98760': ['98760', 'Darwin, C', 'SYEN', {'SYS 800': 1, 'SYS 750': 1, 'SYS 611': 2, 'SYS 645': 1}]}
         

class TestStudent(unittest.TestCase):
    
    def test_num_student(self):
        nr = Repository('C:\Stevens\Fall2019\SSW-810\Stevens').students.keys()
        self.assertEqual(list(nr),['10103','10115','10172','10175','10183','11399','11461','11658','11714','11788'])

    def test_course_student(self):
        nr = Repository('C:\Stevens\Fall2019\SSW-810\Stevens').students["11714"].courses.keys()
        self.assertEqual(list(nr),['SYS 611', 'SYS 645'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)