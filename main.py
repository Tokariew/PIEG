import os
import sys
from math import isnan
from os import mkdir
from os.path import expanduser, join

import matplotlib as mpl
import numpy as np
from imageio import imsave

import kivy.resources
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import ClearBuffers, Fbo, Scale, Translate
from kivy.properties import NumericProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from maintable import MainTable


def resourcePath():
    '''Returns path containing content - either locally or in pyinstaller tmp file'''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)

    return os.path.join(os.path.abspath("."))


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
    cols = NumericProperty(0)


class MagPopup(Popup):
    cols = NumericProperty(0)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []


class NosWidget(Screen):
    def __init__(self, **kwargs):
        super(NosWidget, self).__init__(**kwargs)
        self.noe_input = self.ids.noe_input

    def validate_input(self, instance):
        try:
            elem = int(instance.text)
            app = App.get_running_app()
            app.main.gen_table(elem + 1)
            app.sm.current = 'main'
            instance.text = ''
            app.main.focus_row = ''
            app.main.focus_column = ''
        except ValueError:
            self.ids.info_label.text = 'Please, enter the correct number of columns'


class MainWidget(Screen):

    def validate_input(self, instance):
        if instance.focus:
            self.focus_row = instance.param
            if self.focus_row == 'vignette':
                self.focus_row = ''
                return
            self.focus_column = instance.parent.col_number
        if not instance.focus:
            if not isnan(instance.data):
                return
            instance.text = instance.text.replace(',', '.')
            try:
                instance.data = float(instance.text)
            except ValueError:
                instance.text = '' if isnan(instance.data) else '{:g}'.format(instance.data)
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
            if self.table2.table.loc[row, col] == '':
                instance.text = ''
                return
            val = float(instance.data)
            instance.user = True
            print(instance.user)
            self.table2.change_value(row, col, val)
            self.update_table()

    def help_me(self, instance):
        if instance.param == 'vignette':
            return
        col = int(instance.parent.col_number)
        row = self.forward_map[instance.param]
        print(row, col, self.table2.table.loc[row, col])
        if self.table2.table.loc[row, col] == '':
            return
        if instance.text != '' and instance.user:
            return
        if isnan(self.table2.table.loc[row, col]):
            instance.user = False
            print(col, row, 'set as False')

    def validate_popup_input(self, instance):
        if not instance.focus:
            instance.text = instance.text.replace(',', '.')
            try:
                instance.data = float(instance.text)
            except ValueError:
                instance.text = '{:g}'.format(instance.data)

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
        self.cols = cols
        self.iter_pop = IterPopup(cols=cols)
        self.mag_pop = MagPopup(cols=cols)

    def key_action(self, key, keycode, text, modif):
        if len(modif) == 1:
            if keycode[1] == 'z' and modif[0] == 'ctrl':
                self.update_label('Undo')
                self.table2.undo_changes()
                self.update_table()
        app = App.get_running_app()
        if app.sm.current == 'main' and not self.focus_column == '' and not self.focus_row == '':
            if keycode[1] == 'left':
                all = len(self.ids.table.children[0].children)
                col = all - self.focus_column
                if col > 0 and col < all:
                    for children in self.ids.table.children[0].children[col].children:
                        if children.param == self.focus_row:
                            children.focus = True
            if keycode[1] == 'right':
                all = len(self.ids.table.children[0].children)
                col = all - (self.focus_column + 2)
                if col >= 0 and col < all:
                    for children in self.ids.table.children[0].children[col].children:
                        try:
                            if children.param == self.focus_row:
                                children.focus = True
                        except AttributeError:
                            pass
            if keycode[1] == 'up':
                all = len(self.ids.table.children[0].children)
                col = all - (self.focus_column + 1)
                index = self.ids.table.children[0].children[col].par_q.index(self.focus_row) - 1
                param = self.ids.table.children[0].children[col].par_q[index]
                for children in self.ids.table.children[0].children[col].children:
                    try:
                        if children.param == param:
                            children.focus = True
                    except AttributeError:
                        pass
            if keycode[1] == 'down':
                all = len(self.ids.table.children[0].children)
                col = all - (self.focus_column + 1)
                index = self.ids.table.children[0].children[col].par_q.index(self.focus_row) + 1
                param = self.ids.table.children[0].children[col].par_q[index]
                for children in self.ids.table.children[0].children[col].children:
                    try:
                        if children.param == param:
                            children.focus = True
                    except AttributeError:
                        pass

    def _activ_key(self, *args):
        """ The active keyboard is being closed. """
        self.keyboard = None

    def plot(self):
        try:
            self.table2.plot()
        except ValueError:
            self.update_label('Not enough data')

    def export(self):
        name = join(self.home, 'out.csv')
        self.table2.table.to_csv(name)

    def history(self):
        name = join(self.home, 'history.log')
        with open(name, 'w') as file:
            for line in self.table2.history_input:
                file.write('{}\n'.format(line))

    def update_label(self, msg):
        self.ids.info_label.text = msg

    def magnify(self, v_check, from_col, to_col, val):
        var = 'V' if v_check else 'Q'
        self.table2.magnification(float(from_col), float(to_col), float(val), var)
        self.update_table()
        tmp = ['Magnification {:.2f}, from surface {:.0f} to {:.0f}, type {}'.format(
            dic['magn'], dic['from'], dic['to'], dic['type']) for dic in self.table2.magnify]
        self.ids.magnify_info.text = '\n'.join(tmp)

    def iterate(self, d_check, L_check, from_c, to_c, targ, start, row, col):
        if not (d_check or L_check):
            dim = 'T'
        elif d_check:
            dim = 'd'
        else:
            dim = 'L'
        if row == '\u03B1':
            row = 'alpha'
        elif row == '\u03B2':
            row = 'Beta'
        if self.table2.table.loc[row, int(col)] == '':
            self.update_label("Can't iterate this value")
            return
        from_c, to_c, targ, start, col = int(from_c), int(to_c), float(targ), float(start), int(col)
        try:
            self.table2.iterate(row, col, from_c, to_c, dim, targ, start)
            self.update_table()
        except ValueError as e:
            self.update_label(str(e))

    def capture(self):
        name = join(self.home, 'screen.png')
        self.export_png(name)

    def export_png(self, name):
        print(self.home)
        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=self.size, with_stencilbuffer=True)

        with fbo:
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        test = np.frombuffer(fbo.texture.pixels, dtype=np.uint8)
        test = np.copy(test.reshape((self.height, self.width, 4)))
        alpha = -test[:, :, -1]
        test[:, :, -1] = alpha
        imsave(name, -test)
        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        return True

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.table = self.ids.table.data
        self.table2 = []
        self.forward_map = {'f': 'f', 'd': 'd', 'h': 'H', 'alpha': 'alpha', 'v': 'V',
                            'l': 'L', 'y1': 'Y', 'beta': 'Beta', 'q': 'Q', 't': 'T', 'phi': 'phi', 'vignette': 'vignette', 'lhi': 'lhi'}
        self. reverse_map = dict(reversed(item) for item in self.forward_map.items())
        self.keyboard = Window.request_keyboard(self._activ_key, self)
        self.keyboard.bind(on_key_down=self.key_action)
        self.cols = 0
        self.iter_pop = None
        self.mag_pop = None
        self.focus_column = ''
        self.focus_row = ''
        self.home = join(expanduser('~'), 'Documents', 'PIEG')
        mpl.rcParams["savefig.directory"] = self.home
        try:
            mkdir(self.home)
        except FileExistsError:
            pass


class GabApp(App):
    use_kivy_settings = False
    Config.set('kivy', 'exit_on_escape', '0')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    def build(self):
        self.sm = ScreenManager()
        self.main = MainWidget(name='main')
        self.nos = NosWidget(name='nos')
        self.sm.add_widget(self.nos)
        self.sm.add_widget(self.main)
        self.title = 'PIEG'
        self.icon = 'data/pieg.png'
        return self.sm


if __name__ == '__main__':
    kivy.resources.resource_add_path(resourcePath())
    GabApp().run()
