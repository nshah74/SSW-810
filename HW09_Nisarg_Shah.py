from collections import defaultdict
import os
from prettytable import PrettyTable


class Student:

    def __init__(self, p_info):
        if len(p_info) == 2 or any([item.isspace() for item in p_info]) or '' in p_info:
            raise ValueError("Missing basic information of students!")

        self.CWID, self.name, self.major = p_info
        self.courses = defaultdict(int)

    def add_stu_course(self, course, grade):
        self.courses[course] = grade

    def pr_student(self):
        return [self.CWID, self.name, sorted(self.courses.keys())]


class Instructor:

    def __init__(self, p_info):
        if len(p_info) == 2 or any([item.isspace() for item in p_info]) or '' in p_info:
            raise ValueError("Missing basic information of instructors!")

        self.CWID, self.name, self.department = p_info
        self.courses = defaultdict(int)

    def add_ins_course(self, course):

        self.courses[course] += 1

    def pr_instructor(self):

        for course, count in self.courses.items():
            yield [self.CWID, self.name, self.department, course, count]


class Repository:

    def __init__(self, dir_path):

        self.students_path = os.path.join(dir_path, 'students.txt')
        self.instructors_path = os.path.join(dir_path, 'instructors.txt')
        self.grades_path = os.path.join(dir_path, 'grades.txt')
        try:
            os.chdir(dir_path)
        except FileNotFoundError:
            raise NotADirectoryError ("Please provide a valid directory")

        self.students = dict()
        self.instructors = dict()

        self.students_pth()
        self.instructors_pth()
        self.grades_pth()

        self.print_student_table()
        self.print_instructor_table()

    def file_reader(self, file_path):

        try:
            file = open(file_path, 'r')
        except FileNotFoundError as e:
            print('Error! Cannot open file {}'.format(file_path))
        else:
            with file:
                for line in file:
                    yield line.strip().split('\t')

    def students_pth(self):

        for p_info in self.file_reader(self.students_path):
            CWID, name, major = p_info

            if CWID not in self.students:
                self.students[p_info[0]] = Student(p_info)

    def instructors_pth(self):

        for p_info in self.file_reader(self.instructors_path):
            self.instructors[p_info[0]] = Instructor(p_info)

    def grades_pth(self):

        for CWID_stu, course, grade, CWID_ins in self.file_reader(self.grades_path):
            if CWID_stu not in self.students.keys():
                raise ValueError('Student CWID {} is not in the student system.'.format(CWID_stu))

            if CWID_ins not in self.instructors.keys():
                raise ValueError('Instructor CWID {} is not in the instructor system.'.format(CWID_stu))

            self.students[CWID_stu].add_stu_course(course, grade)
            self.instructors[CWID_ins].add_ins_course(course)

    def print_student_table(self):

        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Completed Courses'])
        for person in self.students.values():
            pt.add_row(person.pr_student())

    def print_instructor_table(self):

        pt = PrettyTable(field_names=['CWID', 'Name', 'Department', 'Courses', 'Student Num'])
        for person in self.instructors.values():
            for c in person.pr_instructor():
                pt.add_row(c)

def main():
    dir_path = 'C:\Stevens\Fall2019\SSW-810\Stevens'
    stevens = Repository(dir_path)


if __name__ == '__main__':
    main()
