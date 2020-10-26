from session import Session

class Instructor:
    max_sess_cnt = 3
    instructors = []
    ordered_times = ['10 am','11 am','12 pm','4 pm','3 pm','4 pm','5 pm','6 pm']
    ordered_days = ['1', '2', '3', '4', '6']
    day_dict = {'0':'Sunday', '1':'Monday', '2':'Tuesday', '3': 'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday'}

    def __init__(self, data):
        self.my_data = data
        self.email = data[1]
        self.cell = data[2]
        self.first_name = data[3].strip()
        self.last_name = data[4].strip()
        self.locations = data[31]
        self.max_wk_hrs = data[30]  # assigned by director
        self.mon_avail = data[7]
        self.tue_avail = data[8]
        self.wed_avail = data[9]
        self.thu_avail = data[10]
        self.sat_avail = data[11]
        self.rank = data[32]  # assinged by director 29 => old rank, 32 = rank assigned 10/13/2020
        self.sessions = []
        self.day_time_tuples = [] # used to eliminate scheduling for more than one location at a time
        self.sess_cnt = {}
        self.duplex_sessions = [] # used to permit center instructors to support on-line sessions

    def __lt__(self, other):
        # return int(self.max_wk_hrs) < int(other.max_wk_hrs) # sort by max availability
        return int(self.rank) < int(other.rank)  # sort by max rank

    def add_duplex_session(self, session, student_count): # todo need to ensure sess_cnt update for both sessions
        self.sessions.append(session)
        self.sess_cnt[session] = student_count
        self.duplex_sessions.append(session)

    def add_session(self, session, student_count = 0):
        self.day_time_tuples.append(session.day_time_tuple)
        self.sessions.append(session)
        self.sess_cnt[session] = 0

    def can_work_location(self, location_string):
        return location_string in self.locations

    def can_work_session(self, session):
        if self.can_work_location(session.location) and self.hours_scheduled() < int(self.max_wk_hrs) \
                and not session.day == '0' and not self.day_time_tuples.__contains__(session.day_time_tuple):
            if (session.day == '1') and (session.time in self.mon_avail):
                return True
            elif (session.day == '2') and (session.time in self.tue_avail):
                return True
            elif (session.day == '3') and (session.time in self.wed_avail):
                return True
            elif (session.day == '4') and (session.time in self.thu_avail):
                return True
            elif (session.day == '6') and (session.time in self.sat_avail):
                return True
        return False

    def can_work_session_with_additional_hours(self, session):
        if self.can_work_location(session.location) and not session.day == '0' \
                and not self.day_time_tuples.__contains__(session.day_time_tuple):
            if (session.day == '1') and (session.time in self.mon_avail):
                return True
            elif (session.day == '2') and (session.time in self.tue_avail):
                return True
            elif (session.day == '3') and (session.time in self.wed_avail):
                return True
            elif (session.day == '4') and (session.time in self.thu_avail):
                return True
            elif (session.day == '6') and (session.time in self.sat_avail):
                return True
        return False

    def can_work_session_with_excess_capacity(self, session):
        return (self.can_work_location(session.location) \
                and self.day_time_tuples.__contains__(session.day_time_tuple) \
                and not self(session).fully_utilized())

    def create_instructors(self, client, SHEET_WORK_AVAIL_NAME, INSTRUCTOR_SHEET_NAME):
        instructor_sheet = client.open(SHEET_WORK_AVAIL_NAME)
        instructor_wks = instructor_sheet.worksheet_by_title(INSTRUCTOR_SHEET_NAME)
        for i in instructor_wks:
            self.instructors.append(Instructor(i))
        self.instructors.pop(0)  # remove 'instructor' created from the header row
        self.instructors = sorted(self.instructors)
        return self.instructors

    def extra_capacity_session_instructor_tuples(self, sessions):
        tuple_dict = {}
        for s in sessions:
            for i in s.instructors:
                if i.student_capacity(s) > 0:
                    if (s.day,s.time) in tuple_dict:
                        temp = tuple_dict[s.day,s.time]
                        temp.append([s,i])
                        tuple_dict[s.day,s.time] = temp
                    else:
                        tuple_dict[s.day,s.time] = [[s,i]]
        return tuple_dict

    def print_extra_capacity_instructors(self, sessions):
        extra_capacity_instructors = []
        for s in sessions:
            for i in s.instructors:
                if i.student_capacity(s) > 0:
                    extra_capacity_instructors.append(i)
                    print(s.day, s.location, s.time, i.first_name, i.student_capacity(s))
        return extra_capacity_instructors

    def fully_utilized(self, session):
        return self.sess_cnt[session] == Instructor.max_sess_cnt

    def student_capacity(self, session):
        return self.max_sess_cnt - self.sess_cnt[session]

    def hours_scheduled(self):
        return len(self.sessions)

    def print(self):
        print(self.first_name, self.last_name, 'Hours Scheduled: ', self.hours_scheduled(), 'Sessions: ',
              len(self.sessions))

    def print_session_count(self):
        if len(self.sessions) == 0:
            print(self.first_name, self.last_name, 'assigned 0 sessions.')
        else:
            print(self.first_name, self.last_name, 'assigned', self.hours_scheduled(), 'sessions:')

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def print_session_count(self):
        suffix = str(len(self.sessions)) + ' Sessions'
        print(self.first_name + ' ' + self.last_name, ' ', suffix)

    def remove_session(self, session): # todo may be more to it for removal
            self.day_time_tuples.remove(session.day_time_tuple)
            self.sessions.remove(session)

    def sess_loc_for_day(self, day):
        result = ''
        for s in self.sessions:
            if s.day == day:
                for t in self.ordered_times:
                    if s.time == t:
                            result = result + s.location + t + ','
                else:
                    result = result + ','
        return result

    def print_schedule(self):
        print(self.full_name())
        printed_days = []
        current_day = 0
        for s in self.sessions:
            if not s.day in printed_days:
                print ('    ' + Session.day_dict[s.day])
                printed_days.append(s.day)
                current_day = s.day
            else:
                if s.day != current_day:
                    print('        ' + s.time,s.location, end = ' ')
                else:
                    print('        ' + s.time,s.location)
                    current_day = s.day
        return

    def print_sessions(self):
        for s in self.sessions:
            print(self.full_name() + ',' + self.day_dict[s.day] +',' + s.time + ',' + s.location)
        return

    def session_records(self):
        records = []
        for s in self.sessions:
            records.append(s.session_record())
        for r in records:
            r.insert(0,self.full_name())
        return records

    def session_record_header(self):
        return ['Full Name', 'Day', 'Time', 'Location']

    def write_sessions(self, instructors, client, SHEET_OUTPUT_NAME, WKS_OUTPUT_NAME):
        sh = client.open(SHEET_OUTPUT_NAME)
        wks = sh.worksheet_by_title(WKS_OUTPUT_NAME)
        wks.update_row(1, self.session_record_header(self))
        row = 1
        for i in instructors:
            for sr in i.session_records():
                row = row + 1
                wks.update_row(row, sr)
        # print('Worksheet rows:' + str(output_wks.rows))
        # print('Worksheet columns:' + str(output_wks.cols))
        # print('A1 Value before update:' + output_wks.get_value('A1'))
        # output_wks.update_value('A1', 'Updated Value')
        # print('A1 Value after update:' + output_wks.get_value('A1'))
        # print('Value of cell (1,1):' + output_wks.cell((1, 1)).value)
        return







