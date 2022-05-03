from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from random import randint


class Course(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    code: str
    hours: int

    @property
    def abbr(self):
        return ''.join([s[0] for s in self.name.upper().split(' ')])

    def __eq__(self, course2):
        return self.code == course2.code

class Instructor(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    courses: Optional[List[Course]] = []

class Department(BaseModel):
    id:  UUID = Field(default_factory=uuid4)
    number: int
    name: str
    year: Optional[int] = None
    courses: Optional[List[Course]] = []
    faculty: Optional[List[Instructor]] = []
    sections: Optional[List[str]] = []

    @property
    def num_courses(self):
        return len(self.courses)

    def __eq__(self, dept2):
        return self.id == dept2.id 

class TimeTable:
    def __init__(self, num_lec=7):
        self.__root__ = []
        for i in range(5):
            self.__root__.append([None] * num_lec)

    def __str__(self):
        s = ''
        for d in self.__root__:
            s += str(d) + '\n'

        return s

    def is_full(self):
        for r in self.__root__:
            for c in r:
                if c is None: return False

        return True

    def __getitem__(self, key):
        if type(key) is int:
            return self.__root__[key]

    def __setitem__(self, key, newvalue):
        self.__root__[key[0]][key[1]] = newvalue

    def insert_random(self, newvalue):
        r = randint(0, 4)
        c = randint(0, 6)

        if self[r][c] is not None and not self.is_full():
            r = 0
            c = 0
            while (self[r][c] is not None):
                c += 1
                if c > 6:
                    r += 1
                    c = 0
                if r > 4:
                    break
            
        if self.is_full():
            return (-1, -1)
            
        self[r, c] = newvalue
        return r, c
        

if __name__ == '__main__':
    # courses = [Course(name='Programming In C', code='CM2101'), Course(name='Linux Basics', code='CM2103')]
    # faculty = [Instructor(name='Someone')]
    # faculty[0].courses.append(courses[1])
    
    # co = Department(number=6, name='Computer Engineering', courses=courses, faculty=faculty)
    # ce = Department(number=2, name='Civil Engineering', courses=courses, faculty=faculty)
    
    # print(co.id)
    tt = TimeTable()
    tt[1, 1] = 2
    print(tt)
