import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation

class PresentationSlide(Screen):
    def __init__(self, title, content, background_color=(1, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        self.title_label = Label(
            text=title, 
            font_size='24sp', 
            bold=True, 
            color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.title_label)
        
        # Content
        self.content_label = Label(
            text=content, 
            font_size='16sp', 
            color=(0.2, 0.2, 0.2, 1),
            text_size=(Window.width * 0.8, None),
            halign='center',
            valign='top'
        )
        self.layout.add_widget(self.content_label)
        
        # Background
        with self.canvas.before:
            Color(*background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.add_widget(self.layout)
        
        # Bind size and position updates
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class BananaMathPuzzlePresentationApp(App):
    def build(self):
        # Screen Manager
        sm = ScreenManager()
        
        # Slides
        slides = [
            {
                'name': 'intro',
                'title': 'Banana Math Puzzle: Software Design Journey',
                'content': 'An innovative educational game\n'
                           'Exploring software design principles\n'
                           'Making math learning fun and interactive',
                'background_color': (1, 0.9, 0.6, 1)  # Banana yellow
            },
            {
                'name': 'design_principles',
                'title': 'Software Design Principles',
                'content': 'Object-Oriented Design\n'
                           'Low Coupling, High Cohesion\n'
                           'Modular, Extensible Architecture',
                'background_color': (0.9, 1, 0.7, 1)  # Light green
            },
            {
                'name': 'event_driven',
                'title': 'Event-Driven Programming',
                'content': 'Interactive User Experiences\n'
                           'Responsive Game Mechanics\n'
                           'Dynamic State Management',
                'background_color': (0.7, 0.9, 1, 1)  # Light blue
            },
            {
                'name': 'interoperability',
                'title': 'Interoperability',
                'content': 'Banana API Integration\n'
                           'Dynamic Puzzle Generation\n'
                           'Secure, Asynchronous Communication',
                'background_color': (1, 0.8, 0.8, 1)  # Light pink
            },
            {
                'name': 'virtual_identity',
                'title': 'Virtual Identity',
                'content': 'Personalized Player Profiles\n'
                           'Achievement Tracking\n'
                           'Secure User Management',
                'background_color': (0.9, 0.7, 1, 1)  # Light purple
            },
            {
                'name': 'conclusion',
                'title': 'The Journey Continues',
                'content': 'More Than a Game\n'
                           'A Learning Experience\n'
                           'Pushing Software Design Boundaries',
                'background_color': (1, 1, 0.8, 1)  # Light yellow
            }
        ]
        
        # Create slides
        for slide in slides:
            sm.add_widget(PresentationSlide(
                name=slide['name'], 
                title=slide['title'], 
                content=slide['content'],
                background_color=slide['background_color']
            ))
        
        # Navigation buttons
        nav_layout = BoxLayout(size_hint_y=None, height=50)
        prev_btn = Button(text='Previous', on_press=self.go_previous)
        next_btn = Button(text='Next', on_press=self.go_next)
        nav_layout.add_widget(prev_btn)
        nav_layout.add_widget(next_btn)
        
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(sm)
        main_layout.add_widget(nav_layout)
        
        return main_layout
    
    def go_previous(self, instance):
        self.root.current = self.root.previous()
    
    def go_next(self, instance):
        self.root.current = self.root.next()

if __name__ == '__main__':
    BananaMathPuzzlePresentationApp().run()
