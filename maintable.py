import pandas as pd
import numpy as np
import matplotlib.lines as lines


# will provide scientific notation for big numbers


# todo add to all analise function boundry for columns, it will fail otherwise on last and first columns
# todo division by zero!
# todo write special formulas from gabar
# todo stop comparing to zero…

class MainTable:
    ind = ['f', 'd', 'H', 'alpha', 'V', 'L', 'Y', 'Beta', 'Q', 'T', 'FIcz']

    def __init__(self, columns):
        """main data structure for code. Table is already preformat, to blank spaces are blank, like in original"""
        self.columns = columns
        self.table = pd.DataFrame(index=MainTable.ind, columns=list(range(self.columns)), dtype=np.float64)
        # some extra precision
        tab = self.table
        tab.loc['f', 0] = ''
        tab.loc['V':'L', 0] = ''
        tab.loc['Q':'FIcz', 0] = ''
        tab.loc['f':'d', self.columns - 1] = ''
        tab.loc['alpha':'L', self.columns - 1] = ''
        tab.loc['Beta':'FIcz', self.columns - 1] = ''
        self.LHI = np.nan
        self.winieta = np.nan

    def change_value(self, row, column, value, func=0):
        tab = self.table
        if row in MainTable.ind:
            if np.isnan(tab.loc[row, column]):
                tab.at[row, column] = value
                #tab.set_value(row, column, value)
                print('{}{} is now {} from {}'.format(row, column, value, func))
                self.analise_input(row, column)

    def change_lhi(self, value, func=0):
        if np.isnan(self.LHI):
            self.LHI = value
            print('LHI is now {} from {}'.format(value, func))
            self.check_lhi_function()

    def set_winieta(self, value, func=0):
        if np.isnan(self.winieta):
            self.winieta = float(value)
            print('Współczynnik winietowania is now {} from {}'.format(value, func))

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
        if 1 <= c <= self.columns-2:
            if not np.any(np.isnan([tab.loc['H',c], tab.loc['Y',c]])):
                a = 2 * np.abs(tab.loc['H',c])
                b = 2 * (np.abs(tab.loc['Y', c]) + self.winieta * np.abs(tab.loc['H', c]))
                val = np.max([a,b])
                self.change_value('FIcz', c, val, 1)

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
                self.change_value('Beta', c, val)
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

    def align_yaxis(self,ax1, v1, ax2, v2):
        _, y1 = ax1.transData.transform((0, v1))
        _, y2 = ax2.transData.transform((0, v2))
        self.adjust_yaxis(ax2,(y1-y2)/2,v2)
        self.adjust_yaxis(ax1,(y2-y1)/2,v1)

    def adjust_yaxis(self, ax,ydif,v):
        inv = ax.transData.inverted()
        _, dy = inv.transform((0, 0)) - inv.transform((0, ydif))
        miny, maxy = ax.get_ylim()
        miny, maxy = miny - v, maxy - v
        if -miny>maxy or (-miny==maxy and dy > 0):
            nminy = miny
            nmaxy = miny*(maxy+dy)/(miny+dy)
        else:
            nmaxy = maxy
            nminy = maxy*(miny+dy)/(maxy+dy)
        ax.set_ylim(nminy-.5+v, nmaxy+v)

    def plot(self):
        import matplotlib.pyplot as plt
        y=list(self.table.loc['Y'])
        h=list(self.table.loc['H'])
        d=list(self.table.loc['d',0:self.columns-2])
        ficz=list(self.table.loc['FIcz'])
        d1 = [0]
        for i, val in enumerate(d):
            d1.append(d1[i]+d[i])
        #fig, ax1 = plt.subplots()
        plt.plot(d1,h, label='h')
        #ax2 = ax1.twinx()
        plt.plot(d1,y, label='y', color='r')
        plt.legend()
        #plt.axhline(y=0, xmin=d1[0],xmax=d1[-1], color = 'k')
        for i, k in zip(d1[1:-1], ficz[1:-1]):
            plt.plot([i,i], [-k/2, k/2], color='black')
        #self.align_yaxis(ax2, 0, ax1, 0)
        print (d1,h,y)



cols = input("Podaj liczbę elementów: ")
table = MainTable(int(cols) + 1)
change_value = table.change_value
win = input("Podaj współczynnik winietowania: ")
table.set_winieta(win)
