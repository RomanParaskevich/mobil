import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
#from kivy.core.window import Window


#Window.size = (390, 844)

# Первая страница
class StatisticsScreen(Screen):
    total_count = StringProperty("0 шт.")
    total_weight = StringProperty("0.0 кг")

    def on_enter(self):
        self.update_ui()

    def update_ui(self):
        app = App.get_running_app()
        # Загрузка данных
        fish_list = app.load_fish_data()
        
        # Статистика
        count = len(fish_list)
        weight = sum(item["weight"] for item in fish_list)
        
        self.total_count = f"{count} шт."
        self.total_weight = f"{weight:.2f} кг"
        
        # Очищаем старый список и строим новый заново
        # Используем reversed, но сохраняем оригинальные индексы для удаления
        self.ids.history_layout.clear_widgets()
        
        for original_index in reversed(range(len(fish_list))):
            item = fish_list[original_index]
            
            row = BoxLayout(
                orientation='horizontal', 
                size_hint_y=None, 
                height=50, 
                padding=[10, 5, 10, 5],
                spacing=10
            )
            
            fish_label = Label(
                text=f"🐟 {item['species']}: {item['weight']} кг", 
                color=(0, 0, 0, 1),
                halign='left',
                valign='middle'
            )
            fish_label.bind(size=fish_label.setter('text_size'))
            
            delete_btn = Button(
                text="❌",
                size_hint_x=None,
                width=40,
                background_color=(0.9, 0.3, 0.3, 1),
                background_normal='',
                on_release=lambda btn, idx=original_index: self.delete_fish_item(idx)
            )
            
            row.add_widget(fish_label)
            row.add_widget(delete_btn)
            self.ids.history_layout.add_widget(row)

    # Удалить по индексу и обновить экран
    def delete_fish_item(self, index):
        app = App.get_running_app()
        app.delete_fish_by_index(index)
        self.update_ui()

# Вторая страница
class InputScreen(Screen):
    error_message = StringProperty("")

    def save_catch(self):
        species = self.ids.species_input.text.strip()
        weight_str = self.ids.weight_input.text.strip().replace(",", ".")

        if not species:
            self.error_message = "Введите вид рыбы!"
            return
        
        try:
            weight = float(weight_str)
            if weight <= 0:
                raise ValueError
        except ValueError:
            self.error_message = "Введите корректный вес (> 0)!"
            return

        # Сохраняем в хранилище через главный класс приложения
        app = App.get_running_app()
        app.save_fish_item(species, weight)
        
        # Сбрасываем поля формы
        self.ids.species_input.text = ""
        self.ids.weight_input.text = ""
        self.error_message = ""
        
        # Возвращаемся на главный экран
        self.manager.current = 'statistics'


class FishingApp(App):
    def build(self):
        # Инициализируем локальную базу данных
        self.store = JsonStore('fishing_data.json')
        
        sm = ScreenManager()
        sm.add_widget(StatisticsScreen(name='statistics'))
        sm.add_widget(InputScreen(name='input'))
        return sm

    def load_fish_data(self):
        if self.store.exists('history'):
            return self.store.get('history')['data']
        else:
            # Данные при первом запуске
            initial_data = []
            self.store.put('history', data=initial_data)
            return initial_data

    def save_fish_item(self, species, weight):
        current_data = self.load_fish_data()
        current_data.append({"species": species, "weight": weight})
        self.store.put('history', data=current_data)

    def delete_fish_by_index(self, index):
        current_data = self.load_fish_data()
        if 0 <= index < len(current_data):
            current_data.pop(index)
            self.store.put('history', data=current_data)


if __name__ == '__main__':
    # Интерфейс на языке KV Language
    from kivy.lang import Builder
    Builder.load_string('''
#:import Window kivy.core.window.Window

<StatisticsScreen>:
    canvas.before:
        Color:
            rgba: 0.95, 0.97, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 15

        Label:
            text: "Статистика улова"
            font_size: '22sp'
            bold: True
            color: 0.1, 0.2, 0.4, 1
            size_hint_y: None
            height: 50

        GridLayout:
            cols: 2
            size_hint_y: None
            height: 80
            spacing: 10

            BoxLayout:
                orientation: 'vertical'
                padding: 10
                canvas.before:
                    Color:
                        rgba: 0.88, 0.95, 0.88, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]
                Label:
                    text: "Всего поймано"
                    font_size: '14sp'
                    color: 0.2, 0.4, 0.2, 1
                Label:
                    text: root.total_count
                    font_size: '18sp'
                    bold: True
                    color: 0, 0, 0, 1

            BoxLayout:
                orientation: 'vertical'
                padding: 10
                canvas.before:
                    Color:
                        rgba: 0.88, 0.92, 0.98, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]
                Label:
                    text: "Общий вес"
                    font_size: '14sp'
                    color: 0.2, 0.3, 0.6, 1
                Label:
                    text: root.total_weight
                    font_size: '18sp'
                    bold: True
                    color: 0.1, 0.4, 0.8, 1

        Label:
            text: "История улова:"
            font_size: '16sp'
            bold: True
            color: 0, 0, 0, 1
            size_hint_y: None
            height: 30
            halign: 'left'
            text_size: self.size

        ScrollView:
            do_scroll_x: False
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10]
            GridLayout:
                id: history_layout
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
                padding: [0, 5, 0, 5]

        Button:
            text: "+ Добавить улов"
            font_size: '16sp'
            size_hint_y: None
            height: 50
            background_color: 0.2, 0.6, 1, 1
            background_normal: ''
            on_release: root.manager.current = 'input'


<InputScreen>:
    canvas.before:
        Color:
            rgba: 0.95, 0.97, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: "Новый улов"
            font_size: '22sp'
            bold: True
            color: 0.1, 0.2, 0.4, 1
            size_hint_y: None
            height: 50

        Label:
            text: "Что вы поймали?"
            font_size: '16sp'
            color: 0, 0, 0, 1
            size_hint_y: None
            height: 20
            halign: 'left'
            text_size: self.size

        TextInput:
            id: species_input
            hint_text: "Вид рыбы (например, Плотва)"
            multiline: False
            size_hint_y: None
            height: 45
            font_size: '16sp'
            padding: [10, 10, 10, 10]

        TextInput:
            id: weight_input
            hint_text: "Вес в кг (например, 1.2)"
            multiline: False
            size_hint_y: None
            height: 45
            font_size: '16sp'
            padding: [10, 10, 10, 10]
            input_filter: 'float'

        Label:
            text: root.error_message
            font_size: '14sp'
            color: 1, 0, 0, 1
            size_hint_y: None
            height: 25
        
        Widget:
            size_hint_y: 1
        
        Button:
            text: "Сохранить улов"
            font_size: '16sp'
            size_hint_y: None
            height: 50
            background_color: 0.2, 0.7, 0.3, 1
            background_normal: ''
            on_release: root.save_catch()
        
        Button:
            text: "Отмена"
            font_size: '16sp'
            size_hint_y: None
            height: 50
            background_color: 0.7, 0.7, 0.3, 1
            background_normal: ''
            on_release: 
                root.manager.current = 'statistics'
                root.error_message = ""
''')

FishingApp().run()
