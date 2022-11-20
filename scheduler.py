import pygsheets
from instructor import Instructor
# from duplexinstructor import DuplexInstructor
from session import Session
# from reducer import Reducer

SHEET_WORK_AVAIL_NAME = 'Mathnasium Work Availability Form (Responses)' #'Test Case Work Availability'
INSTRUCTOR_SHEET_NAME = 'Form Responses 1' # 'TC Form Responses 1'
SHEET_MASTER_NAME = 'Master Student Schedule (Version 6).20200910' # 'Test Case Master Schedule'
# WKS_EXPECTED_STUDENTS_NAME = 'TC Expected Students' # 'Expected Students'
WKS_ACTUAL_STUDENTS_NAME = 'Actual Students' #'TC Actual Students'
ACT_STUDENT_COL_NUM = 113 # the column number (0, 1, 2, 3 ...) containing the projected student count of each session

SHEET_INSTRUCTOR_SCHEDULE_NAME = 'Schedule'
WKS_SCHEDULE_NAME = 'Instructor Schedule'

SECRET_FILE = 'C:\PythonPrograms\SchedulerGSheets\Working Directory\credentials.json'


def main():
    client = pygsheets.authorize(client_secret=SECRET_FILE)
    # create instructors
    instructors = Instructor.create_instructors(Instructor, client, SHEET_WORK_AVAIL_NAME, INSTRUCTOR_SHEET_NAME)
    # instructors = DuplexInstructor.create_instructors(DuplexInstructor, client, SHEET_WORK_AVAIL_NAME,
    #                                                                    INSTRUCTOR_SHEET_NAME)
    # create required my_sessions
    sessions = Session.create_sessions(Session, client, SHEET_MASTER_NAME, WKS_ACTUAL_STUDENTS_NAME,ACT_STUDENT_COL_NUM)

    chancellor_sessions = []
    stafford_sessions = []
    home_sessions = []
    for s in sessions:
            if s.location == 'Chancellor':
                chancellor_sessions.append(s)
            elif s.location == 'Stafford':
                stafford_sessions.append(s)
            elif s.location == 'Home':
                home_sessions.append(s)

    # Find in-center my_sessions

    # Pass 1. Assign instructors to serve at center locations
    Instructor.max_student_capacity = Instructor.max_inCenter_student_capacity
    for l in [chancellor_sessions, stafford_sessions]:
        for s in l:
            for i in instructors:
                if not s.fully_staffed() and i.can_work_session(s):
                    i.add_session(s)
                    s.add_instructor(i)

    # Pass 3. Schedule the remaining home sessions
    for s in home_sessions:
        for i in instructors:
            if not s.fully_staffed() and i.can_work_session(s):
                i.add_session(s)
                s.add_instructor(i)

    # Pass 2. Assign instructors to serve at home
    Instructor.max_student_capacity = Instructor.max_atHome_student_capacity
    for s in home_sessions:
        for i in instructors:
            if not s.fully_staffed() and i.can_work_duplex_session(s):
                i.add_duplex_session(s)
                s.add_duplex_instructor(i)

#    # Pass 3. Schedule the remaining home sessions
#    for s in home_sessions:
#        for i in instructors:
#            if not s.fully_staffed() and i.can_work_session(s):
#                i.add_session(s)
#                s.add_instructor(i)

    if True:
        print('\nSessions Staffing Report\n')
        fully_staffed = []
        not_fully_staffed = []
        for s in sessions:
            if s.fully_staffed():
                fully_staffed.append(s)
            else:
                not_fully_staffed.append(s)
        print('--->Total Sessions:', len(sessions))
        print('------>Fully Staffed:', len(fully_staffed))
        print('------>Not Fully Staffed:', len(not_fully_staffed))
        for s in not_fully_staffed:
            s.print_pretty()

    if False:
        print('\nStaffing Efficiency Report\n')
        session_count = len(sessions)
        student_count = 0
        instructor_hours_count = 0
        for s in sessions:
            student_count = student_count + s.students_to_serve
        for i in instructors:
            instructor_hours_count = i.hours_scheduled() + instructor_hours_count
        students_per_instructor = student_count / instructor_hours_count

        print('Chancellor:', len(chancellor_sessions), 'Stafford:', len(stafford_sessions), 'Home:', len(home_sessions))
        print('Sessions provided:', session_count)
        print('Students served:', student_count)
        print("Instructor hours needed:", round(student_count / Instructor.max_student_capacity))
        print('Instructor hours used:', instructor_hours_count)
        print('Ratio:', students_per_instructor)
        print('Waste: $', round((3 - students_per_instructor) * instructor_hours_count * 15))

    if False: #Print Instructor Schedules
        print('\nInstructor Schedules\n')
        for i in instructors:
            i.print_schedule()
            print()

    if True:
        print('\nStudents Expected Each Session\n')
        for s in sessions:
            s.print_comma_delimited()

    if True: # Print Instructor Session Count
        print('\nInstructor Session Counts\n')
        for i in instructors:
            i.print_session_count_comma_delimited()

    if False:
        print('\nExtra Capacity Instructors\n')
        Instructor.print_extra_capacity_instructors(Instructor, sessions)

    if False:
        print('\nMaster Schedule\n')
        Session.print_master_schedule(Session)

    if True: # print comma delimited my_sessions, by instructor, to transcript
        print('\nInstructor Schedule\n')
        for i in instructors:
            i.print_sessions()

    if False:
        print('\nWriting Instructor Schedules to Google Spreadsheet\n')
        Instructor.write_sessions(Instructor, instructors, client, SHEET_INSTRUCTOR_SCHEDULE_NAME, WKS_SCHEDULE_NAME)

if __name__ == '__main__':
    main()
