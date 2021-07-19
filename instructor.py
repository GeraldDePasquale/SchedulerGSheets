from session import Session

class Instructor:
    instructors = []
    ordered_times = ['10 am','11 am','12 pm','4 pm','3 pm','4 pm','5 pm','6 pm']
    ordered_days = ['1', '2', '3', '4', '6']
    day_dict = {'0':'Sunday', '1':'Monday', '2':'Tuesday', '3': 'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday'}
    max_student_capacity = 3

    def __init__(self, data):
        self.max_student_capacity = Instructor.max_student_capacity
        self.my_data = data
        self.email = data[1]
        self.cell = data[2]
        self.first_name = data[3].strip()
        self.last_name = data[4].strip()
        self.locations = data[31]
        self.max_wk_hrs = int(data[30])  # assigned by director
        self.my_monday_hours = data[7]
        self.my_tuesday_hours = data[8]
        self.my_wednesday_hours = data[9]
        self.my_thursday_hours = data[10]
        self.my_saturday_hours = data[11]
        self.rank = data[32]  # assinged by director 29 => old rank, 32 = rank assigned 10/13/2020
        self.my_sessions = []
        self.day_time_tuples = [] # used to eliminate scheduling for more than one location at a time
        self.student_count_session = {}
        self.student_count_day_time = {}
        self.my_duplex_sessions = [] # used to permit center instructors to support on-line my_sessions

    def __lt__(self, other):
        # return int(self.max_wk_hrs) < int(other.max_wk_hrs) # sort by max availability
        return int(self.rank) < int(other.rank)  # sort by max rank

    def add_session(self, session, student_count = 0):
        self.day_time_tuples.append(session.day_time_tuple)
        self.my_sessions.append(session)
        self.student_count_session[session] = 0
        self.student_count_day_time[session.day_time_tuple] = 0

    def add_duplex_session(self, session, student_count = 0):
        # self.day_time_tuples.append(session.day_time_tuple)
        self.my_sessions.append(session)
        self.my_duplex_sessions.append(session)
        self.student_count_session[session] = 0
        #self.student_count_day_time[session.day_time_tuple] = 0

    def can_work_location(self, location_string):
        return location_string in self.locations

    def can_work_session(self, session):
        if self.can_work_location(session.location) and self.hours_scheduled() < self.max_wk_hrs \
                and not self.day_time_tuples.__contains__(session.day_time_tuple):
            if (session.day == '1') and (session.time in self.my_monday_hours):
                return True
            elif (session.day == '2') and (session.time in self.my_tuesday_hours):
                return True
            elif (session.day == '3') and (session.time in self.my_wednesday_hours):
                return True
            elif (session.day == '4') and (session.time in self.my_thursday_hours):
                return True
            elif (session.day == '6') and (session.time in self.my_saturday_hours):
                return True
        return False

    def can_work_duplex_session(self, session): # pass center session and home session, student_count_session = count for both sessions.
        # duplex session
        if self.day_time_tuples.__contains__(session.day_time_tuple) and self.student_count_day_time[session.day_time_tuple] < self.max_student_capacity: #touched
            #print('student_count_day_time is: '+str(self.student_count_day_time[session.day_time_tuple])+' max_student_capacity is: '+str(self.max_student_capacity))
            return True
        return False

    def create_instructors(self, client, SHEET_WORK_AVAIL_NAME, INSTRUCTOR_SHEET_NAME):
        instructor_sheet = client.open(SHEET_WORK_AVAIL_NAME)
        instructor_wks = instructor_sheet.worksheet_by_title(INSTRUCTOR_SHEET_NAME)
        header = True
        for i in instructor_wks:
            if not header:
                self.instructors.append(Instructor(i))
            else:
                header = False
        self.instructors = sorted(self.instructors)
        return self.instructors

    def extra_capacity_session_instructor_tuples(self, sessions):
        tuple_dict = {}
        for s in sessions:
            for i in s.instructors:
                if i.remaining_student_capacity(s) > 0:
                    if (s.day,s.time) in tuple_dict:
                        temp = tuple_dict[s.day,s.time]
                        temp.append([s,i])
                        tuple_dict[s.day,s.time] = temp
                    else:
                        tuple_dict[s.day,s.time] = [[s,i]]
        return tuple_dict

    def extra_capacity_instructors(self, sessions):
        extra_capacity_instructors = []
        for s in sessions:
            for i in s.instructors:
                if i.remaining_student_capacity(s) > 0:
                    extra_capacity_instructors.append(i)
        return extra_capacity_instructors

    def print_extra_capacity_instructors(self, sessions):
        extra_capacity_instructors = []
        for s in sessions:
            for i in s.my_instructors:
                if i.remaining_student_capacity(s) > 0:
                    extra_capacity_instructors.append(i)
                    print(s.day, s.location, s.time, i.first_name, i.remaining_student_capacity(s))
        return extra_capacity_instructors

    def fully_utilized(self, session):
        return self.student_count_day_time[session.day_time_tuple] == self.max_student_capacity #touched

    def remaining_student_capacity(self, session):
        return self.max_student_capacity - self.student_count_day_time[session.day_time_tuple] #touched

    def hours_scheduled(self):
        return len(self.my_sessions) - len(self.my_duplex_sessions)

    def print(self):
        print(self.full_name(), 'Hours Scheduled: ', self.hours_scheduled(), 'Sessions: ',
              len(self.my_sessions))

    def print_session_count(self):
        if len(self.my_sessions) == 0:
            print(self.full_name(), 'assigned 0')
        else:
            print(self.full_name(), 'assigned', self.hours_scheduled())

    def print_session_count_comma_delimited(self):
        if len(self.my_sessions) == 0:
            print(self.full_name() + ',' + '0')
        else:
            print(self.full_name() + ',' + str(self.hours_scheduled()))

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def remove_session(self, session): # todo may be more to it for removal
            self.day_time_tuples.remove(session.day_time_tuple)
            self.my_sessions.remove(session)

    def sess_loc_for_day(self, day):
        result = ''
        for s in self.my_sessions:
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
        for s in self.my_sessions:
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

    def has_duplex_session(self, s):
        for ds in self.my_duplex_sessions:
            if s.day_time_tuple == ds.day_time_tuple:
                return True
        return False

    def get_duplex_session(self, s):
        for ds in self.my_duplex_sessions:
            if s.day_time_tuple == ds.day_time_tuple: return ds
        return None

    def print_sessions(self):
        for s in self.my_sessions:
            if self.has_duplex_session(s):
                ds = self.get_duplex_session(s)
                if not ds.location == s.location:
                    print(self.full_name() + ',' + s.day +',' + s.time + ',' + s.location +
                        ',' + str(self.student_count_session[s]) + '@' + s.location + ':' +
                        str(self.student_count_session[ds]) + '@' + ds.location)
            else:
                print(self.full_name() + ',' + s.day + ',' + s.time + ',' + s.location +
                      ',' + str(self.student_count_session[s])+'@' + s.location)
        return

    def session_records(self):
        records = []
        for s in self.my_sessions:
            if self.has_duplex_session(s):
                ds = self.get_duplex_session(s)
                if not ds.location == s.location:
                    records.append([self.full_name(),s.day,s.time,s.location, str(self.student_count_session[s]) +
                                    '@' + s.location + ':' + str(self.student_count_session[ds]) + '@' + ds.location])
            else:
                records.append([self.full_name(),s.day,s.time,s.location, str(self.student_count_session[s]) +
                                '@' + s.location])
        return records

    def session_record_header(self):
        return ['Full Name', 'Day', 'Time', 'Location', 'Serving']

    def write_sessions(self, instructors, client, SHEET_OUTPUT_NAME, WKS_OUTPUT_NAME):
        sh = client.open(SHEET_OUTPUT_NAME)
        wks = sh.worksheet_by_title(WKS_OUTPUT_NAME)
        wks.update_row(1, self.session_record_header(self))
        row = 1
        for i in instructors:
            for sr in i.session_records():
                row = row + 1
                wks.update_row(row, sr)
        return







