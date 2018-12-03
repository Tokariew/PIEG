from math import isnan

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from maintable import MainTable

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class SelectableRecycleBoxLayout(FocusBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class Col(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = 0

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = data['col_number']
        return super(Col, self).refresh_view_attrs(
            rv, index, data)


class IterPopup(Popup):
    pass


class MagPopup(Popup):
    pass


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []


class NosWidget(Screen):
    def __init__(self, **kwargs):
        super(NosWidget, self).__init__(**kwargs)

    def validate_input(self, instance):
        elem = int(instance.text)
        app = App.get_running_app()
        app.main.gen_table(elem + 1)
        app.sm.current = 'main'
        instance.text = ''

    def help(self, instance):
        print('nos')


class MainWidget(Screen):
    def validate_input(self, instance):
        if not isnan(instance.data):
            return
        instance.text = instance.text.replace(',', '.')
        try:
            instance.data = float(instance.text)
        except ValueError:
            instance.text = '' if isnan(instance.data) else '{:0.2f}'.format(instance.data).rstrip('0').rstrip('.')
        if isnan(instance.data):
            return
        if instance.param == 'vignette':
            if float(instance.text) > 1 or float(instance.text) < 0:
                instance.data = float('nan')
                return
            self.table2.set_vignetting(float(instance.text))
            self.update_table()
            return
        col = int(instance.parent.col_number)
        row = self.forward_map[instance.param]
        val = float(instance.data)
        self.table2.change_value(row, col, val)
        self.update_table()

        print(instance.data, instance.parent.col_number, instance.param)

    def help(self, instance):
        if not instance.focus:
            self.validate_input(instance)

    def update_table(self):
        temp = self.table2.table.to_dict()
        for item in temp.items():
            it = dict([(self.reverse_map[key], float('nan') if value == '' else value)
                       for key, value in item[1].items()])
            it['col_number'] = item[0]
            self.ids.table.data[item[0]] = it
            if not isnan(self.table2.LHI):
                self.ids.lhi_label.data = str(self.table2.LHI)
            else:
                self.ids.lhi_label.data = float('nan')
            if isnan(self.table2.vignette):
                self.ids.vignette_input.data = float('nan')
            else:
                self.ids.vignette_input.data = self.table2.vignette

    def gen_table(self, cols):
        nan = float('nan')
        self.ids.table.data = [{'col_number': i, 'f': nan, 'd': nan, 'h': nan, 'alpha': nan,
                                'v': nan, 'l': nan, 'y1': nan, 'beta': nan, 'q': nan, 't': nan, 'phi': nan} for i in range(cols)]
        self.table2 = MainTable(cols)

    def key_action(self, key, keycode, text, modif):
        if keycode[1] == 'z' and modif[0] == 'ctrl':
            self.update_label('Undo')
            self.table2.undo_changes()
            self.update_table()

    def _activ_key(self, *args):
        """ The active keyboard is being closed. """
        self.keyboard = None

    def plot(self):
        try:
            self.table2.plot()
        except ValueError:
            self.update_label('Not enough data')

    def export(self):
        self.table2.table.to_csv('out.csv')

    def debug(self):
        with open('debug.log', 'w') as file:
            for line in self.table2.history:
                file.write('{}\n'.format(line))

    def update_label(self, msg):
        self.ids.info_label.text = msg

    def magnify(self, v_check, from_col, to_col, val):
        var = 'V' if v_check else 'Q'
        self.table2.magnification(float(from_col), float(to_col), float(val), var)
        self.update_table()

    def iterate(self, d_check, L_check, from_c, to_c, targ, start, row, col):
        if not (d_check or L_check):
            dim = 'T'
        elif d_check:
            dim = 'd'
        else:
            dim = 'L'
        from_c, to_c, targ, start, col = float(from_c), float(to_c), float(targ), float(start), float(col)
        self.table2.iterate(row, col, from_c, to_c, dim, targ, start)
        self.update_table()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.table = self.ids.table.data
        self.table2 = []
        self.forward_map = {'f': 'f', 'd': 'd', 'h': 'H', 'alpha': 'alpha', 'v': 'V',
                            'l': 'L', 'y1': 'Y', 'beta': 'Beta', 'q': 'Q', 't': 'T', 'phi': 'phi', 'vignette': 'vignette', 'lhi': 'lhi'}
        self. reverse_map = dict(reversed(item) for item in self.forward_map.items())
        self.keyboard = Window.request_keyboard(self._activ_key, self)
        self.keyboard.bind(on_key_down=self.key_action)
        self.iter_pop = IterPopup()
        self.mag_pop = MagPopup()


class GabApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.main = MainWidget(name='main')
        self.nos = NosWidget(name='nos')
        self.sm.add_widget(self.nos)
        self.sm.add_widget(self.main)
        return self.sm


if __name__ == '__main__':
    GabApp().run()
