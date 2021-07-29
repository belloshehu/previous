from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton, MDRaisedButton
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.gridlayout import GridLayout
from kivy.metrics import dp
#from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.list import (
    TwoLineAvatarListItem, 
    IconLeftWidget, 
    ThreeLineAvatarListItem
)
import time
from datetime import datetime
from database import (
    create_tables, add_course, add_tutor, 
    add_lesson, get_courses, get_tutors,
    get_tutor, get_course, get_course_tutors,
    get_course_lessons, get_lesson, get_lessons,
    delete_tutor, update_tutor, update_lesson,
    delete_lesson, update_course, delete_course
)



Window.size = (300, 500)


class MainScreen(Screen):
    pass


class CourseScreen(Screen):
    pass


class AppRoot(ScreenManager):

    def back_to_main(self, instance):
        self.current = 'main'
        self.refresh_lessons_list()
        self.refresh_tutors_list()

    def refresh_lessons_list(self):
        ''' get lesson instances from database and add them to the scroll list '''
        # clear the parent widget
        self.ids.main_screen.ids.lessons_list.clear_widgets()
        lessons = get_lessons()
        for lesson in lessons:
            item = CustomThreeLineAvatarListItem( 
                item_id=lesson[0], 
                app=self.parent,
                model='lesson', 
                text=lesson[1], 
                secondary_text=lesson[2], 
                tertiary_text=lesson[3],
                course_id=lesson[4]
            )
            icon = IconLeftWidget(icon='book-open-blank-variant')
            item.add_widget(icon)
            self.ids.main_screen.ids.lessons_list.add_widget(item)


    def refresh_course_lessons_list(self, course_id):
        ''' get lesson instances from database and add them to the scroll list '''
        # clear the parent widget
        self.ids.course_screen.ids.course_lessons.clear_widgets()
        lessons = get_course_lessons(course_id)
        for lesson in lessons:
            item = CustomThreeLineAvatarListItem( 
                item_id=lesson[0], 
                app=self.parent,
                model='lesson', 
                text=lesson[1], 
                secondary_text=lesson[2], 
                tertiary_text=lesson[3],
                course_id=lesson[4]
            )
            icon = IconLeftWidget(icon='book-open-blank-variant')
            item.add_widget(icon)
            self.ids.course_screen.ids.course_lessons.add_widget(item)



    def refresh_tutors_list(self):
        ''' get tutor instances from database and add them the scrolling list '''
        # clear the parent widget
        self.ids.main_screen.ids.tutors_list.clear_widgets()
        tutors = get_tutors()
        for tutor in tutors:
            item = CustomTwoLineAvatarListItem(
                item_id=tutor[0],
                app=self.parent,
                model='tutor',
                text=tutor[1],
                secondary_text=tutor[2],
            )
            icon = IconLeftWidget(icon='book-account-outline')
            item.add_widget(icon)
            self.ids.main_screen.ids.tutors_list.add_widget(item)


    def refresh_course_tutors_list(self, course_id):
        ''' get tutor instances of a course from database and add them the scrolling list '''
        # clear the parent widget
        self.ids.course_screen.ids.course_tutors.clear_widgets()
        tutors = get_course_tutors(course_id)
        for tutor in tutors:
            item = CustomTwoLineAvatarListItem(
                item_id=tutor[0],
                app=self.parent,
                model='tutor',
                text=tutor[1],
                secondary_text=tutor[2],
            )
            icon = IconLeftWidget(icon='book-account-outline')
            item.add_widget(icon)
            self.ids.course_screen.ids.course_tutors.add_widget(item)


    def refresh_courses_list(self):
        ''' get courses instances from database and add them the scrolling list '''
        # clear the parent widget
        self.ids.main_screen.ids.courses_list.clear_widgets()
        courses = get_courses()
        for course in courses:
            item = CustomTwoLineAvatarListItem(
                item_id=course[0],
                app=self.parent,
                model='course',
                text=course[1],
                secondary_text=course[2],
            )
            icon = IconLeftWidget(icon='school')
            item.add_widget(icon)
            self.ids.main_screen.ids.courses_list.add_widget(item)


class LessonDialogContent(BoxLayout):
    orientation = 'vertical'
    def __init__(self, course_detail, **kwargs):
        super().__init__(**kwargs)
        self.course_detail = course_detail
    
    def open_datepicker(self):
        date_picker = MDDatePicker(
            callback=self.get_date,

        )
        date_picker.open()

    def get_date(self, date):
        self.ids.date.text = str(date)



class TutorDialogContent(BoxLayout):
    orientation = 'vertical'
    def __init__(self, course_detail, **kwargs):
        super().__init__(**kwargs)
        self.course_detail = course_detail


class CourseDialogContent(BoxLayout):
    orientation = 'vertical'
    

class EditDialogContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.primary_text = args[0]
        self.secondary_text = args[1]
        self.size_hint_y = None
        self.height = 100
        self.primary_text_field = MDTextField(
            text = self.primary_text,
        )
        self.secondary_text_field = MDTextField(
            text = self.secondary_text, 
        )
        self.add_widget(self.primary_text_field)
        self.add_widget(self.secondary_text_field)
        if len(args) > 2:
            self.tertiary_text = args[2]
            self.tertiary_text_field = MDTextField(
                text = self.tertiary_text, 
            )
            self.add_widget(self.tertiary_text_field)
        

kv = Builder.load_file('design.kv')


class CustomThreeLineAvatarListItem(ThreeLineAvatarListItem, HoverBehavior):
    start = 0
    stop = 0
    def __init__(self, item_id, model, app, course_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.app = app
        self.item_id = item_id
        self.course_id = course_id


    def on_enter(self, *args):
        self.md_bg_color = (1, 0, 1, 1)


    def on_leave(self, *args):
        self.md_bg_color = (1, 1, 1, 1)


    def on_release(self):
        print(self.text)
        self.stop = time.time()
        print(self.stop - self.start)
        if self.stop - self.start > 1:
            self.update_delete_dialog = MDDialog(
                title='DELETE/EDIT LESSON' if self.model=='lesson' else 'EDIT', 
                type='custom',
                content_cls=EditDialogContent(
                    self.text,
                    self.secondary_text,
                    self.tertiary_text
                ),
                buttons=[
                    MDFlatButton(text='Save', on_release=self.save_item),
                    MDRaisedButton(text='Delete', on_release=self.delete_item)
                ]
            )
            self.update_delete_dialog.open()


    def delete_item(self, instance):
        if self.model == 'lesson':
            delete_lesson(self.item_id)
            self.app.root.refresh_course_lessons_list(self.course_id)
            self.app.root.refresh_lessons_list()


    def save_item(self, instance):
        if self.model == 'lesson':
            update_lesson(
                self.update_delete_dialog.content_cls.primary_text_field.text,
                self.update_delete_dialog.content_cls.secondary_text_field.text,
                self.update_delete_dialog.content_cls.tertiary_text_field.text,
                self.item_id,
            )
            self.app.root.refresh_course_lessons_list(self.course_id)
            self.app.root.refresh_lessons_list()


class CustomTwoLineAvatarListItem(TwoLineAvatarListItem):
    start = 0
    stop = 0


    def __init__(self, item_id, model, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.app = app
        self.item_id = item_id


    def on_release(self):
        print(self.text)
        self.stop = time.time()
        print(self.stop - self.start)
        if self.stop - self.start > 1:
            title = ''
            if self.model == 'lesson':
                title = 'DELETE/EDIT LESSON'
            elif self.model == 'tutor':
                title = 'DELETE/EDIT TEACHER'
            else:
                title = 'DELETE/EDIT COURSE'
    
            self.update_delete_dialog = MDDialog(
                title=title,
                type='custom',
                content_cls=EditDialogContent(
                    self.text,
                    self.secondary_text,
                ),
                buttons=[
                    MDFlatButton(text='Save', on_release=self.save_item),
                    MDRaisedButton(text='delete', on_release=self.delete_item)
                ]
            )
            self.update_delete_dialog.open()
        elif self.model == 'course':
            self.app.root.current = 'course'
            self.app.root.course_screen.course_detail.text = self.text
            self.app.root.course_screen.course_detail.secondary_text = self.secondary_text
            self.app.root.course_screen.course_detail.course_id = self.item_id
            
            # get tutors for this course 
            tutors = get_course_tutors(self.item_id)
            print(self.item_id)
            # clear the lists:
            self.app.root.course_screen.ids.course_lessons.clear_widgets()
            self.app.root.course_screen.ids.course_tutors.clear_widgets()
            # append them to the list
            for tutor in tutors:
                self.add_course_children(
                    item_id=tutor[0], 
                    model='tutor', 
                    text=tutor[1], 
                    secondary_text=tutor[2]
                )
            # get lessons for the course 
            lessons = get_course_lessons(self.item_id)
            # append lessons to the list
            for lesson in lessons:
                item = CustomThreeLineAvatarListItem(
                    item_id=lesson[0],
                    app=self.app,
                    model='lesson',
                    text=lesson[1],
                    secondary_text=lesson[2],
                    tertiary_text=lesson[3],
                    course_id=self.item_id
                )
                icon = IconLeftWidget(icon='book-open-blank-variant')
                item.add_widget(icon)
                self.app.root.course_screen.ids.course_lessons.add_widget(item)

        else:
            pass

    def add_course_children(self, item_id, *args, **kwargs):
        """ Add tutors and lessons belonging to a course in their respective list."""
        item = CustomTwoLineAvatarListItem(
                item_id=item_id,
                app=self.app,
                model=kwargs['model'],
                text=kwargs['text'],
                secondary_text=kwargs['secondary_text'],
            )
        
        if kwargs['model'] == 'lesson':
            icon = IconLeftWidget(icon='book-open-blank-variant')
            item.add_widget(icon)
            self.app.root.course_screen.ids.course_lessons.add_widget(item)
        else:
            icon = IconLeftWidget(icon='book-account-outline')
            item.add_widget(icon)
            self.app.root.course_screen.ids.course_tutors.add_widget(item)


    def delete_item(self, instance):
        if self.model == 'tutor':
            delete_tutor(self.item_id)
            # refresh the list
            self.app.root.refresh_tutors_list()
            self.app.root.refresh_course_tutors_list(self.course_id)
        elif self.model == 'course':
            delete_course(self.item_id)
            self.app.root.refresh_courses_list()
    

    def save_item(self, instance):
        if self.model == 'tutor':
            update_tutor(
                self.update_delete_dialog.content_cls.primary_text_field.text,
                self.update_delete_dialog.content_cls.secondary_text_field.text,
                self.item_id,
            )
            # refresh the list
            self.app.root.refresh_tutors_list()
            self.app.root.refresh_course_tutors_list(self.course_id)
        elif self.model == 'course':
            update_course(
                self.update_delete_dialog.content_cls.primary_text_field.text,
                self.update_delete_dialog.content_cls.secondary_text_field.text,
                self.item_id
            )
            self.app.root.refresh_courses_list()
    

    def on_press(self):
        self.start = time.time()


    def on_touch_down(self, *args, **kwargs):
        super().on_touch_down(*args, **kwargs)
    
class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Red'
        self.text_color = 'White'
        return AppRoot()


    def on_start(self):
        self.lesson_dialog = None
        create_tables()
        courses = get_courses()
        for course in courses:
            self.add_item(item_id=course[0], model='course', text=course[1], secondary_text=course[2])

        tutors = get_tutors()
        for tutor in tutors:
            self.add_item(item_id=tutor[0], model='tutors', text=tutor[1], secondary_text=tutor[2]) 
            item = CustomTwoLineAvatarListItem(
                item_id=tutor[0],
                app=self,
                model='tutor',
                text=tutor[1],
                secondary_text=tutor[2],
            )
            icon = IconLeftWidget(icon='book-account-outline')
            item.add_widget(icon)
            self.root.main_screen.ids.tutors_list.add_widget(item)

        lessons = get_lessons()
        for lesson in lessons:
            item = CustomThreeLineAvatarListItem( 
                item_id=lesson[0], 
                app=self,
                model='lesson', 
                text=lesson[1], 
                secondary_text=lesson[2], 
                tertiary_text=lesson[3],
                course_id=lesson[4]
            )
            icon = IconLeftWidget(icon='book-open-blank-variant')
            item.add_widget(icon)
            self.root.main_screen.ids.lessons_list.add_widget(item)


    def add_item(self, item_id, *args, **kwargs):
        item = CustomTwoLineAvatarListItem(
                item_id=item_id,
                app=self,
                model=kwargs['model'],
                text=kwargs['text'],
                secondary_text=kwargs['secondary_text'],
            )
        
        if kwargs['model'] == 'course':
            icon = IconLeftWidget(icon='school')
            item.add_widget(icon)
            self.root.main_screen.ids.courses_list.add_widget(item)
        else:
            icon = IconLeftWidget(icon='book-open-blank-variant')
            item.add_widget(icon)
            self.root.course_screen.ids.course_tutors.add_widget(item)
            

    def submit_lessons_form(self, instance):
        # ger all reference: name, description
        name = self.lesson_dialog.content_cls.ids.name
        description = self.lesson_dialog.content_cls.ids.description
        date = self.lesson_dialog.content_cls.ids.date
        course_detail = self.root.course_screen.ids.course_detail
        if name.text != '' and description.text != '':
            # save in the database
            add_lesson(name.text, description.text, date.text, course_detail)
            # get the saved lesson from database
            lesson = get_lesson(name.text, description.text, course_detail)
            if lesson is not None:
                item = CustomThreeLineAvatarListItem(
                    item_id=lesson[0],
                    app=self,
                    model='lesson',
                    text=lesson[1],
                    secondary_text=lesson[2],
                    tertiary_text=lesson[3],
                    course_id=course_detail.course_id
                )
                icon = IconLeftWidget(icon='book-open-blank-variant')
                item.add_widget(icon)
                # append it to the lessons under its course
                self.root.course_screen.ids.course_lessons.add_widget(item)
                # append it to the lessons's list
                #self.root.main_screen.ids.lessons_list.add_widget(item)
                # clear the name and description textinputs
                name.text = ''
                description.text = ''


    def submit_tutors_form(self, instance):
        # get all references
        contact = self.tutor_dialog.content_cls.ids.contact
        full_name = self.tutor_dialog.content_cls.ids.full_name
        course_detail = self.root.course_screen.ids.course_detail
        if contact.text !='' and full_name.text !='':
            # save in the database table
            add_tutor(full_name.text, contact.text, course_detail)
            tutor = get_tutor(full_name.text, contact.text, course_detail)
             # add the tutor instance to the list 
            self.add_item(item_id=tutor[0], model='tutor', text=tutor[1], secondary_text=tutor[2])
            #clears the input widgets
            contact.text = ''
            full_name.text = ''

    
    def submit_courses_form(self, instance):
        # get all references
        title = self.course_dialog.content_cls.ids.title
        name = self.course_dialog.content_cls.ids.name
        if title.text != '' and name.text != '':
            add_course(title.text, name.text)
            course = get_course(title.text, name.text)
            self.add_item(item_id=course[0] ,model='course', text=course[1], secondary_text=course[2])
            # clear the input widgets
            title.text = ''
            name.text = ''

    def add_tutor(self, course_detail):
        self.tutor_dialog  = MDDialog(
            title='Add teacher/lecturer', 
            type='custom', 
            content_cls=TutorDialogContent(course_detail),
            buttons=[
                MDFlatButton(
                    text='SUBMIT',
                    on_release=self.submit_tutors_form
                ),
                MDRaisedButton(
                    text='CANCEL', 
                    on_release=self.close_tutor_dialog
                )
            ]
        )
        self.tutor_dialog.open()


    def add_lesson(self, course_detail):
        self.lesson_dialog  = MDDialog(
            title='Add lesson/topic', 
            type='custom', 
            content_cls=LessonDialogContent(course_detail),
            buttons=[
                MDFlatButton(
                    text='SUBMIT',
                    on_release=self.submit_lessons_form
                ),
                MDRaisedButton(
                    text='CANCEL', 
                    on_release=self.close_lesson_dialog
                )
            ]
        )
        self.lesson_dialog.open()


    def add_course(self):
        self.course_dialog  = MDDialog(
            title='Add course/subject', 
            type='custom', 
            content_cls=CourseDialogContent(),
            buttons=[
                MDFlatButton(
                    text='SUBMIT',
                    on_release=self.submit_courses_form,
                    text_color=self.theme_cls.primary_color
                ),
                MDRaisedButton(
                    text='CANCEL', 
                    on_release=self.close_course_dialog,
                    
                )
            ]
        )

        self.course_dialog.open()

    def close_tutor_dialog(self, instance):
        self.tutor_dialog.dismiss()
    

    def close_course_dialog(self, instance):
        self.course_dialog.dismiss()
    

    def close_lesson_dialog(self, instance):
        self.lesson_dialog.dismiss()
    

MyApp().run()
