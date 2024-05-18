from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from kivy.uix.scrollview import ScrollView
from ButtonInputs import ButtonInputs
from ComboValidityCheck import ComboValidityChecker
from ComboToLEDConversion import ledCode
import time

cred = credentials.Certificate(r"/home/dojo/Desktop/CapstoneProject-main/dojoui/dojo-capstone-firebase-adminsdk-xntkg-a7ee737a7a.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

collection_name = "combos"

combos_ref = db.collection("combos")
combos = combos_ref.stream()

combo_list = [combo.to_dict() for combo in combos]

feedback = []

selected_combo = [combo_list[0]['name'], " > ".join(str(x) for x in combo_list[0]['combo'])]

class CharacterGrid(GridLayout):
    def __int__(self, **kwargs):
        super(CharacterGrid, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 1

        for i in range(3):
            image = Image(source=str(i) + '.jpg')
            self.add_widget(image)


class CharacterSelectionLayout():
    def __int__(self, **kwargs):
        self.cols = 2


def nav_to_combos_select(self):
    app = App.get_running_app()
    #
    app.sm.current = "home"


def nav_to_combos(instance, data):
    global selected_combo
    selected_combo = data
    app = App.get_running_app()
    #
    app.sm.current = "combos"



class CharacterSelectScreen(Screen):
    def __init__(self, **kwargs):
        super(CharacterSelectScreen, self).__init__(**kwargs)
        self.name = "char_select"
        character_grid = CharacterGrid()
        character_grid.cols = 4
        character_grid.rows = 1
        self.size = (1480, 320)

        for i in range(4):
            image = Button(
                background_normal=str(i) + '.jpg',
                background_down=str(i) + '.jpg',
                size_hint=(.2, .2),
                pos_hint={"x": 0.2, "y": 0.2}
            )
            image.bind(on_press=nav_to_combos_select)
            character_grid.add_widget(image)
        self.add_widget(character_grid)


class ComboDetailsGrid(GridLayout):
    def __int__(self, **kwargs):
        super(ComboDetailsGrid, self).__init__(**kwargs)


class ComboSelectionGrid(GridLayout):

    def __init__(self, **kwargs):
        super(ComboSelectionGrid, self).__init__(**kwargs)
        self.cols = 4

        combo_details_grid = ComboDetailsGrid(rows=2, cols=1)
        combo_name_lbl = Label(text="Ryu")
        combo_steps_lbl = Label(text=str(combo_list[0]['combo']))
        combo_name_lbl.pos_hint = {'x': 0, 'y': 0}
        combo_steps_lbl.pos_hint = {'x': 0, 'y': 0}
        combo_details_grid.add_widget(Image(source='0.jpg'))
        combo_details_grid.add_widget(combo_name_lbl)

        scroll_view = ScrollView(size_hint_min=(1, None), size=(Window.width, 150))
        moves_list = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None)
        moves_list.bind(minimum_height=moves_list.setter('height'))

        for combo_dict in combo_list:
            combo_name = combo_dict['name']
            combo = " > ".join(str(x) for x in combo_dict['combo'])
            button = Button(text=f"{combo_name}: {combo}", size_hint_y=None, height=60)
            button.bind(on_press=partial(nav_to_combos, data=[combo_name, combo]))
            moves_list.add_widget(button)

        scroll_view.add_widget(moves_list)
        combo_details_grid.size_hint_x = 0.3

        reload_btn = Button(text="Reload")
        select_btn = Button(text="Select")
        prev_btn = Button(text="Back")
        next_btn = Button(text="Next")

        reload_btn.size_hint_x = 0.3
        select_btn.size_hint_x = 0.3
        prev_btn.size_hint_x = 0.3
        next_btn.size_hint_x = 0.3

        def reload(self):
            global combo_list
            global combos_ref
            global combos
            combos_ref = db.collection("combos")
            combos = combos_ref.stream()

            combo_list = [combo.to_dict() for combo in combos]
            scroll_view.clear_widgets()
            moves_list.clear_widgets()
            for cd in combo_list:
                cn = cd['name']
                cmbo = " > ".join(str(x) for x in cd['combo'])
                btn = Button(text=f"{cn}: {cmbo}", size_hint_y=None, height=60)
                btn.bind(on_press=partial(nav_to_combos, data=[cn, cmbo]))
                moves_list.add_widget(btn)

            print(moves_list)
            scroll_view.add_widget(moves_list)
            combo_details_grid.size_hint_x = 0.3

        def select(self):
            print("select")

        def previous(self):
            app = App.get_running_app()
            app.sm.current = "char_select"

        def next_combo(self):
            global selected_combo
            selected_combo = (selected_combo + 1) % len(combo_list)
            combo_name_lbl.text = combo_list[selected_combo]["name"]
            combo_steps_lbl.text = str(combo_list[selected_combo]["combo"])
            print("next")

        reload_btn.bind(on_press=reload)
        select_btn.bind(on_press=select)
        prev_btn.bind(on_press=previous)
        next_btn.bind(on_press=next_combo)

        self.add_widget(prev_btn)
        self.add_widget(combo_details_grid)
        self.add_widget(scroll_view)
        self.add_widget(reload_btn)


class ComboGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ComboGrid, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 4

        self.selected_combo_name = selected_combo[0]
        self.selected_combo_moves = selected_combo[1].split(' > ')

        def frameNumberAssignment(savedCombo):
            # savedCombo = [item.replace("Ryu-", '') for item in savedCombo if "Ryu-" in item]
            ryuFrameData = [
                ["5LP", 4, 12, 7, 22, "ALL", 4],
                ["5MP", 6, 15, 11, 31, "ALL", 7],
                ["5HP", 10, 18, 18, 45, "ALL", 3],
                ["5LK", 5, 12, 11, 27, "ALL", 2],
                ["5MK", 9, 14, 18, 40, "NONE", 4],
                ["5HK", 12, 17, 20, 48, "NONE", 9],
                ["2LP", 4, 11, 9, 23, "ALL", 4],
                ["2MP", 6, 14, 14, 33, "ALL", 5],
                ["2HP", 9, 19, 21, 48, "ALL", 1],
                ["2LK", 5, 11, 10, 25, "NONE", 3],
                ["2MK", 8, 12, 19, 38, "ALL", 1],
                ["2HK", 9, 16, 23, 47, "NONE", 32],
                ["6MP", 20, 22, 19, 60, "NONE", 2],
                ["6HP", 20, 27, 16, 62, "NONE", 6],
                ["4HP", 7, 17, 25, 48, "ALL", 1],
                ["4HK", 10, 26, 21, 56, "ALL", 0],
                ["6HK", 16, 17, 20, 52, "NONE", 2],
                ["236LP", 16, 0, 31, 47, "SA3", -1],
                ["236MP", 14, 0, 33, 47, "SA3", -3],
                ["236HP", 12, 0, 35, 47, "SA3", -5],
                ["236PP", 12, 0, 28, 40, "SA2 SA3", 54],
                ["623LP", 5, 25, 33, 62, "SA3", 38],
                ["623MP", 6, 25, 42, 72, "SA3", 34],
                ["623HP", 7, 25, 49, 80, "SA3", 29],
                ["623PP", 7, 24, 52, 82, "NONE", 29],
                ["214LK", 12, 18, 32, 61, "NONE", 35],
                ["214MK", 14, 31, 31, 76, "NONE", 23],
                ["214HK", 16, 46, 31, 93, "NONE", 20],
                ["214KK", 13, 51, 23, 87, "NONE", 57],
                ["236LK", 15, 24, 22, 60, "SA3", 35],
                ["236MK", 18, 24, 19, 60, "SA3", 40],
                ["236HK", 29, 29, 16, 73, "SA3", 45],
                ["236KK", 18, 25, 33, 75, "SA2 SA3", 49],
                ["214LP", 12, 21, 18, 50, "SA3", 2],
                ["214MP", 19, 21, 17, 56, "SA3", 2],
                ["214HP", 30, 36, 19, 84, "SA3", 61],
                ["214PP", 18, 21, 20, 58, "SA2 SA3", 3],
                ["214P Denjin", 21, 6, 18, 44, "SA3", 62],
                ["236236P", 8, 0, 79, 87, "NONE", 26],
                ["214214P", 12, 24, 39, 74, "NONE", 20],
                ["236236K", 5, 12, 71, 87, "NONE", 8],
                ["THROW", 5, 9, 23, 36, "NONE", 17],
                ["DI", 26, 27, 35, 87, "NONE", 65],
                ["PARRY (RAW)", 11, 56, 23, 89, "NONE", 0],
                ["PARRY", 9, 54, 24, 86, "NONE", 0],
                ["236P", 16, 0, 31, 47, "SA3", -1],
                ["623P", 5, 25, 33, 62, "SA3", 38],
                ["214K", 12, 18, 32, 61, "NONE", 35],
                ["236K", 15, 24, 22, 60, "SA3", 35],
                ["214P", 12, 21, 18, 50, "SA3", 2]
            ]
            special_moves = [
            '236LP', '236MP', '236HP', '236PP',
            '623LP', '623MP', '623HP', '623PP',
            '214LK', '214MK', '214HK', '214KK',
            '236LK', '236MK', '236HK', '236KK',
            '214LP', '214MP', '214HP', '214PP',
            '236236P', '214214P', '236236K', 'PARRY'
            ]
            cancels = {'SA2': ['214214P', '623623P'], 'SA3': '236236K', 'ALL': special_moves, 'NONE': []}

            moveArray = savedCombo
            comboWithFrames = []
            if len(moveArray) != 0:
                last_max_frame = 0
                comboWithFrames.append([moveArray[0], 1])

                for i in range(1, len(moveArray)):
                    player_move = moveArray[i] # Move the player executed
                    last_player_move = moveArray[i-1]
                    last_move_data = [*[row for row in ryuFrameData if row[0] == moveArray[i-1]][0]]
                    last_startup = int(last_move_data[1])
                    last_total = int(last_move_data[4])
                    last_cancel_flag = last_move_data[5]

                    if player_move in cancels[last_cancel_flag]:
                        last_max_frame = last_startup + 1
                    elif last_player_move == "PARRY":
                        last_max_frame = last_startup + 1
                    else:
                        last_max_frame = last_total + 1
                    comboWithFrames.append([moveArray[i], last_max_frame])
            return comboWithFrames

        self.combowithframes = frameNumberAssignment(self.selected_combo_moves)
        
        #self.buttonInputs = ButtonInputs(self.combowithframes)
        #self.leds = ledCode(self.combowithframes)

        self.demoflag = False
        char_lbl = Label(text="Ryu")
        combo_lbl = Label(text=self.selected_combo_name)
        icon = Image(source='0.jpg')
        back_btn = Button(text="Back")
        self.demo_btn = Button(text="Demo Lights")
        self.start_btn = Button(text = "Start")
        self.demo_btn.size_hint_x = 0.2
        char_lbl.size_hint_x = 0.2
        self.start_btn.size_hint_x = 0.2
        icon.size_hint_x = 0.2
        back_btn.size_hint_x = 0.2
        moves_grid = GridLayout()
        moves_grid.cols = 16
        moves_grid.rows = 1

        for move in self.selected_combo_moves:
            moves_grid.add_widget(Label(text=move))

        def back(self):
            app = App.get_running_app()
            app.sm.current = "home"

        back_btn.bind(on_press=back)
        self.demo_btn.bind(on_press=self.demo)
        self.start_btn.bind(on_press=self.start)

        self.add_widget(icon)
        self.add_widget(combo_lbl)
        self.add_widget(self.demo_btn)
        self.add_widget(moves_grid)
        self.add_widget(back_btn)
        self.add_widget(self.start_btn)


    def demo(self, temp):
        leds = ledCode(self.combowithframes)
        leds.run()
        del leds        

    def start(self, temp):
        self.leds.startSequence()
        buttonInputs = ButtonInputs(self.combowithframes)
        output = buttonInputs.run()
        del buttonInputs
        global feedback
        feedback.clear()
        feedback = output
        app = App.get_running_app()
        app.sm.current = "feedback"

    def on_leave(self, *args):
        self.clear_widgets()


class ComboScreen(Screen):
    def __init__(self, **kwargs):
        super(ComboScreen, self).__init__(**kwargs)
        self.name = "combos"
        self.size = (1480, 320)

    def on_pre_enter(self, *args):
        combo_grid = ComboGrid()
        self.add_widget(combo_grid)

    def on_leave(self, *args):
        self.clear_widgets()

class feedbackScreen(Screen):
    def __init__(self):
        super(feedbackScreen, self).__init__()
        self.name = "feedback"
        global feedback
        self.feedback_lbl = Label
        self.restart_btn = Button(text="Restart \ncombo")
        self.comboMenu_btn = Button(text="Return to \nCombo Menu")
        self.restart_btn.size_hint_x = 0.2
        self.comboMenu_btn.size_hint_x = 0.2
        self.size = (1480, 320)
        self.feedback_grid = GridLayout()
        self.feedback_grid.cols = 3
        self.feedback_grid.rows = 1

        def restart(self):
            feedback.clear()
            app = App.get_running_app()
            app.sm.current = "combos"

        def comboMenu(self):
            feedback.clear()
            app = App.get_running_app()
            app.sm.current = "home"

        self.restart_btn.bind(on_press = restart)
        self.comboMenu_btn.bind(on_press = comboMenu)
        self.feedback_grid.add_widget(self.restart_btn)
        self.feedback_grid.add_widget(self.comboMenu_btn)
        self.add_widget(self.feedback_grid)

    def on_pre_enter(self, *args):
        feedbackString = ""
        for row in feedback:
            feedbackString += str(row)
            feedbackString += "\n"
        self.feedback_lbl = Label(text = feedbackString)
        self.feedback_grid.add_widget(self.feedback_lbl)

    def on_leave(self, *args):
        self.feedback_grid.remove_widget(self.feedback_lbl)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.name = "home"
        self.cols = 2
        self.add_widget(ComboSelectionGrid())
        self.size = (1480, 320)


class DojoUI(App):
    def build(self):
        Window.size = (1480, 320)
        Window.maximize()
        self.sm = ScreenManager()
        character_select_screen = CharacterSelectScreen()
        self.sm.add_widget(character_select_screen)

        home_screen = HomeScreen()
        self.sm.add_widget(home_screen)

        combo_screen = ComboScreen()
        self.sm.add_widget(combo_screen)

        feedback_screen = feedbackScreen()
        self.sm.add_widget(feedback_screen)
        self.sm.size = (1480,320)
        return self.sm

if __name__ == '__main__':
    DojoUI().run()
