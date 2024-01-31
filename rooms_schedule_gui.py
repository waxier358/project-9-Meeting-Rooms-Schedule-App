import tkinter
from tkcalendar import Calendar
from tkinter import PhotoImage, Label, Frame, Button, DISABLED, NORMAL
from datetime import date, datetime

from check_fields import CheckFields
from db import Database, RoomsNamePictures
from login_error_gui import NewScheduleGui, TimeSchedulePassedGui, EmailSendErrorGui
from send_email import prep_and_send_email_schedule_information
from email_send_exception import EmailSendException


class RoomsSchedule(tkinter.Tk):
    """ A class for creating and controlling a room schedule window.

    This class is responsible for initializing and managing a user interface window that facilitates the scheduling
    and overseeing of room bookings."""
    def __init__(self, main_window: tkinter, username: str):
        super().__init__()

        self.main_window = main_window
        self.check_fields = CheckFields(self)
        self.db = Database()
        self.rooms_name_and_pictures = RoomsNamePictures()

        self.username = username
        self.current_user_email_address = None
        self.interval = None
        self.initial_room_name = None
        self.initial_image_file_name = ""
        self.next_picture = None
        self.prev_picture = None
        self.check_time_interval = None

        self.title('Meeting Rooms Schedule App - Rooms Schedule')
        self.resizable(False, False)
        self.geometry('1020x660')
        self.iconbitmap('icon/meeting.ico')
        self.focus()

        # create background
        self.background_label = Label(self, height=1020, width=660, bg='white')
        self.background_label.place(x=0, y=0)

        # create a frame
        Frame(self, width=1020, height=2, bg='black').place(x=0, y=0)

        # create username label
        self.username_label = Label(self, text=f'username: {self.username}', border=False, fg='#529ffc',
                                    font=('TimesNewRoman', 12, 'bold'), background='white')
        self.username_label.place(x=10, y=10)

        # create user title label
        self.title_label = Label(self, text='Schedule rooms', border=False, fg='#529ffc',
                                 font=('TimesNewRoman', 23, 'bold'), background='white')
        self.title_label.place(x=400, y=50)

        # set initial room name and picture
        self.initialize_room_name_and_pictures()

        # create room name label
        self.room_name_label = Label(self, text=self.rooms_name_and_pictures.return_initial_room_name(), border=False,
                                     fg='#529ffc', font=('TimesNewRoman', 12, 'bold'), background='white')
        self.room_name_label.place(x=250, y=110)

        # create image label
        self.initial_image = PhotoImage(file=self.initial_image_file_name)
        self.image_label = Label(self, border=True, image=self.initial_image, borderwidth=1)
        self.image_label.place(x=100, y=140)

        # create a calendar
        self.calendar = Calendar(self, selectmode='day', year=date.today().year, month=date.today().month,
                                 day=date.today().day, date_pattern="dd.mm.yyyy", font=('TimesNewRoman', 16, 'bold'),
                                 showweeknumbers=False,
                                 showothermonthdays=False,
                                 background='#529ffc',
                                 cursor='hand2', borderwidth=5
                                 )
        self.calendar.place(x=550, y=140)
        self.calendar.bind("<<CalendarSelected>>", self.date_selected_from_calendar)

        # create room name backward button
        self.room_name_button_backward = Button(self, text=u'\u25C4', font=('TimesNewRoman', 8), cursor='hand2',
                                                command=self.show_prev_room_name)
        self.room_name_button_backward.place(x=75, y=110)

        # create room name forward button
        self.room_name_button_forward = Button(self, text=u'\u25BA', font=('TimesNewRoman', 8), cursor='hand2',
                                               command=self.show_next_room_name)
        self.room_name_button_forward.place(x=485, y=110)

        # create room image backward button
        self.room_image_button_backward = Button(self, text=u'\u25C4', font=('TimesNewRoman', 8), cursor='hand2',
                                                 command=self.show_prev_picture)
        self.room_image_button_backward.place(x=75, y=240)

        # create room image forward button
        self.room_image_button_forward = Button(self, text=u'\u25BA', font=('TimesNewRoman', 8), cursor='hand2',
                                                command=self.show_next_picture)
        self.room_image_button_forward.place(x=485, y=240)

        # create scheduler label
        self.schedule_title_label = Label(self, text=f'scheduler for {self.room_name_label.cget("text")} on date '
                                                     f'{self.calendar.get_date()} ',
                                          border=False, fg='#529ffc',
                                          font=('TimesNewRoman', 12, 'bold'), background='white')
        self.schedule_title_label.place(x=350, y=420)

        # create hours interval label
        self.hours_interval_label = Label(self, text=f'08:00 - 10:00   10:00 - 12:00   12:00 - 14:00   14:00 - 16:00   '
                                                     f'16:00 - 18:00   18:00 - 20:00   20:00 - 22:00',
                                          border=False, fg='#529ffc',
                                          font=('TimesNewRoman', 12, 'bold'), background='white')
        self.hours_interval_label.place(x=140, y=460)
        # create button 08
        self.button_08 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('08:00 - 10:00'))
        self.button_08.place(x=140, y=480)

        # create button 10
        self.button_10 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('10:00 - 12:00'))
        self.button_10.place(x=250, y=480)

        # create button 12
        self.button_12 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('12:00 - 14:00'))
        self.button_12.place(x=360, y=480)

        # create button 14
        self.button_14 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('14:00 - 16:00'))
        self.button_14.place(x=470, y=480)

        # create button 16
        self.button_16 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('16:00 - 18:00'))
        self.button_16.place(x=580, y=480)

        # create button 18
        self.button_18 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('18:00 - 20:00'))
        self.button_18.place(x=690, y=480)

        # create button 20
        self.button_20 = Button(self, text='', font=('TimesNewRoman', 8), cursor='hand2', width=14, height=2,
                                command=lambda: self.schedule_button_press('20:00 - 22:00'))
        self.button_20.place(x=800, y=480)

        self.update_schedule_gui(current_date=self.calendar.get_date())

    def show_next_room_name(self):
        """Retrieves the 'new_room_name' as a string from a CDLL, updates the GUI elements with this information.
        This function performs the following actions:
        1. Gets the 'new_room_name' from a CDLL and stores it as a string.
        2. Updates the 'room_name_label' in the GUI with the retrieved room name.
        3. Displays the picture associated with 'new_room_name'.
        4. Refreshes the GUI to show the updated picture corresponding to the new room name.
        """
        next_room_name = self.rooms_name_and_pictures.return_next_room_name(self.db)
        self.room_name_label.configure(text=next_room_name)
        self.show_next_picture()

        self.update_schedule_gui(current_date=self.calendar.get_date())

    def show_prev_room_name(self):
        """Retrieves the 'prev_room_name' as a string from a CDLL and updates the GUI with this information.
        Steps performed by this function include:
        1. Obtains the 'prev_room_name' from a CDLL, storing it as a string.
        2. Updates the 'room_name_label' in the GUI with the obtained previous room name.
        3. Displays the picture associated with 'prev_room_name'.
        4. Refreshes the GUI to show the updated picture for the previous room name.
        """
        prev_room_name = self.rooms_name_and_pictures.return_prev_room_name(self.db)
        self.room_name_label.configure(text=prev_room_name)
        self.show_prev_picture()

        self.update_schedule_gui(current_date=self.calendar.get_date())

    def show_next_picture(self):
        """Retrieves the next picture from the database and updates the image label in the GUI.

        This function performs the following actions:
        1. Fetches 'next_picture' from the database.
        2. Updates the 'image_label' in the GUI with the retrieved picture.
        """
        self.rooms_name_and_pictures.return_next_picture(self.db)
        self.next_picture = PhotoImage(file=self.initial_image_file_name)
        self.image_label.configure(image=self.next_picture)

    def show_prev_picture(self):
        """Retrieves the previous picture from the database and updates the image label in the GUI.
        This function executes the following steps:
        1. Fetches 'prev_picture' from the database.
        2. Updates the 'image_label' in the GUI with the fetched previous picture.
        """
        self.rooms_name_and_pictures.return_prev_picture(self.db)
        self.prev_picture = PhotoImage(file=self.initial_image_file_name)
        self.image_label.configure(image=self.prev_picture)

    def initialize_room_name_and_pictures(self):
        """Extracts room information from the database and initializes settings in a CDLL.
        This function performs the following actions:
        1. Extracts information about each room from the database, using namedtuple('Room', 'id room_name room_id').
        2. Creates a list, 'room_names', containing the names of the rooms based on the extracted namedtuple data.
        3. Inserts all the room names into a CDLL.
        4. Sets the initial room name ('initial_room_name') and initial image file name ('initial_image_file_name')
        in the CDLL environment.
        """
        # get all rooms_name from db
        all_rooms_name = [room.room_name for room in self.db.get_all_rooms_form_db()]
        self.rooms_name_and_pictures.insert_room_names(all_rooms_name, self.db)

        self.initial_room_name = self.rooms_name_and_pictures.return_initial_room_name()
        self.initial_image_file_name = 'images/current_image/current_picture.png'

    def date_selected_from_calendar(self, event):
        """ Updates the schedule GUI to display the date selected by the user from a calendar.
        This function performs the following action:
        1. Captures the date chosen by the user from the calendar interface.
        2. Updates the schedule GUI to display the selected date, showing relevant schedule information or events for
        that day."""
        current_date = self.calendar.get_date()
        self.update_schedule_gui(current_date=current_date)

    def update_schedule_gui(self, current_date: str):
        """Updates the schedule GUI based on the current date and manages orders associated with that date.
        Args:
            current_date (str): The date selected from the calendar, represented as a string.
        This function performs the following actions:
        1. Updates the 'schedule_title_label' with the current date.
        2. Retrieves all orders from the database associated with 'current_date'.
        3. Enables all schedule buttons in the GUI.
        4. Disables buttons associated with time intervals that have scheduled orders.
        5. Compares 'current_date' with today's date to set the 'self.check_time_interval' attribute.
        """
        # update schedule title
        self.schedule_title_label.configure(text=f'scheduler for {self.room_name_label.cget("text")} on date '
                                                 f'{self.calendar.get_date()} ')

        # get all record from database on current_date
        current_orders = self.db.get_schedule_for_current_date_and_room(room_name=self.room_name_label.cget('text'),
                                                                        current_date=current_date)
        self.enable_all_buttons()

        if current_orders:
            self.disable_all_scheduled_interval_buttons(current_orders=current_orders)

        self.is_current_date_today()

    def is_current_date_today(self):
        """Compares the current date with today's date to set the 'self.check_time_interval' attribute and manage
         button states.
        This function performs the following actions:
        1. Compares 'current_date' with today's date.
        2. Sets the 'self.check_time_interval' attribute based on the comparison result.
        3. If 'current_date' is earlier than today's date, disables all scheduling buttons to prevent room booking in
        the past.
        Note:
        This function is designed to ensure that room scheduling is only allowed for present or future dates.
        """
        today_date = datetime.today().date()
        calendar_date = datetime.strptime(self.calendar.get_date(), '%d.%m.%Y').date()

        self.check_time_interval = False
        if calendar_date < today_date:
            self.disable_all_buttons()
        elif calendar_date == today_date:
            self.check_time_interval = True

    def disable_all_scheduled_interval_buttons(self, current_orders):
        """Disables buttons associated with time intervals that are already scheduled on the specified current_day.
        Args:
            current_orders (list of namedtuples): A list of orders for the current date, each represented as a
            namedtuple('Order', 'order_by order_interval').
        This function iterates through the list of current orders and disables the buttons in the GUI that correspond
        to the time intervals of these orders. This action ensures that no double bookings occur for already scheduled
        time intervals on the current day.
        """
        for order in current_orders:
            if order.order_interval == "08:00 - 10:00":
                self.button_08.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')
            elif order.order_interval == "10:00 - 12:00":
                self.button_10.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')
            elif order.order_interval == "12:00 - 14:00":
                self.button_12.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')
            elif order.order_interval == "14:00 - 16:00":
                self.button_14.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')
            elif order.order_interval == "16:00 - 18:00":
                self.button_16.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')
            elif order.order_interval == "18:00 - 20:00":
                self.button_18.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')
            elif order.order_interval == "20:00 - 22:00":
                self.button_20.configure(text='Reserved', background='red', state=DISABLED, cursor='',
                                         disabledforeground='black')

    def enable_all_buttons(self):
        self.button_08.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')
        self.button_10.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')
        self.button_12.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')
        self.button_14.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')
        self.button_16.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')
        self.button_18.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')
        self.button_20.configure(text='Free', background='green', state=NORMAL, cursor='hand2',
                                 activebackground='green')

    def disable_all_buttons(self):
        self.button_08.configure(state=DISABLED, cursor='', disabledforeground='black')
        self.button_10.configure(state=DISABLED, cursor='', disabledforeground='black')
        self.button_12.configure(state=DISABLED, cursor='', disabledforeground='black')
        self.button_14.configure(state=DISABLED, cursor='', disabledforeground='black')
        self.button_16.configure(state=DISABLED, cursor='', disabledforeground='black')
        self.button_18.configure(state=DISABLED, cursor='', disabledforeground='black')
        self.button_20.configure(state=DISABLED, cursor='', disabledforeground='black')

    def schedule_button_press(self, interval: str):
        """Creates a schedule for a specified time interval.
        Args:
            interval (str): A string representing the time interval associated with a schedule button,
            for example 08:00.
        This function is responsible for setting up a schedule for the given time interval.
        """
        self.interval = interval

        if self.check_time_interval:
            self.current_date_is_today_date_handler()
        else:
            self.create_new_schedule_window()

    def current_date_is_today_date_handler(self):
        """Handles the scheduling process based on the comparison of the current date with today's date.
        This method initiates the scheduling process if the current date (self.current_date) is the same as today's
        date (self.today_date). If an attempt is made to schedule for a time interval that has already passed, an error
        message window is displayed to inform the user. Otherwise, the scheduling process continues as normal.
        Note:
            This method relies on class attributes like 'self.current_date' and 'self.today_date' to perform
            the comparison."""
        current_time = datetime.today().time()
        interval_time = datetime.strptime(self.interval[:5], '%H:%M').time()
        if current_time > interval_time:
            TimeSchedulePassedGui(self, 'Time for scheduling this interval passed!')
        else:
            self.create_new_schedule_window()

    def create_new_schedule_window(self):
        """Initiates a confirmation window GUI with a custom message based on the current user's email address.
        This method retrieves the email address associated with the 'current_user'. Using this email address,
        it constructs a message that is then displayed in a confirmation window GUI. This window is typically used to
        confirm scheduling actions or to provide additional information to the user related to their account or
        schedule.
        Note:
            The method assumes that the 'current_user' attribute is set and contains valid information for retrieving
            the email address."""
        self.current_user_email_address = self.db.get_user_by_username(self.username).email_address
        window_message = (f'You are going to schedule {self.room_name_label.cget("text")} for date '
                          f'{self.calendar.get_date()} \n on {self.interval}! \n Press OK to continue (check'
                          f' {self.current_user_email_address}) \nor \nCANCEL to return.')
        NewScheduleGui(self, window_message)

    def add_new_schedule_to_db(self):
        """Inserts new scheduling details into the database, updates the schedule GUI, and sends a notification email
         about the new schedule.
        This method performs the following actions:
        1. Inserts the new schedule information (including room_name, order_by, order_date, and order_interval) into
        the database.
        2. Updates the schedule GUI to reflect the newly added schedule information.
        3. Sends an email notification about the new schedule, providing details of the booking.
        Note:
            The method assumes that the necessary scheduling details are already set as class attributes or are
            accessible within the method.
        """
        room_name = self.room_name_label.cget('text')
        order_by = self.username
        order_date = self.calendar.get_date()
        order_interval = self.interval
        self.db.insert_new_schedule_in_db(room_name=room_name, order_by=order_by, order_date=order_date,
                                          order_interval=order_interval)
        self.update_schedule_gui(self.calendar.get_date())
        try:
            prep_and_send_email_schedule_information(destination_email_address=self.current_user_email_address,
                                                     room_name=room_name, order_date=order_date,
                                                     order_interval=order_interval)
        except EmailSendException:
            # create email send error window
            error_message = (f'An error occurred during send email process!\n'
                             f'Your schedule is registered and valid.\n'
                             f'See you sun!')
            EmailSendErrorGui(self, message=error_message)
