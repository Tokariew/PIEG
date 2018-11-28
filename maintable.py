import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import figaspect

# will provide scientific notation for big numbers


# todo add to all analise function boundry for columns, it will fail otherwise on last and first columns
# todo division by zero!
# todo write special formulas from gabar
# todo stop comparing to zero…

class MainTable:
    ind = ['f', 'd', 'H', 'alpha', 'V', 'L', 'Y', 'Beta', 'Q', 'T', 'phi', 'vignette', 'lhi']

    def __init__(self, columns):
        """main data structure for code. Table is already preformat, to blank spaces are blank, like in original"""
        self.columns = columns
        self.table = pd.DataFrame(index=MainTable.ind, columns=list(range(self.columns)), dtype=np.float64)
        tab = self.table
        tab.loc['f', 0] = ''
        tab.loc['V':'L', 0] = ''
        tab.loc['Q':'phi', 0] = ''
        tab.loc['f':'d', self.columns - 1] = ''
        tab.loc['alpha':'L', self.columns - 1] = ''
        tab.loc['Beta':'phi', self.columns - 1] = ''
        self.magnify = []
        self.LHI = np.nan
        self.vignette = np.nan
        self.prev_tables = []

    def change_value(self, row, column, value, func=0):
        tab = self.table
        if np.isnan(value):
            print('A ty co robisz, czemu mi sie buntuje', row, column)
            value = 0
        if func == 0:
            self.prev_tables.append(tab.copy(True))
            print('appending with:', row, column)
        if row in MainTable.ind:
            if np.isnan(tab.loc[row, column]):
                tab.at[row, column] = value
                print('{}{} is now {} from {}'.format(row, column, value, func))
                self.analise_input(row, column)

    def undo_changes(self):
        self.table = self.prev_tables.pop()
        self.vignette = self.table.loc['vignette', 0]
        self.LHI = self.table.loc['lhi', 0]

    def magnification(self, from_col, to_col, magn, var):
        if from_col > to_col:
            from_col, to_col = to_col, from_col
        if to_col >= self.columns:
            raise ValueError()
        else:
            for item in self.magnify:
                if from_col == item['from'] and to_col == item['to']:
                    return
            self.magnify.append({'from': from_col, 'to': to_col, 'magn': magn, 'type': var})

    def iterate(self, row, col, from_col, to_col, var, target_dimension, start_value):
        tab = self.table
        if not np.isnan(tab.loc[row, col]):
            return

    def change_lhi(self, value, func=0):
        if np.isnan(self.LHI):
            self.LHI = value
            self.table.loc['lhi', 0] = self.LHI
            print('LHI is now {} from {}'.format(value, func))
            self.check_lhi_function()

    def set_vignetting(self, value):
        if np.isnan(self.vignette):
            self.prev_tables.append(self.table.copy(True))
            self.vignette = float(value)
            for i in range(self.columns):
                self.table.loc['vignette', i] = self.vignette
                self.analyse1(i)
            print('Współczynnik winietowania is now {}'.format(value))

    def analise_input(self, row, column):
        if row == MainTable.ind[0]:
            self.check_f_function(column)
        elif row == MainTable.ind[1]:
            self.check_d_function(column)
        elif row == MainTable.ind[2]:
            self.check_h_function(column)
        elif row == MainTable.ind[3]:
            self.check_alpha_function(column)
        elif row == MainTable.ind[4]:
            self.check_v_function(column)
        elif row == MainTable.ind[5]:
            self.check_l_function(column)
        elif row == MainTable.ind[6]:
            self.check_y_function(column)
        elif row == MainTable.ind[7]:
            self.check_beta_function(column)
        elif row == MainTable.ind[8]:
            self.check_q_function(column)
        elif row == MainTable.ind[9]:
            self.check_t_function(column)
        if len(self.magnify) > 0:
            for i, elem in enumerate(self.magnify):
                from_col, to_col = elem['from'], elem['to']
                if elem['type'] == 'V':
                    if not np.all([np.isnan(self.table.loc['alpha', from_col]), np.isnan(self.table.loc['alpha', to_col])]):
                        self.analyse44(i)
                elif elem['type'] == 'Q':
                    if not np.all([np.isnan(self.table.loc['Beta', from_col]), np.isnan(self.table.loc['Beta', to_col])]):
                        self.analyse45(i)

        self.check_lhi_function()

    def check_f_function(self, column):
        self.analyse15(column)
        self.analyse16(column)
        self.analyse17(column)
        self.analyse22(column)
        self.analyse23(column)
        self.analyse24(column)
        self.analyse42(column)

    def check_d_function(self, column):
        self.analyse20(column)
        self.analyse27(column)
        self.analyse43(column)

    def check_h_function(self, column):
        self.analyse1(column)
        self.analyse15(column)
        self.analyse16(column)
        self.analyse18(column)
        self.analyse19(column)
        self.analyse20(column)
        self.analyse20(column - 1)
        self.analyse36(column)
        self.analyse37(column)
        self.analyse39(column)
        self.analyse41(column)
        self.analyse43(column)
        self.analyse43(column - 1)

    def check_alpha_function(self, column):
        # todo add calculation based on magnification between any to columns
        self.analyse14(column)
        self.analyse14(column + 1)  # we have more two alphas in here, one which is in previous column
        self.analyse15(column)
        self.analyse15(column + 1)
        self.analyse16(column)
        self.analyse18(column)
        self.analyse18(column + 1)
        self.analyse19(column + 1)
        self.analyse20(column)
        self.analyse36(column)
        self.analyse37(column + 1)
        self.analyse40(column)
        self.analyse42(column + 1)

    def check_v_function(self, column):
        self.analyse14(column)
        self.analyse16(column)
        self.analyse17(column)
        self.analyse19(column)
        self.analyse39(column)
        self.analyse40(column)
        self.analyse41(column)

    def check_l_function(self, column):
        self.analyse17(column)
        self.analyse18(column)
        self.analyse19(column)

    def check_y_function(self, column):
        self.analyse1(column)
        self.analyse22(column)
        self.analyse23(column)
        self.analyse25(column)
        self.analyse26(column)
        self.analyse27(column)
        self.analyse27(column - 1)
        self.analyse36(column)
        self.analyse37(column)
        self.analyse40(column + 1)
        self.analyse43(column)
        self.analyse43(column - 1)

    def check_beta_function(self, column):
        # todo magnify option between betas to write
        self.analyse21(column)
        self.analyse21(column + 1)
        self.analyse22(column)
        self.analyse22(column + 1)
        self.analyse23(column)
        self.analyse25(column)
        self.analyse25(column + 1)
        self.analyse26(column + 1)
        self.analyse27(column)
        self.analyse36(column)
        self.analyse37(column + 1)
        self.analyse39(column)
        self.analyse41(column + 1)
        self.analyse42(column)
        self.analyse42(column + 1)

    def check_q_function(self, column):
        self.analyse21(column)
        self.analyse24(column)

    def check_t_function(self, column):
        # deleted two function, they didn't have a T term, so it will be run from some other place.
        self.analyse24(column)
        self.analyse25(column)
        self.analyse26(column)

    def check_lhi_function(self):
        if not np.isnan(self.LHI):
            for i in range(0, self.columns):
                self.analyse36(i)
                self.analyse37(i)
                self.analyse39(i)
                self.analyse40(i)
                self.analyse41(i)
                self.analyse42(i)
                self.analyse43(i)

    def analyse1(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([self.vignette, tab.loc['H', c], tab.loc['Y', c]])):
                a = 2 * np.abs(tab.loc['H', c])
                b = 2 * (np.abs(tab.loc['Y', c]) + self.vignette * np.abs(tab.loc['H', c]))
                val = np.max([a, b])
                self.change_value('phi', c, val, 1)

    def analyse14(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['alpha', c]])):
                val = tab.loc['V', c] * tab.loc['alpha', c]
                self.change_value('alpha', c - 1, val, 14)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['V', c]])) and tab.loc['V', c] != 0:
                val = tab.loc['alpha', c - 1] / tab.loc['V', c]
                self.change_value('alpha', c, val, 14)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['alpha', c]])) and tab.loc['alpha', c] != 0:
                val = tab.loc['alpha', c - 1] / tab.loc['alpha', c]
                self.change_value('V', c, val, 14)

    def analyse15(self, column):
        tab = self.table
        c = column
        if 1 <= c <= column - 2:
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['H', c], tab.loc['f', c]])) and \
                    tab.loc['f', c] != 0:
                val = tab.loc['alpha', c - 1] + tab.loc['H', c] / tab.loc['f', c]
                self.change_value('alpha', c, val, 15)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['H', c], tab.loc['f', c]])) and tab.loc['f', c] != 0:
                val = tab.loc['alpha', c] - tab.loc['H', c] / tab.loc['f', c]
                self.change_value('alpha', c - 1, val, 15)
            if not np.any(np.isnan([tab.loc['f', c], tab.loc['alpha', c], tab.loc['alpha', c - 1]])):
                val = tab.loc['f', c] * (tab.loc['alpha', c] - tab.loc['alpha', c - 1])
                self.change_value('H', c, val, 15)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['alpha', c - 1], tab.loc['H', c]])) and (
                    tab.loc['alpha', c] - tab.loc['alpha', c - 1]) != 0:
                val = tab.loc['H', c] / (tab.loc['alpha', c] - tab.loc['alpha', c - 1])
                self.change_value('f', c, val, 15)

    def analyse16(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['H', c], tab.loc['f', c]])) and (
                    tab.loc['f', c] * (1 - tab.loc['V', c])) != 0:
                val = - tab.loc['H', c] / (tab.loc['f', c] * (tab.loc['V', c] - 1))
                self.change_value('alpha', c, val, 16)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['H', c], tab.loc['f', c]])) and (
                    tab.loc['alpha', c] * tab.loc['f', c]) != 0:
                val = 1 - tab.loc['H', c] / (tab.loc['f', c] * tab.loc['alpha', c])
                self.change_value('V', c, val, 16)
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['alpha', c], tab.loc['f', c]])):
                val = tab.loc['alpha', c] * tab.loc['f', c] * (1 - tab.loc['V', c])
                self.change_value('H', c, val, 16)
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['H', c], tab.loc['alpha', c]])) and (
                    tab.loc['alpha', c] * (1 - tab.loc['V', c])) != 0:
                val = tab.loc['H', c] / (tab.loc['alpha', c] * (1 - tab.loc['V', c]))
                self.change_value('f', c, val, 16)

    def analyse17(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['f', c]])) and tab.loc['V', c] != 0:
                val = - (tab.loc['f', c] * (1 - tab.loc['V', c]) ** 2) / tab.loc['V', c]
                self.change_value('L', c, val, 17)
            if not np.any(np.isnan([tab.loc['L', c], tab.loc['f', c]])) and (1 - tab.loc['V', c]) != 0:
                val = (-tab.loc['V', c] * tab.loc['L', c]) / (1 - tab.loc['V', c]) ** 2
                self.change_value('f', c, val, 17)

    def analyse18(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['H', c], tab.loc['L', c]])) and (
                    tab.loc['alpha', c - 1] * tab.loc['L', c] + tab.loc['H', c]) != 0:
                val = tab.loc['H', c] * tab.loc['alpha', c - 1] / (
                    tab.loc['alpha', c - 1] * tab.loc['L', c] + tab.loc['H', c])
                self.change_value('alpha', c, val, 18)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['H', c], tab.loc['L', c]])) and (
                    tab.loc['H', c] - tab.loc['alpha', c] * tab.loc['L', c]) != 0:
                val = tab.loc['H', c] * tab.loc['alpha', c] / (tab.loc['H', c] - tab.loc['alpha', c] * tab.loc['L', c])
                self.change_value('alpha', c - 1, val, 18)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['alpha', c], tab.loc['L', c]])) and (
                    tab.loc['alpha', c - 1] - tab.loc['alpha', c]) != 0:
                val = tab.loc['alpha', c] * tab.loc['alpha', c - 1] * tab.loc['L', c] / (
                    tab.loc['alpha', c - 1] - tab.loc['alpha', c])
                self.change_value('H', c, val, 18)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['H', c], tab.loc['alpha', c]])) and (
                    tab.loc['alpha', c - 1] * tab.loc['alpha', c]) != 0:
                val = tab.loc['H', c] * (tab.loc['alpha', c - 1] - tab.loc['alpha', c]) / (
                    tab.loc['alpha', c - 1] * tab.loc['alpha', c])
                self.change_value('L', c, val, 18)

    def analyse19(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['V', c], tab.loc['L', c]])) and tab.loc['L', c] != 0:
                val = tab.loc['H', c] * (tab.loc['V', c] - 1) / tab.loc['L', c]
                self.change_value('alpha', c - 1, val, 19)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['V', c], tab.loc['alpha', c - 1]])) and \
                    tab.loc['alpha', c - 1] != 0:
                val = tab.loc['H', c] * (tab.loc['V', c] - 1) / tab.loc['alpha', c - 1]
                self.change_value('L', c, val, 19)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['V', c], tab.loc['L', c]])) and (
                    1 - tab.loc['V', c]) != 0:
                val = tab.loc['alpha', c - 1] * tab.loc['L', c] / (tab.loc['V', c] - 1)
                self.change_value('H', c, val, 19)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['alpha', c - 1], tab.loc['L', c]])) and \
                    tab.loc['H', c] != 0:
                val = (tab.loc['alpha', c - 1] * tab.loc['L', c] + tab.loc['H', c]) / tab.loc['H', c]
                self.change_value('V', c, val, 19)

    def analyse20(self, column):
        tab = self.table
        c = column
        if self.columns - 2 >= c >= 0:
            if not np.any(np.isnan([tab.loc['H', c + 1], tab.loc['alpha', c], tab.loc['d', c]])):
                val = tab.loc['H', c + 1] + tab.loc['alpha', c] * tab.loc['d', c]
                self.change_value('H', c, val, 20)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['alpha', c], tab.loc['d', c]])):
                val = tab.loc['H', c] - tab.loc['alpha', c] * tab.loc['d', c]
                self.change_value('H', c + 1, val, 20)
            if not np.any(np.isnan([tab.loc['H', c + 1], tab.loc['H', c], tab.loc['d', c]])) and tab.loc['d', c] != 0:
                val = (tab.loc['H', c] - tab.loc['H', c + 1]) / tab.loc['d', c]
                self.change_value('alpha', c, val, 20)
            if not np.any(np.isnan([tab.loc['H', c + 1], tab.loc['alpha', c], tab.loc['H', c]])) and \
                    tab.loc['alpha', c] != 0:
                val = (tab.loc['H', c] - tab.loc['H', c + 1]) / tab.loc['alpha', c]
                self.change_value('d', c, val, 20)

    def analyse21(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Q', c]])):
                val = tab.loc['Beta', c] * tab.loc['Q', c]
                self.change_value('Beta', c - 1, val, 21)
            if not np.any(np.isnan([tab.loc['Beta', c - 1], tab.loc['Q', c]])) and tab.loc['Q', c] != 0:
                val = tab.loc['Beta', c - 1] / tab.loc['Q', c]
                self.change_value('Beta', c, val, 21)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Beta', c - 1]])) and tab.loc['Beta', c] != 0:
                val = tab.loc['Beta', c - 1] / tab.loc['Beta', c]
                self.change_value('Q', c, val, 21)

    def analyse22(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Y', c], tab.loc['f', c]])) and tab.loc['f', c] != 0:
                val = tab.loc['Beta', c] - tab.loc['Y', c] / tab.loc['f', c]
                self.change_value('Beta', c - 1, val, 22)
            if not np.any(np.isnan([tab.loc['Beta', c - 1], tab.loc['Y', c], tab.loc['f', c]])) and \
                    tab.loc['f', c] != 0:
                val = tab.loc['Beta', c - 1] + tab.loc['Y', c] / tab.loc['f', c]
                self.change_value('Beta', c, val, 22)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Y', c], tab.loc['f', c]])):
                val = tab.loc['f', c] * (tab.loc['Beta', c] - tab.loc['Beta', c - 1])
                self.change_value('Y', c, val, 22)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Y', c], tab.loc['Beta', c - 1]])) and (
                    tab.loc['Beta', c] - tab.loc['Beta', c - 1]) != 0:
                val = tab.loc['Y', c] / (tab.loc['Beta', c] - tab.loc['Beta', c - 1])
                self.change_value('f', c, val, 22)

    def analyse23(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Q', c], tab.loc['Y', c], tab.loc['f', c]])) and (
                    tab.loc['f', c] * (1 - tab.loc['Q', c])) != 0:
                val = tab.loc['Y', c] / (tab.loc['f', c] * (1 - tab.loc['Q', c]))
                self.change_value('Beta', c, val, 23)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Y', c], tab.loc['f', c]])):
                if (tab.loc['Beta', c] * tab.loc['f', c]) != 0:
                    val = 1 - (tab.loc['Y', c]) / (tab.loc['f', c] * tab.loc['Beta', c])
                    self.change_value('Q', c, val, 23)
            if not np.any(np.isnan([tab.loc['Q', c], tab.loc['Beta', c], tab.loc['f', c]])):
                val = tab.loc['f', c] * tab.loc['Beta', c] * (1 - tab.loc['Q', c])
                self.change_value('Y', c, val, 23)
            if not np.any(np.isnan([tab.loc['Q', c], tab.loc['Y', c], tab.loc['Beta', c]])) and (
                    tab.loc['Beta', c] * (1 - tab.loc['Q', c])) != 0:
                val = tab.loc['Y', c] / (tab.loc['Beta', c] * (1 - tab.loc['Q', c]))
                self.change_value('f', c, val, 23)

    def analyse24(self, column):
        tab = self.table
        c = column
        if not np.any(np.isnan([tab.loc['f', c], tab.loc['Q', c]])) and tab.loc['Q', c] != 0:
            val = (-tab.loc['f', c] * (1 - tab.loc['Q', c]) ** 2) / tab.loc['Q', c]
            self.change_value('T', c, val, 24)
        if not np.any(np.isnan([tab.loc['T', c], tab.loc['Q', c]])) and (1 - tab.loc['Q', c]) != 0:
            val = -tab.loc['Q', c] * tab.loc['T', c] / (1 - tab.loc['Q', c]) ** 2
            self.change_value('f', c, val, 24)

    def analyse25(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['T', c], tab.loc['Y', c]])) and (
                    tab.loc['Y', c] - tab.loc['Beta', c] * tab.loc['T', c]) != 0:
                val = tab.loc['Y', c] * tab.loc['Beta', c] / (
                    tab.loc['Y', c] - tab.loc['Beta', c] * tab.loc['T', c])
                self.change_value('Beta', c - 1, val, 25)
            if not np.any(np.isnan([tab.loc['Beta', c - 1], tab.loc['T', c], tab.loc['Y', c]])) and (
                    tab.loc['Beta', c - 1] * tab.loc['T', c] + tab.loc['Y', c]) != 0:
                val = tab.loc['Y', c] * tab.loc['Beta', c - 1] / (
                    tab.loc['Beta', c - 1] * tab.loc['T', c] + tab.loc['Y', c])
                self.change_value('Beta', c, val, 25)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['Y', c]])) and (
                    tab.loc['Beta', c] * tab.loc['Beta', c - 1]) != 0:
                val = tab.loc['Y', c] * (tab.loc['Beta', c - 1] - tab.loc['Beta', c]) / (
                    tab.loc['Beta', c] * tab.loc['Beta', c - 1])
                self.change_value('T', c, val, 25)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['T', c], tab.loc['Beta', c - 1]])) and (
                    tab.loc['Beta', c - 1] - tab.loc['Beta', c]) != 0:
                val = tab.loc['Beta', c] * tab.loc['Beta', c - 1] * tab.loc['T', c] / (
                    tab.loc['Beta', c - 1] - tab.loc['Beta', c])
                self.change_value('Y', c, val, 25)

    def analyse26(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['T', c], tab.loc['Q', c]])) and tab.loc['T', c] != 0:
                val = tab.loc['Y', c] * (tab.loc['Q', c] - 1) / tab.loc['T', c]
                self.change_value('Beta', c - 1, val, 26)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['T', c], tab.loc['Q', c]])) and \
                    tab.loc['Beta', c - 1] != 0:
                val = tab.loc['Y', c] * (tab.loc['Q', c] - 1) / tab.loc['Beta', c - 1]
                self.change_value('T', c, val, 26)
            if not np.any(np.isnan([tab.loc['Beta', c - 1], tab.loc['T', c], tab.loc['Q', c]])) and \
                    (1 - tab.loc['Q', c]) != 0:
                val = tab.loc['Beta', c - 1] * tab.loc['T', c] / (tab.loc['Q', c] - 1)
                self.change_value('Y', c, val, 26)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['T', c], tab.loc['Beta', c - 1]])) and \
                    tab.loc['Y', c] != 0:
                val = 1 + tab.loc['Beta', c - 1] * tab.loc['T', c] / tab.loc['Y', c]
                self.change_value('Q', c, val, 26)

    def analyse27(self, column):
        tab = self.table
        c = column
        if self.columns - 2 >= c >= 0:
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['Beta', c], tab.loc['d', c]])):
                val = tab.loc['Y', c] - tab.loc['Beta', c] * tab.loc['d', c]
                self.change_value('Y', c + 1, val, 27)
            if not np.any(np.isnan([tab.loc['Y', c + 1], tab.loc['Beta', c], tab.loc['d', c]])):
                val = tab.loc['Y', c + 1] + tab.loc['Beta', c] * tab.loc['d', c]
                self.change_value('Y', c, val, 27)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['Y', c + 1], tab.loc['d', c]])) and tab.loc['d', c] != 0:
                val = (tab.loc['Y', c] - tab.loc['Y', c + 1]) / tab.loc['d', c]
                self.change_value('Beta', c, val, 27)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['Beta', c], tab.loc['Y', c + 1]])) and \
                    tab.loc['Beta', c] != 0:
                val = (tab.loc['Y', c] - tab.loc['Y', c + 1]) / tab.loc['Beta', c]
                self.change_value('d', c, val, 27)

    def analyse36(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if self.columns - 2 > c:
            # normals
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['Y', c], tab.loc['Beta', c], lhi])) and tab.loc[
                    'Beta', c] != 0:
                val = (tab.loc['alpha', c] * tab.loc['Y', c] - lhi) / tab.loc['Beta', c]
                self.change_value('H', c, val, 36)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['H', c], tab.loc['Beta', c], lhi])) and tab.loc[
                    'alpha', c] != 0:
                val = (tab.loc['H', c] * tab.loc['Beta', c] + lhi) / tab.loc['alpha', c]
                self.change_value('Y', c, val, 36)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['Y', c], tab.loc['H', c], lhi])) and tab.loc[
                    'H', c] != 0:
                val = (tab.loc['alpha', c] * tab.loc['Y', c] - lhi) / tab.loc['H', c]
                self.change_value('Beta', c, val, 36)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['Y', c], tab.loc['Beta', c], lhi])) and tab.loc[
                    'Y', c] != 0:
                val = (tab.loc['H', c] * tab.loc['Beta', c] + lhi) / tab.loc['Y', c]
                self.change_value('alpha', c, val, 36)
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['Y', c], tab.loc['Beta', c], tab.loc['H', c]])):
                val = tab.loc['alpha', c] * tab.loc['Y', c] - tab.loc['H', c] * tab.loc['Beta', c]
                self.change_lhi(val)
            # specials
            if not np.any(np.isnan([tab.loc['Beta', c], lhi])):
                if tab.loc['Beta', c] != 0 and (tab.loc['Y', c] == 0 or tab.loc['alpha', c] == 0):
                    val = - lhi / tab.loc['Beta', c]
                    self.change_value('H', c, val, '36s')
            if not np.any(np.isnan([lhi, tab.loc['alpha', c]])):
                if tab.loc['alpha', c] != 0 and (tab.loc['H', c] == 0 or tab.loc['Beta', c] == 0):
                    val = lhi / tab.loc['alpha', c]
                    self.change_value('Y', c, val, '36s')
            if not np.any(np.isnan([tab.loc['H', c], lhi])):
                if tab.loc['H', c] != 0 and (tab.loc['Y', c] == 0 or tab.loc['alpha', c] == 0):
                    val = -lhi / tab.loc['H', c]
                    self.change_value('Beta', c, val, '36s')
            if not np.any(np.isnan([lhi, tab.loc['Y', c]])):
                if tab.loc['Y', c] != 0 and (tab.loc['H', c] == 0 or tab.loc['Beta', c] == 0):
                    val = lhi / tab.loc['Y', c]
                    self.change_value('alpha', c, val, '36s')
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['Beta', c]])):
                if tab.loc['Y', c] == 0 or tab.loc['alpha', c] == 0:
                    val = - tab.loc['H', c] * tab.loc['Beta', c]
                    self.change_lhi(val, '36s1')
            if not np.any(np.isnan([tab.loc['alpha', c], tab.loc['Y', c]])):
                if tab.loc['H', c] == 0 or tab.loc['Beta', c] == 0:
                    val = tab.loc['alpha', c] * tab.loc['Y', c]
                    self.change_lhi(val, '36s2')

    def analyse37(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if c >= 1:
            # normal
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['Y', c], tab.loc['Beta', c - 1], lhi])) and \
                    tab.loc['Beta', c - 1] != 0:
                val = (tab.loc['alpha', c - 1] * tab.loc['Y', c] - lhi) / tab.loc['Beta', c - 1]
                self.change_value('H', c, val, 37)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['H', c], tab.loc['Beta', c - 1], lhi])) and \
                    tab.loc['alpha', c - 1] != 0:
                val = (tab.loc['H', c] * tab.loc['Beta', c - 1] + lhi) / tab.loc['alpha', c - 1]
                self.change_value('Y', c, val, 37)
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['Y', c], tab.loc['H', c], lhi])) and \
                    tab.loc['H', c] != 0:
                val = (tab.loc['alpha', c - 1] * tab.loc['Y', c] - lhi) / tab.loc['H', c]
                self.change_value('Beta', c - 1, val, 37)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['Y', c], tab.loc['Beta', c - 1], lhi])) and \
                    tab.loc['Y', c] != 0:
                val = (tab.loc['H', c] * tab.loc['Beta', c - 1] + lhi) / tab.loc['Y', c]
                self.change_value('alpha', c - 1, val, 37)
            if not np.any(
                    np.isnan([tab.loc['alpha', c - 1], tab.loc['Y', c], tab.loc['Beta', c - 1], tab.loc['H', c]])):
                val = tab.loc['alpha', c - 1] * tab.loc['Y', c] - tab.loc['H', c] * tab.loc['Beta', c - 1]
                self.change_lhi(val)
            # special
            if not np.any(np.isnan([tab.loc['Beta', c - 1], lhi])):
                if tab.loc['Beta', c - 1] != 0 and (tab.loc['Y', c] == 0 or tab.loc['alpha', c - 1] == 0):
                    val = - lhi / tab.loc['Beta', c - 1]
                    self.change_value('H', c, val, '37s')
            if not np.any(np.isnan([lhi, tab.loc['alpha', c - 1]])):
                if tab.loc['alpha', c - 1] != 0 and (tab.loc['H', c] == 0 or tab.loc['Beta', c - 1] == 0):
                    val = lhi / tab.loc['alpha', c - 1]
                    self.change_value('Y', c, val, '37s')
            if not np.any(np.isnan([tab.loc['H', c], lhi])):
                if tab.loc['H', c] != 0 and (tab.loc['Y', c] == 0 or tab.loc['alpha', c - 1] == 0):
                    val = -lhi / tab.loc['H', c]
                    self.change_value('Beta', c - 1, val, '37s')
            if not np.any(np.isnan([lhi, tab.loc['Y', c]])):
                if tab.loc['Y', c] != 0 and (tab.loc['H', c] == 0 or tab.loc['Beta', c - 1] == 0):
                    val = lhi / tab.loc['Y', c]
                    self.change_value('alpha', c - 1, val, '37s')
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['Beta', c - 1]])):
                if tab.loc['Y', c] == 0 or tab.loc['alpha', c - 1] == 0:
                    val = - tab.loc['H', c] * tab.loc['Beta', c - 1]
                    self.change_lhi(val, '37s1')
            if not np.any(np.isnan([tab.loc['alpha', c - 1], tab.loc['Y', c]])):
                if tab.loc['H', c] == 0 or tab.loc['Beta', c - 1] == 0:
                    val = tab.loc['alpha', c - 1] * tab.loc['Y', c]
                    self.change_lhi(val, '37s2')

    def analyse39(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if 0 < c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['V', c], tab.loc['Q', c], lhi])) and (
                    tab.loc['Beta', c] * (tab.loc['Q', c] - tab.loc['V', c])) != 0:
                val = lhi * (1 - tab.loc['V', c]) / (tab.loc['Beta', c] * (tab.loc['Q', c] - tab.loc['V', c]))
                self.change_value('H', c, val, 39)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['H', c], tab.loc['Q', c], lhi])) and (
                    tab.loc['Beta', c] * tab.loc['H', c] - lhi) != 0:
                val = (tab.loc['Beta', c] * tab.loc['H', c] * tab.loc['Q', c] - lhi) / (
                    tab.loc['Beta', c] * tab.loc['H', c] - lhi)
                self.change_value('V', c, val, 39)
            if not np.any(np.isnan([tab.loc['Beta', c], tab.loc['H', c], tab.loc['V', c], lhi])) and (
                    tab.loc['Beta', c] * tab.loc['H', c]) != 0:
                val = (tab.loc['Beta', c] * tab.loc['H', c] * tab.loc['V', c] - lhi * (tab.loc['V', c] - 1)) / (
                    tab.loc['Beta', c] * tab.loc['H', c])
                self.change_value('Q', c, val, 39)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['V', c], tab.loc['Q', c], lhi])) and (
                    tab.loc['H', c] * (tab.loc['Q', c] - tab.loc['V', c])) != 0:
                val = (lhi * (1 - tab.loc['V', c])) / (tab.loc['H', c] * (tab.loc['Q', c] - tab.loc['V', c]))
                self.change_value('Beta', c, val, 39)
            if not np.any(np.isnan([tab.loc['H', c], tab.loc['V', c], tab.loc['Q', c], tab.loc['Beta', c]])) and (
                    tab.loc['V', c] - 1) != 0:
                val = (tab.loc['Beta', c] * tab.loc['H', c] * (tab.loc['V', c] - tab.loc['Q', c])) / (
                    tab.loc['V', c] - 1)
                self.change_lhi(val)

    def analyse40(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if 0 < c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['alpha', c - 1], tab.loc['Q', c], lhi])) and (
                    lhi * (tab.loc['Q', c] - 1) + tab.loc['alpha', c - 1] * tab.loc['Y', c]) != 0:
                val = tab.loc['alpha', c - 1] * tab.loc['Y', c] * tab.loc['Q', c] / (
                    lhi * (tab.loc['Q', c] - 1) + tab.loc['alpha', c - 1] * tab.loc['Y', c])
                self.change_value('V', c, val, 40)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['alpha', c - 1], tab.loc['V', c], lhi])) and (
                    tab.loc['alpha', c - 1] * tab.loc['Y', c] - lhi * tab.loc['V', c]) != 0:
                val = tab.loc['V', c] * (lhi - tab.loc['alpha', c - 1] * tab.loc['Y', c]) / (
                    lhi * tab.loc['V', c] - tab.loc['alpha', c - 1] * tab.loc['Y', c])
                self.change_value('Q', c, val, 40)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['V', c], tab.loc['Q', c], lhi])) and \
                    tab.loc['Y', c] * (tab.loc['V', c] - tab.loc['Q', c]) != 0:
                val = tab.loc['V', c] * lhi * (1 - tab.loc['Q', c]) / (
                    tab.loc['Y', c] * (tab.loc['V', c] - tab.loc['Q', c]))
                self.change_value('alpha', c, val, 40)
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['alpha', c - 1], tab.loc['Q', c], lhi])) and \
                    tab.loc['alpha', c - 1] * (tab.loc['V', c] - tab.loc['Q', c]) != 0:
                val = tab.loc['V', c] * lhi * (1 - tab.loc['Q', c]) / (
                    tab.loc['alpha', c - 1] * (tab.loc['V', c] - tab.loc['Q', c]))
                self.change_value('Y', c, val, 40)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['alpha', c - 1], tab.loc['Q', c], tab.loc['V', c]])) and (
                    tab.loc['V', c] * (1 - tab.loc['Q', c])) != 0:
                val = tab.loc['alpha', c - 1] * tab.loc['Y', c] * (tab.loc['V', c] - tab.loc['Q', c]) / (
                    tab.loc['V', c] * (1 - tab.loc['Q', c]))
                self.change_lhi(val)

    def analyse41(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if 1 <= c <= self.columns - 2:
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['Beta', c - 1], tab.loc['H', c], lhi])) and (
                    lhi * (1 - tab.loc['V', c]) + tab.loc['Beta', c - 1] * tab.loc['H', c]) != 0:
                val = tab.loc['Beta', c - 1] * tab.loc['H', c] * tab.loc['V', c] / (
                    lhi * (1 - tab.loc['V', c]) + tab.loc['Beta', c - 1] * tab.loc['H', c])
                self.change_value('Q', c, val, 41)
            if not np.any(np.isnan([tab.loc['Q', c], tab.loc['Beta', c - 1], tab.loc['H', c], lhi])) and (
                    tab.loc['Beta', c - 1] * tab.loc['H', c] + tab.loc['Q', c] * lhi) != 0:
                val = tab.loc['Q', c] * (tab.loc['Beta', c - 1] * tab.loc['H', c] + lhi) / (
                    tab.loc['Beta', c - 1] * tab.loc['H', c] + tab.loc['Q', c] * lhi)
                self.change_value('V', c, val, 41)
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['Q', c], tab.loc['H', c], lhi])) and (
                    tab.loc['H', c] * (tab.loc['V', c] - tab.loc['Q', c])) != 0:
                val = tab.loc['Q', c] * lhi * (1 - tab.loc['V', c]) / (
                    tab.loc['H', c] * (tab.loc['V', c] - tab.loc['Q', c]))
                self.change_value('Beta', c - 1, val, 41)
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['Beta', c - 1], tab.loc['Q', c], lhi])) and (
                    tab.loc['Beta', c - 1] * (tab.loc['V', c] - tab.loc['Q', c])) != 0:
                val = tab.loc['Q', c] * lhi * (1 - tab.loc['V', c]) / (
                    tab.loc['Beta', c - 1] * (tab.loc['V', c] - tab.loc['Q', c]))
                self.change_value('H', c, val, 41)
            if not np.any(np.isnan([tab.loc['V', c], tab.loc['Beta', c - 1], tab.loc['H', c], tab.loc['Q', c]])) and (
                    tab.loc['Q', c] * (tab.loc['V', c] - 1)) != 0:
                val = tab.loc['Beta', c - 1] * tab.loc['H', c] * (tab.loc['Q', c] - tab.loc['V', c]) / (
                    tab.loc['Q', c] * (tab.loc['V', c] - 1))
                self.change_value('Q', c, val, 41)

    def analyse42(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if 1 <= c <= self.columns - 2:
            if not np.any(
                    np.isnan(
                        [tab.loc['alpha', c - 1], tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['f', c],
                         lhi])) and (tab.loc['f', c] * tab.loc['Beta', c - 1]) != 0:
                val = (tab.loc['alpha', c - 1] * tab.loc['Beta', c] * tab.loc['f', c] - lhi) / (
                    tab.loc['f', c] * tab.loc['Beta', c - 1])
                self.change_value('alpha', c, val, 42)
            if not np.any(
                np.isnan(
                    [tab.loc['alpha', c], tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['f', c], lhi])) and (
                    tab.loc['f', c] * tab.loc['Beta', c]) != 0:
                val = (tab.loc['alpha', c] * tab.loc['Beta', c - 1] * tab.loc['f', c] + lhi) / (
                    tab.loc['f', c] * tab.loc['Beta', c])
                self.change_value('alpha', c - 1, val, 42)
            if not np.any(
                    np.isnan(
                        [tab.loc['alpha', c - 1], tab.loc['alpha', c], tab.loc['Beta', c - 1], tab.loc['f', c],
                         lhi])) and (tab.loc['f', c] * tab.loc['alpha', c - 1]) != 0:
                val = (tab.loc['alpha', c] * tab.loc['Beta', c - 1] * tab.loc['f', c] + lhi) / (
                    tab.loc['f', c] * tab.loc['alpha', c - 1])
                self.change_value('Beta', c, val, 42)
            if not np.any(
                    np.isnan(
                        [tab.loc['alpha', c - 1], tab.loc['alpha', c], tab.loc['Beta', c - 1], tab.loc['f', c],
                         lhi])) and (tab.loc['f', c] * tab.loc['alpha', c]) != 0:
                val = (tab.loc['alpha', c - 1] * tab.loc['Beta', c] * tab.loc['f', c] - lhi) / (
                    tab.loc['f', c] * tab.loc['alpha', c])
                self.change_value('Beta', c - 1, val, 42)
            if not np.any(
                    np.isnan(
                        [tab.loc['alpha', c - 1], tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['f', c], lhi])):
                if (tab.loc['alpha', c] * tab.loc['Beta', c - 1] - tab.loc['alpha', c - 1] * tab.loc['Beta', c]) != 0:
                    val = lhi / (
                        tab.loc['alpha', c - 1] * tab.loc['Beta', c] - tab.loc['alpha', c] * tab.loc['Beta', c - 1])
                    self.change_value('f', c, val, 42)
            if not np.any(
                    np.isnan([tab.loc['alpha', c - 1], tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['f', c],
                              tab.loc['alpha', c]])):
                val = tab.loc['f', c] * (tab.loc['alpha', c - 1] * tab.loc['Beta', c] - tab.loc['alpha', c] * tab.loc[
                    'Beta', c - 1])
                self.change_lhi(val)

    def analyse43(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if self.columns - 2 >= c >= 0:
            """check h"""
            if not np.any(
                    np.isnan([tab.loc['Y', c], tab.loc['Y', c + 1], tab.loc['H', c + 1], tab.loc['d', c], lhi])) and \
                    tab.loc['Y', c + 1] != 0:
                val = (tab.loc['H', c + 1] * tab.loc['Y', c] + lhi * tab.loc['d', c]) / tab.loc['Y', c + 1]
                self.change_value('H', c, val, 43)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['Y', c + 1], tab.loc['H', c], tab.loc['d', c], lhi])) and \
                    tab.loc['Y', c] != 0:
                val = (tab.loc['H', c] * tab.loc['Y', c + 1] + lhi * tab.loc['d', c]) / tab.loc['Y', c]
                self.change_value('H', c + 1, val, 43)
            """check y"""
            if not np.any(
                    np.isnan([tab.loc['H', c], tab.loc['Y', c + 1], tab.loc['H', c + 1], tab.loc['d', c], lhi])) and \
                    tab.loc['H', c + 1] != 0:
                val = (tab.loc['H', c] * tab.loc['Y', c + 1] - lhi * tab.loc['d', c]) / tab.loc['H', c + 1]
                self.change_value('Y', c, val, 43)
            if not np.any(np.isnan([tab.loc['Y', c], tab.loc['H', c], tab.loc['H', c + 1], tab.loc['d', c], lhi])) and \
                    tab.loc['H', c] != 0:
                val = (tab.loc['H', c + 1] * tab.loc['Y', c] + lhi * tab.loc['d', c]) / tab.loc['H', c]
                self.change_value('Y', c + 1, val, 43)
            """rest"""
            if not np.any(np.isnan(
                    [tab.loc['Y', c], tab.loc['Y', c + 1], tab.loc['H', c + 1], tab.loc['H', c], lhi])) and lhi != 0:
                val = (tab.loc['H', c] * tab.loc['Y', c + 1] - tab.loc['H', c + 1] * tab.loc['Y', c]) / lhi
                self.change_value('d', c, val, 43)
            if not np.any(np.isnan(
                    [tab.loc['Y', c], tab.loc['Y', c + 1], tab.loc['H', c], tab.loc['d', c], tab.loc['H', c + 1]])) and \
                    tab.loc['d', c] != 0:
                val = (tab.loc['H', c] * tab.loc['Y', c + 1] - tab.loc['H', c + 1] * tab.loc['Y', c]) / tab.loc['d', c]
                self.change_lhi(val)

    def analyse44(self, i):
        tab = self.table
        elem = self.magnify[i]
        c1 = elem['from']
        c2 = elem['to']
        if np.isnan(tab.loc['alpha', c1]):
            val = tab.loc['alpha', c2] * elem['magn']
            self.change_value('alpha', c1, val, 44)
            del self.magnify[i]
        elif np.isnan(tab.loc['alpha', c2]):
            val = tab.loc['alpha', c1] / elem['magn']
            self.change_value('alpha', c2, val, 44)
            del self.magnify[i]

    def analyse45(self, i):
        tab = self.table
        elem = self.magnify[i]
        c1 = elem['from']
        c2 = elem['to']
        if np.isnan(tab.loc['Beta', c1]):
            val = tab.loc['Beta', c2] * elem['magn']
            self.change_value('Beta', c1, val, 45)
            del self.magnify[i]
        elif np.isnan(tab.loc['Beta', c2]):
            val = tab.loc['Beta', c1] / elem['magn']
            self.change_value('Beta', c2, val, 45)
            del self.magnify[i]

    def plot(self):
        plt.close('all')
        y = list(self.table.loc['Y'])
        h = list(self.table.loc['H'])
        f = list(self.table.loc['f'])
        d = list(self.table.loc['d', 0:self.columns - 2])
        phi = list(self.table.loc['phi'])
        phi = [el if not el == '' else np.nan for el in phi]
        y_max = np.abs(y).max()
        h_max = np.abs(h).max()
        phi_max = np.nanmax(np.abs(phi))
        ax_max = np.max([y_max, h_max, phi_max])
        d1 = [0]
        for i, val in enumerate(d):
            d1.append(d1[i] + d[i])
        plt.plot(d1, h, label='h')
        plt.plot(d1, y, label='y', color='r')
        plt.legend()
        plt.axhline(y=0, xmin=d1[0], xmax=d1[-1], linestyle='-.', color='k')
        fig = plt.gcf()
        ax = plt.gca()
        for i, k, f in zip(d1[1:-1], phi[1:-1], f[1:-1]):
            fb = 1 / f
            if np.isclose(fb, 0):
                self.draw_stop(i, k, ax)
            elif fb > 0:
                self.draw_plus(i, k, ax)
            else:
                self.draw_minus(i, k, ax)
        plt.ylim(-ax_max, ax_max)
        plt.xlim(-1, d[-1] + 1)
        ax.set_aspect('equal')
        a = 2 * ax_max
        b = d[-1] + 2
        c, d = figaspect(a / b)
        if np.max([c, d]) < 15:
            c, d = 2 * c, 2 * d
        fig.set_size_inches(c, d)
        plt.tight_layout()
        plt.savefig('test.png', dpi=300)
        plt.show()

    def draw_stop(self, x, y, ax):
        ax.plot((x, x), (y, y + 10), marker='_', markevery=2, color='k', markersize=10)
        ax.plot((x, x), (-y, -y - 10), marker='_', markevery=2, color='k', markersize=10)

    def draw_minus(self, x, y, ax):
        ax.plot((x, x), (y, 0), marker='1', markevery=2, color='k', markersize=10)
        ax.plot((x, x), (-y, 0), marker='2', markevery=2, color='k', markersize=10)

    def draw_plus(self, x, y, ax):
        ax.annotate('', xy=(x, y), xytext=(x, -y), arrowprops=dict(arrowstyle="<->", shrinkA=0, shrinkB=0))
