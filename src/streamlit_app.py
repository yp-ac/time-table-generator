from dis import dis
from components import display_list_with_input_options
import hydralit as hy
from typing import List
from utils import *
from components import *

if 'COURSES' not in hy.session_state:
    hy.session_state['COURSES'] =  {"CM2101": Course(name='Programming In C', code='CM2101'), "CM2103": Course(name='Linux Basics', code='CM2103')}

if 'DEPARTMENTS' not in hy.session_state:
    hy.session_state['DEPARTMENTS'] = []

if 'INSTRUCTORS' not in hy.session_state:
    hy.session_state['INSTRUCTORS'] = [Instructor(name='Suhas', courses=list(hy.session_state.COURSES.values()))]

INSTRUCTORS = hy.session_state.INSTRUCTORS
COURSES = hy.session_state.COURSES
DEPARTMENTS = hy.session_state.DEPARTMENTS

app = hy.HydraApp(title='Time Table Generator', favicon=":chart:", use_navbar=True, navbar_sticky=True)

@app.addapp(title="HOME", is_home=True)
def home():
    hy.write('Hello from app 1')

###### DEPARTMENTS PAGE ######
@app.addapp(title="Department")
def departments_page():
    def print_dept(dept: Department):
        def course_processor(out):
            if c := COURSES.get(out[0], None):
                dept.courses.append(c)
            else:
                hy.warning(f"{out[0]} does not exist!")

        with hy.expander(f"[{dept.number}] {dept.name}"):
            hy.write("Sections: ")

            display_list_with_input_options(
                dept.sections, 
                ['Section'],
                lambda out: dept.sections.append(out[0]),
                lambda x: hy.info(x),
                key=f"{dept.id}sp"
            )

            hy.write("Courses: ")

            display_list_with_input_options(
                dept.courses, 
                ['Course Code'],
                course_processor,
                lambda x: hy.info(f"[{x.code}] {x.name}"),
                key=f"{dept.id}cp"
            )

    display_list_with_input_options(
        DEPARTMENTS,
        ['Dept Name'],
        lambda out: DEPARTMENTS.append(Department(number=len(DEPARTMENTS), name=out[0])),
        print_dept,
        key='dp'
    )


###### Teachers PAGE ######
@app.addapp(title="Teachers")
def teachers():
    def teacher_to_str(teacher: Instructor):
        def teach_processor(out):
            if c := COURSES.get(out[0], None):
                teacher.courses.append(c)
            else:
                hy.warning(f"{out[0]} does not exist!")

        with hy.expander(teacher.name):
            hy.write("Courses: ")

            display_list_with_input_options(
                teacher.courses, 
                ["Course Code"],
                teach_processor, 
                lambda x: hy.info(f"[{x.code}] {x.name}"),
                key=teacher.id
            )

    display_list_with_input_options(
        INSTRUCTORS,
        ["Instructor Name"], 
        lambda out: INSTRUCTORS.append(Instructor(name=out[0])), 
        teacher_to_str, 
        key='ip'
    )

###### Courses PAGE ######
@app.addapp(title='Courses')
def courses_page():
    def processor(out):
        COURSES[out[0]] = Course(code=out[0], name=out[1], hours=int(out[2].strip()))

    def course_to_string(course: Course):
        return hy.info(f"[{course.code}] {course.name}")

    display_list_with_input_options(COURSES.values(), ["Course Code", "Course Name", "num hours"], processor, course_to_string, key='cp')


if __name__ == '__main__':
    app.run()
