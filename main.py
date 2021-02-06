from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
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
    create_tables, 
    add_course, 
    add_tutor, 
    add_lesson
)



Window.size = (300, 500)

class AppRoot(BoxLayout):
    orientation = 'vertical'

class LessonDialog(BoxLayout):
    orientation = 'vertical'

class Content(BoxLayout):
    orientation = 'vertical'

class CourseDialog(BoxLayout):
    orientation = 'vertical'
    

class EditDialogContent(GridLayout):
 
    def __init__(self, primary_text, secondary_text, **kwargs):
        super().__init__(**kwargs)
        self.primary_text = primary_text
        self.secondary_text = secondary_text
        self.size_hint_y = None
        self.height = 100
        self.cols=1
        self.rows=2
        self.padding=(0,50,0,0)
        field_layout = BoxLayout(
            orientation='vertical'
        )
    
        primary_text_field = MDTextField(
            text = self.primary_text, 
        )
        secondary_text_field = MDTextField(
            text = self.secondary_text, 
        )
        field_layout.add_widget(primary_text_field)
        field_layout.add_widget(secondary_text_field)
        self.add_widget(field_layout)
        boxlayout = BoxLayout(
            spacing=20,
            padding=(0,20,0,0)
        )
        save_button = MDFillRoundFlatButton(text='Save')
        delete_button = MDFillRoundFlatButton(text='Delete')
        boxlayout.add_widget(save_button)
        boxlayout.add_widget(delete_button)
    

Builder.load_file('design.kv')

class CustomThreeLineAvatarListItem(ThreeLineAvatarListItem, HoverBehavior):
    start = 0
    stop = 0
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model


    def on_enter(self, *args):
        self.md_bg_color = (1, 0, 1, 1)

    def on_leave(self, *args):
        self.md_bg_color = (1, 1, 1, 1)

    def on_release(self):
        print(self.text)
        self.stop = time.time()
        print(self.stop - self.start)
        if self.stop - self.start > 1:
            MDDialog(
                title='Delete/Edit Lesson' if self.model=='lesson' else 'Edit', 
                type='custom',
                content_cls=EditDialogContent(
                    primary_text=self.text,
                    secondary_text=self.secondary_text,
                ),
                buttons=[
                    MDFillRoundFlatButton(text='Save', on_release=self.save_item),
                    MDFillRoundFlatButton(text='Delete', on_release=self.delete_item)
                ]
            ).open()

    def delete_item(self, instance):
        print(f'deleting {self.text}, from {self.model}')
    

    def save_item(self, instance):
        print(f'saving {self.text}, from {self.model}')


class CustomTwoLineAvatarListItem(TwoLineAvatarListItem):
    start = 0
    stop = 0
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model

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
    
            MDDialog(
                title=title,
                type='custom',
                content_cls=EditDialogContent(
                    primary_text=self.text,
                    secondary_text=self.secondary_text,
                ),
                buttons=[
                    MDFillRoundFlatButton(text='Save', on_release=self.save_item),
                    MDFillRoundFlatButton(text='delete', on_release=self.delete_item)
                ]
            ).open()
    def delete_item(self, instance):
        print(f'deleting {self.text}, from {self.model}')
    
    def save_item(self, instance):
        print(f'saving {self.text}, from {self.model}')
    

    def on_press(self):
        self.start = time.time()

    def on_touch_down(self, *args, **kwargs):
        super().on_touch_down(*args, **kwargs)
    

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        self.color = 'White'
        return AppRoot()

    def on_start(self):
        create_tables()

    def submit_lessons_form(self, name, description):
        if name.text != '' and description.text != '':
            lesson = CustomThreeLineAvatarListItem(
                model='lesson',
                text=name.text,
                secondary_text=description.text,
                tertiary_text=str(datetime.now()),
            )
            icon = IconLeftWidget(icon='book')
            lesson.add_widget(icon)
            self.root.ids.lessons_list.add_widget(lesson)
            add_lesson(name.text, description.text,str(datetime.now()) )
            # clear the name and description textinputs
            name.text = ''
            description.text = ''


    def submit_tutors_form(self, contact, full_name):
        if contact.text !='' and full_name.text !='':
            tutor = CustomTwoLineAvatarListItem(
                model='tutor',
                text=full_name.text,
                secondary_text=contact.text,
            )
            icon = IconLeftWidget(icon='account')
            tutor.add_widget(icon)
            self.root.ids.tutors_list.add_widget(tutor)
            # save in the database table
            add_tutor(full_name.text, contact.text)
            #clears the input widgets
            contact.text = ''
            full_name.text = ''

    
    def submit_courses_form(self, title, name):
        if title.text != '' and name.text != '':
            course = CustomTwoLineAvatarListItem(
                model='course',
                text=title.text,
                secondary_text=name.text,
            )
            icon = IconLeftWidget(icon='school')
            course.add_widget(icon)
            self.root.ids.courses_list.add_widget(course)
            add_course(title.text, name.text)
            # clear the input widgets
            title.text = ''
            name.text = ''

    def add_tutor(self):
        self.dialog  = MDDialog(
            title='Add teacher/lecturer', 
            type='custom', 
            content_cls=Content()
        )
        self.dialog.open()


    def add_lesson(self):
        self.dialog  = MDDialog(
            title='Add lesson/topic', 
            type='custom', 
            content_cls=LessonDialog()
        )
        self.dialog.open()

    def add_course(self):
        self.dialog  = MDDialog(
            title='Add course/subject', 
            type='custom', 
            content_cls=CourseDialog()
        )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()

MyApp().run()