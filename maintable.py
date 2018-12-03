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
        tab.loc['Q':'T', 0] = ''
        tab.loc['f':'d', self.columns - 1] = ''
        tab.loc['alpha':'L', self.columns - 1] = ''
        tab.loc['Beta':'T', self.columns - 1] = ''
        self.magnify = []
        self.LHI = np.nan
        self.vignette = np.nan
        self.prev_tables = []
        self.history_input = []
        self.history = []

    def change_value(self, row, column, value, func=0):
        tab = self.table
        if np.isnan(value):
            return
        if func == 0:
            self.prev_tables.append(tab.copy(True))
            self.history_input.append('{}{} set as {}'.format(row, column, value))
        if row in MainTable.ind:
            if np.isnan(tab.loc[row, column]):
                tab.at[row, column] = value
                self.history.append('{}{} is now {} from {}'.format(row, column, value, func))
                self.analise_input(row, column)

    def undo_changes(self):
        self.table = self.prev_tables.pop()
        self.history_input.pop()
        self.vignette = self.table.loc['vignette', 0]
        self.LHI = self.table.loc['lhi', 0]

    def magnification(self, from_col, to_col, magn, var):
        if from_col > to_col:
            from_col, to_col = to_col, from_col
        from_col -= 1
        if to_col >= self.columns or from_col < 0:
            raise ValueError()
        else:
            for item in self.magnify:
                if from_col == item['from'] and to_col == item['to']:
                    return
            self.magnify.append({'from': from_col, 'to': to_col, 'magn': magn, 'type': var})

        if len(self.magnify) > 0:
            for i, elem in enumerate(self.magnify):
                from_col, to_col = elem['from'], elem['to']
                if elem['type'] == 'V':
                    if not np.all(np.isnan((self.table.loc['alpha', from_col], self.table.loc['alpha', to_col]))):
                        self.analyse44(i)
                elif elem['type'] == 'Q':
                    if not np.all(np.isnan((self.table.loc['Beta', from_col], self.table.loc['Beta', to_col]))):
                        self.analyse45(i)

    def iterate(self, row, col, from_col, to_col, var, target_dimension, start_value):
        tab = self.table
        increament = start_value
        if not np.isnan(tab.loc[row, col]):
            return
        dim = np.array((self.table.loc[var, from_col:to_col - 1]), dtype=np.float64)
        if not np.any(np.isnan(dim)):
            return
        dim[np.isnan(dim)] = 0
        prev_dim = np.sum(dim)
        for i in range(100):
            self.change_value(row, col, start_value, 0)
            dim = np.array((self.table.loc[var, from_col:to_col - 1]), dtype=np.float64)
            if np.any(np.isnan(dim)):
                self.undo_changes()
                return
            cur_dim = np.sum(dim)
            print('prev: {}; curr: {}, target: {}'.format(prev_dim, cur_dim, target_dimension))
            if prev_dim < target_dimension < cur_dim or cur_dim < target_dimension < prev_dim:
                increament *= -1 / 3
            elif target_dimension < prev_dim < cur_dim or target_dimension > prev_dim > cur_dim:
                increament *= -1
            else:
                increament *= 2
            prev_dim = cur_dim
            start_value += increament
            if np.isclose(target_dimension - cur_dim, 0):
                break
            self.undo_changes()
            #print('{} inc: {}, next_try: {}'.format(i, increament, start_value))

    def change_lhi(self, value, func=0):
        if np.isnan(self.LHI):
            self.LHI = value
            self.table.loc['lhi', 0] = self.LHI
            self.history.append('LHI set as {} from {}'.format(value, func))
            self.check_lhi_function()

    def set_vignetting(self, value):
        if np.isnan(self.vignette):
            self.prev_tables.append(self.table.copy(True))
            self.vignette = float(value)
            for i in range(self.columns):
                self.table.loc['vignette', i] = self.vignette
                self.analyse1(i)
            self.history_input.append('vignette set as {}'.format(value))

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
                    if not np.all(np.isnan((self.table.loc['alpha', from_col], self.table.loc['alpha', to_col]))):
                        self.analyse44(i)
                elif elem['type'] == 'Q':
                    if not np.all(np.isnan((self.table.loc['Beta', from_col], self.table.loc['Beta', to_col]))):
                        self.analyse45(i)

        self.check_lhi_function()

    def check_f_function(self, column):
        self.analyse15(column)
        self.analyse16(column)
        self.analyse17(column)
        self.analyse19(column)
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
        self.analyse38(column)
        self.analyse40(column + 1)
        self.analyse42(column)
        self.analyse42(column + 1)

    def check_v_function(self, column):
        self.analyse14(column)
        self.analyse16(column)
        self.analyse17(column)
        self.analyse19(column)
        self.analyse38(column)
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
        self.analyse38(column)
        self.analyse40(column)
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
        self.analyse23(column)
        self.analyse24(column)
        self.analyse26(column)
        self.analyse38(column)
        self.analyse39(column)
        self.analyse40(column)
        self.analyse41(column)

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
                self.analyse38(i)
                self.analyse39(i)
                self.analyse40(i)
                self.analyse41(i)
                self.analyse42(i)
                self.analyse43(i)

    def analyse1(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            temp = dict(vignette=self.vignette, H=tab.loc['H', c], Y=tab.loc['Y', c], phi=tab.loc['phi', c])
            ans = self.check_if_nan(**temp)
            if ans != 'phi':
                return
            a = 2 * np.abs(tab.loc['H', c])
            b = 2 * (np.abs(tab.loc['Y', c]) + self.vignette * np.abs(tab.loc['H', c]))
            val = np.max([a, b])
            self.change_value('phi', c, val, 1)

    def analyse14(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            V, alpha, alpha_1 = tab.loc['V', c], tab.loc['alpha', c], tab.loc['alpha', c - 1]
            temp = dict(V=V, alpha=alpha, alpha_1=alpha_1)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'alpha_1':
                val = V * alpha
                self.change_value('alpha', c - 1, val, 14)
            if ans == 'alpha' and not np.isclose(V, 0):
                val = alpha_1 / V
                self.change_value('alpha', c, val, 14)
            if ans == 'V' and not np.isclose(alpha, 0):
                self.history.append(temp)
                val = alpha_1 / alpha
                self.change_value('V', c, val, 14)

    def analyse15(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            H, f, alpha, alpha_1 = tab.loc['H', c], tab.loc['f', c], tab.loc['alpha', c], tab.loc['alpha', c - 1]
            temp = dict(alpha=alpha, alpha_1=alpha_1, H=H, f=f)
            ans = self.check_if_nan(**temp)
            '''if ans == '':
                return'''
            if 'alpha' in ans and not np.isclose(f, 0):
                val = alpha_1 if H == 0 else alpha_1 + H / f
                self.change_value('alpha', c, val, 15)
            if 'alpha_1' in ans and not np.isclose(f, 0):
                val = alpha if H == 0 else alpha - H / f
                self.change_value('alpha', c - 1, val, 15)
            if ans == 'H' and not np.isclose(alpha - alpha_1, 0):
                val = f * (alpha - alpha_1)
                self.change_value('H', c, val, 15)
            if ans == 'f' and not np.isclose(alpha - alpha_1, 0):
                val = H / (alpha - alpha_1)
                self.change_value('f', c, val, 15)

    def analyse16(self, column):
        tab = self.table
        c = column
        H, f, V, alpha = tab.loc['H', c], tab.loc['f', c], tab.loc['V', c], tab.loc['alpha', c]
        if 1 <= c <= self.columns - 2:
            temp = dict(alpha=alpha, V=V, H=H, f=f)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'alpha' and not np.isclose(f * (V - 1), 0):
                val = - H / (f * (V - 1))
                self.change_value('alpha', c, val, 16)
            if ans == 'V' and not np.isclose(alpha * f, 0):
                val = 1 - H / (alpha * f)
                self.change_value('V', c, val, 16)
            if ans == 'H':
                val = alpha * f * (1 - V)
                self.change_value('H', c, val, 16)
            if ans == 'f' and not np.isclose(alpha * (V - 1), 0):
                val = H / (alpha * (1 - V))
                self.change_value('f', c, val, 16)

    def analyse17(self, column):
        tab = self.table
        c = column
        L, f, V, = tab.loc['L', c], tab.loc['f', c], tab.loc['V', c]
        if 1 <= c <= self.columns - 2:
            temp = dict(f=f, V=V, L=L)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'L' and not np.isclose(V, 0):
                val = - (f * (1 - V) ** 2) / V
                self.change_value('L', c, val, 17)
            if ans == 'f' and not np.isclose(V - 1, 0):
                val = - L * V / (1 - V) ** 2
                self.change_value('f', c, val, 17)

    def analyse18(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            alpha, alpha_1, L, H = tab.loc['alpha', c], tab.loc['alpha', c - 1], tab.loc['L', c], tab.loc['H', c]
            temp = dict(alpha=alpha, alpha_1=alpha_1, L=L, H=H)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'alpha' and not np.isclose(H + L * alpha_1, 0):
                val = H * alpha_1 / (H + L * alpha_1)
                self.change_value('alpha', c, val, 18)
            if ans == 'alpha_1' and not np.isclose(H - L * alpha, 0):
                val = H * alpha / (H - L * alpha)
                self.change_value('alpha', c - 1, val, 18)
            if ans == 'H' and not np.isclose(alpha - alpha_1, 0):
                val = L * alpha * alpha_1 / (alpha_1 - alpha)
                self.change_value('H', c, val, 18)
            if ans == 'L' and not np.isclose(alpha * alpha_1, 0):
                val = H * (alpha_1 - alpha) / (alpha * alpha_1)
                self.change_value('L', c, val, 18)

    def analyse19(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            H, V, L, alpha_1 = tab.loc['H', c], tab.loc['V', c], tab.loc['L', c], tab.loc['alpha', c - 1]
            temp = dict(alpha_1=alpha_1, H=H, L=L, V=V)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'alpha_1' and not np.isclose(L, 0):
                val = H * (V - 1) / L
                self.change_value('alpha', c - 1, val, 19)
            if ans == 'L' and not np.isclose(alpha_1, 0):
                val = H * (V - 1) / alpha_1
                self.change_value('L', c, val, 19)
            if ans == 'H' and not np.isclose(V - 1, 0):
                val = L * alpha_1 / (V - 1)
                self.change_value('H', c, val, 19)
            if ans == 'V' and not np.isclose(H, 0):
                val = (H + L * alpha_1) / H
                self.change_value('V', c, val, 19)

    def analyse20(self, column):
        tab = self.table
        c = column
        if self.columns - 2 >= c >= 0:
            H1, H, alpha, d = tab.loc['H', c + 1], tab.loc['H', c], tab.loc['alpha', c], tab.loc['d', c]
            temp = dict(H1=H1, H=H, alpha=alpha, d=d)
            ans = self.check_if_nan(**temp)
            '''if ans == '':
                return'''
            if 'H' in ans:
                val = H1 if np.any(np.isclose((alpha, d), 0)) else H1 + alpha * d
                self.change_value('H', c, val, 20)
            if 'H1' in ans:
                val = H if np.any(np.isclose((alpha, d), 0)) else H - alpha * d
                self.change_value('H', c + 1, val, 20)
            if 'alpha' in ans and not np.isclose(tab.loc['d', c], 0):
                val = 0 if np.isclose(H - H1, 0) else (H - H1) / d
                self.change_value('alpha', c, val, 20)
            if ans == 'd' and not np.isclose(alpha, 0):
                val = (H - H1) / alpha
                self.change_value('d', c, val, 20)

    def analyse21(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            Beta, Beta_1, Q = tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['Q', c]
            temp = dict(Beta=Beta, Beta_1=Beta_1, Q=Q)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Beta_1':
                val = Beta * Q
                self.change_value('Beta', c - 1, val, 21)
            if ans == 'Beta' and not np.isclose(Q, 0):
                val = Beta_1 / Q
                self.change_value('Beta', c, val, 21)
            if ans == 'Q' and not np.isclose(Beta, 0):
                val = Beta_1 / Beta
                self.change_value('Q', c, val, 21)

    def analyse22(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            Beta, Beta_1, Y, f = tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['Y', c], tab.loc['f', c]
            temp = dict(Beta=Beta, Beta_1=Beta_1, Y=Y, f=f)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Beta_1' and not np.isclose(f, 0):
                val = Beta - Y / f
                self.change_value('Beta', c - 1, val, 22)
            if ans == 'Beta' and not np.isclose(f, 0):
                val = Beta_1 + Y / f
                self.change_value('Beta', c, val, 22)
            if ans == 'Y':
                val = f * (Beta - Beta_1)
                self.change_value('Y', c, val, 22)
            if ans == 'f' and not np.isclose(Beta - Beta_1, 0):
                val = Y / (Beta - Beta_1)
                self.change_value('f', c, val, 22)

    def analyse23(self, column):
        tab = self.table
        c = column
        Beta, Q, Y, f = tab.loc['Beta', c], tab.loc['Q', c], tab.loc['Y', c], tab.loc['f', c]
        if 0 < c <= self.columns - 2:
            temp = dict(Beta=Beta, Q=Q, Y=Y, f=f)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Beta' and not np.isclose(f * (1 - Q), 0):
                val = Y / (f * (1 - Q))
                self.change_value('Beta', c, val, 23)
            if ans == 'Q' and not np.isclose(Beta * f, 0):
                val = 1 - Y / (Beta * f)
                self.change_value('Q', c, val, 23)
            if ans == 'Y':
                val = Beta * f * (1 - Q)
                self.change_value('Y', c, val, 23)
            if ans == 'f' and not np.isclose(Beta * (1 - Q), 0):
                val = Y / (Beta * (1 - Q))
                self.change_value('f', c, val, 23)

    def analyse24(self, column):
        tab = self.table
        c = column
        f, Q, T = tab.loc['f', c], tab.loc['Q', c], tab.loc['T', c]
        if 0 < c <= self.columns - 2:
            temp = dict(f=f, Q=Q, T=T)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'T' and not np.isclose(Q, 0):
                val = - (f * (1 - Q) ** 2) / Q
                self.change_value('T', c, val, 24)
            if ans == 'f' and not np.isclose(1 - Q, 0):
                val = - Q * T / (1 - Q) ** 2
                self.change_value('f', c, val, 24)

    def analyse25(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            Beta, Beta_1, T, Y = tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['T', c], tab.loc['Y', c]
            temp = dict(Beta=Beta, Beta_1=Beta_1, T=T, Y=Y)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Beta_1' and not np.isclose(Y - Beta * T, 0):
                val = Beta * Y / (Y - Beta * T)
                self.change_value('Beta', c - 1, val, 25)
            if ans == 'Beta' and not np.isnan(Beta_1 * T + Y, 0):
                val = Y * Beta_1 / (Y + Beta_1 * T)
                self.change_value('Beta', c, val, 25)
            if ans == 'T' and not np.isclose(Beta * Beta_1, 0):
                val = Y * (Beta_1 - Beta) / (Beta * Beta_1)
                self.change_value('T', c, val, 25)
            if ans == 'Y' and not np.isclose(Beta_1 - Beta, 0):
                val = Beta * Beta_1 * T / (Beta_1 - Beta)
                self.change_value('Y', c, val, 25)

    def analyse26(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            Beta_1, T, Y, Q = tab.loc['Beta', c - 1], tab.loc['T', c], tab.loc['Y', c], tab.loc['Q', c]
            temp = dict(Beta_1=Beta_1, T=T, Q=Q, Y=Y)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Beta_1' and not np.isclose(T, 0):
                val = Y * (Q - 1) / T
                self.change_value('Beta', c - 1, val, 26)
            if ans == 'T' and not np.isclose(Beta_1, 0):
                val = Y * (Q - 1) / Beta_1
                self.change_value('T', c, val, 26)
            if ans == 'Y' and not np.isclose(Q - 1, 0):
                val = Beta_1 * T / (Q - 1)
                self.change_value('Y', c, val, 26)
            if ans == 'Q' and not np.isclose(Y, 0):
                val = 1 + Beta_1 * T / Y
                self.change_value('Q', c, val, 26)

    def analyse27(self, column):
        tab = self.table
        c = column
        if self.columns - 2 >= c >= 0:
            Beta, Y, Y1, d = tab.loc['Beta', c], tab.loc['Y', c], tab.loc['Y', c + 1], tab.loc['d', c]
            temp = dict(Beta=Beta, Y=Y, Y1=Y1, d=d)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Y1':
                val = Y - Beta * d
                self.change_value('Y', c + 1, val, 27)
            if ans == 'Y':
                val = Y1 + Beta * d
                self.change_value('Y', c, val, 27)
            if ans == 'Beta' and not np.isclose(d, 0):
                val = (Y - Y1) / d
                self.change_value('Beta', c, val, 27)
            if ans == 'd' and not np.isclose(Beta, 0):
                val = (Y - Y1) / Beta
                self.change_value('d', c, val, 27)

    def analyse36(self, column):
        tab = self.table
        c = column
        lhi, Beta, H, Y, alpha = self.LHI, tab.loc['Beta', c], tab.loc['H', c], tab.loc['Y', c], tab.loc['alpha', c]
        if self.columns - 2 > c:
            temp = dict(Beta=Beta, Y=Y, alpha=alpha, H=H, lhi=lhi)
            ans = self.check_if_nan(**temp)
            # normals
            if ans == 'H' and not np.isclose(Beta, 0):
                val = (Y * alpha - lhi) / Beta
                self.change_value('H', c, val, 36)
            if ans == 'Y' and not np.isclose(alpha, 0):
                val = (Beta * H + lhi) / alpha
                self.change_value('Y', c, val, 36)
            if ans == 'Beta' and not np.isclose(H, 0):
                val = (Y * alpha - lhi) / H
                self.change_value('Beta', c, val, 36)
            if ans == 'alpha' and not np.isclose(Y, 0):
                val = (Beta * H + lhi) / Y
                self.change_value('alpha', c, val, 36)
            if ans == 'lhi':
                val = Y * alpha - Beta * H
                self.change_lhi(val)
            # specials
            if np.isnan(H) and np.any(np.isclose((Y, alpha), 0)) and not np.isclose(Beta, 0):
                val = - lhi / Beta
                self.change_value('H', c, val, '36s')
            if np.isnan(Y) and np.any(np.isclose((H, Beta), 0)) and not np.isclose(alpha, 0):
                val = lhi / alpha
                self.change_value('Y', c, val, '36s')
            if np.isnan(Beta) and np.any(np.isclose((Y, alpha), 0)) and not np.isclose(H, 0):
                val = -lhi / H
                self.change_value('Beta', c, val, '36s')
            if np.isnan(alpha) and np.any(np.isclose((H, Beta), 0)) and not np.isclose(Y, 0):
                val = lhi / Y
                self.change_value('alpha', c, val, '36s')
            if np.isnan(lhi) and np.any(np.isclose((Y, alpha), 0)) and not np.any(np.isnan((H, Beta))):
                val = - H * Beta
                self.change_lhi(val, '36s1')
            if np.isnan(lhi) and np.any(np.isclose((H, Beta), 0)) and not np.any(np.isnan((Y, alpha))):
                val = alpha * Y
                self.change_lhi(val, '36s2')

    def analyse37(self, column):
        tab = self.table
        c = column
        lhi = self.LHI
        if c >= 1:
            Beta, H, Y, alpha = tab.loc['Beta', c - 1], tab.loc['H', c], tab.loc['Y', c], tab.loc['alpha', c - 1]
            temp = dict(Beta=Beta, Y=Y, alpha=alpha, H=H, lhi=lhi)
            ans = self.check_if_nan(**temp)
            if ans == 'H' and not np.isclose(Beta, 0):
                val = (Y * alpha - lhi) / Beta
                self.change_value('H', c, val, 37)
            if ans == 'Y' and not np.isclose(alpha, 0):
                val = (Beta * H + lhi) / alpha
                self.change_value('Y', c, val, 37)
            if ans == 'Beta' and not np.isclose(H, 0):
                val = (Y * alpha - lhi) / H
                self.change_value('Beta', c - 1, val, 37)
            if ans == 'alpha' and not np.isclose(Y, 0):
                val = (Beta * H + lhi) / Y
                self.change_value('alpha', c - 1, val, 37)
            if ans == 'lhi':
                val = Y * alpha - Beta * H
                self.change_lhi(val)
            if np.isnan(H) and np.any(np.isclose((Y, alpha), 0)) and not np.isclose(Beta, 0):
                val = - lhi / Beta
                self.change_value('H', c, val, '37s')
            if np.isnan(Y) and np.any(np.isclose((H, Beta), 0)) and not np.isclose(alpha, 0):
                val = lhi / alpha
                self.change_value('Y', c, val, '37s')
            if np.isnan(Beta) and np.any(np.isclose((Y, alpha), 0)) and not np.isclose(H, 0):
                val = -lhi / H
                self.change_value('Beta', c - 1, val, '37s')
            if np.isnan(alpha) and np.any(np.isclose((H, Beta), 0)) and not np.isclose(Y, 0):
                val = lhi / Y
                self.change_value('alpha', c - 1, val, '37s')
            if np.isnan(lhi) and np.any(np.isclose((Y, alpha), 0)) and not np.any(np.isnan((H, Beta))):
                val = - H * Beta
                self.change_lhi(val, '37s1')
            if np.isnan(lhi) and np.any(np.isclose((H, Beta), 0)) and not np.any(np.isnan((Y, alpha))):
                val = alpha * Y
                self.change_lhi(val, '37s2')

    def analyse38(self, column):
        tab = self.table
        c = column
        alpha, Y, Q, V, lhi = tab.loc['alpha', c], tab.loc['Y', c], tab.loc['Q', c], tab.loc['V', c], self.LHI
        temp = dict(alpha=alpha, Y=Y, Q=Q, V=V, lhi=lhi)
        if 0 < c <= self.columns - 2:
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Y' and not np.isclose(alpha * (Q - V), 0):
                val = lhi * (Q - 1) / (alpha * (Q - V))
                self.change_value('Y', c, val, 38)
            if ans == 'V' and not np.isclose(Y * alpha, 0):
                val = (lhi * (1 - Q) + Q * Y * alpha) / (Y * alpha)
                self.change_value('V', c, val, 38)
            if ans == 'Q' and not np.isclose(lhi - Y * alpha, 0):
                val = (lhi - V * Y * alpha) / (lhi - Y * alpha)
                self.change_value('Q', c, val, 38)
            if ans == 'alpha' and not np.isclose(Y * (Q - V), 0):
                val = lhi * (Q - 1) / (Y * (Q - V))
                self.change_value('alpha', c, val, 38)
            if ans == 'lhi' and not np.isclose(Q - 1, 0):
                val = Y * alpha * (Q - V) / (Q - 1)
                self.change_lhi(val)

    def analyse39(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            Beta, H, Q, V, lhi = tab.loc['Beta', c], tab.loc['H', c], tab.loc['Q', c], tab.loc['V', c], self.LHI
            temp = dict(Beta=Beta, H=H, Q=Q, V=V, lhi=lhi)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'H' and not np.isclose(Beta * (Q - V), 0):
                val = lhi * (V - 1) / (Beta * (Q - V))
                self.change_value('H', c, val, 39)
            if ans == 'V' and not np.isclose(Beta * H + lhi, 0):
                val = (Beta * H * Q + lhi) / (Beta * H + lhi)
                self.change_value('V', c, val, 39)
            if ans == 'Q' and not np.isclose(Beta * H, 0):
                val = (Beta * H * V + lhi * (V - 1)) / (Beta * H)
                self.change_value('Q', c, val, 39)
            if ans == 'Beta' and not np.isclose(H * (Q - V), 0):
                val = lhi * (V - 1) / (H * (Q - V))
                self.change_value('Beta', c, val, 39)
            if ans == 'lhi' and not np.isclose(V - 1, 0):
                val = Beta * H * (Q - V) / (V - 1)
                self.change_lhi(val)

    def analyse40(self, column):
        tab = self.table
        c = column
        if 0 < c <= self.columns - 2:
            Y, alpha_1, Q, V, lhi = tab.loc['Y', c], tab.loc['alpha', c - 1], tab.loc['Q', c], tab.loc['V', c], self.LHI
            temp = dict(Y=Y, alpha_1=alpha_1, Q=Q, V=V, lhi=lhi)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'V' and not np.isclose(lhi * (Q - 1) + Y * alpha_1, 0):
                val = Q * Y * alpha_1 / (lhi * (Q - 1) + Y * alpha_1)
                self.change_value('V', c, val, 40)
            if ans == 'Q' and not np.isclose(lhi * V - Y * alpha_1, 0):
                val = V * (lhi - Y * alpha_1) / (lhi * V - Y * alpha_1)
                self.change_value('Q', c, val, 40)
            if ans == 'alpha_1' and not np.isclose(Y * (Q - V), 0):
                val = lhi * V * (Q - 1) / (Y * (Q - V))
                self.change_value('alpha', c - 1, val, 40)
            if ans == 'Y' and not np.isclose(alpha_1 * (Q - V), 0):
                val = lhi * V * (Q - 1) / (alpha_1 * (Q - V))
                self.change_value('Y', c, val, 40)
            if ans == 'lhi' and not np.isclose(V * (Q - 1), 0):
                val = Y * alpha_1 * (Q - V) / (V * (Q - 1))
                self.change_lhi(val)

    def analyse41(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            H, Beta_1, Q, V, lhi = tab.loc['H', c], tab.loc['Beta', c - 1], tab.loc['Q', c], tab.loc['V', c], self.LHI
            temp = dict(H=H, Beta_1=Beta_1, Q=Q, V=V, lhi=lhi)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'Q' and not np.isclose(Beta_1 * H + lhi * (1 - V), 0):
                val = Beta_1 * H * V / (Beta_1 * H + lhi * (1 - V))
                self.change_value('Q', c, val, 41)
            if ans == 'V' and not np.isclose(Beta_1 * H + lhi * Q, 0):
                val = Q * (Beta_1 * H + lhi) / (Beta_1 * H + lhi * Q)
                self.change_value('V', c, val, 41)
            if ans == 'Beta_1' and not np.isclose(H * (Q - V), 0):
                val = lhi * Q * (V - 1) / (H * (Q - V))
                self.change_value('Beta', c - 1, val, 41)
            if ans == 'H' and not np.isclose(Beta_1 * (Q - V), 0):
                val = lhi * Q * (V - 1) / (Beta_1 * (Q - V))
                self.change_value('H', c, val, 41)
            if ans == 'lhi' and not np.isclose(Q * (V - 1)):
                val = Beta_1 * H * (Q - V) / (Q * (V - 1))
                self.change_lhi(val)

    def analyse42(self, column):
        tab = self.table
        c = column
        if 1 <= c <= self.columns - 2:
            lhi, alpha_1 = self.LHI, tab.loc['alpha', c - 1]
            Beta, Beta_1, f, alpha = tab.loc['Beta', c], tab.loc['Beta', c - 1], tab.loc['f', c], tab.loc['alpha', c]
            temp = dict(Beta=Beta, Beta_1=Beta_1, alpha=alpha, alpha_1=alpha_1, f=f, lhi=lhi)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'alpha' and not np.isclose(Beta_1 * f, 0):
                val = (Beta * alpha_1 * f - lhi) / (Beta_1 * f)
                self.change_value('alpha', c, val, 42)
            if ans == 'alpha_1' and not np.isclose(Beta * f, 0):
                val = (Beta_1 * alpha * f + lhi) / (Beta * f)
                self.change_value('alpha', c - 1, val, 42)
            if ans == 'Beta' and not np.isclose(alpha_1 * f, 0):
                val = (Beta_1 * alpha * f + lhi) / (alpha_1 * f)
                self.change_value('Beta', c, val, 42)
            if ans == 'Beta_1' and not np.isclose(alpha * f, 0):
                val = (Beta * alpha_1 * f - lhi) / (alpha * f)
                self.change_value('Beta', c - 1, val, 42)
            if ans == 'f' and not np.isclose(Beta * alpha_1 - Beta_1 * alpha, 0):
                val = lhi / (Beta * alpha_1 - Beta_1 * alpha)
                self.change_value('f', c, val, 42)
            if ans == 'lhi':
                val = f * (Beta * alpha_1 - Beta_1 * alpha)
                self.change_lhi(val)

    def analyse43(self, column):
        tab = self.table
        c = column
        if self.columns - 2 >= c >= 0:
            lhi, d = self.LHI, tab.loc['d', c]
            H, H1, Y, Y1 = tab.loc['H', c], tab.loc['H', c + 1], tab.loc['Y', c], tab.loc['Y', c + 1]
            temp = dict(H=H, H1=H1, Y=Y, Y1=Y1, d=d, lhi=lhi)
            ans = self.check_if_nan(**temp)
            if ans == '':
                return
            if ans == 'H' and not np.isclose(Y1, 0):
                val = (H1 * Y + lhi * d) / Y1
                self.change_value('H', c, val, 43)
            if ans == 'H1' and not np.isclose(Y, 0):
                val = (H * Y1 - lhi * d) / Y
                self.change_value('H', c + 1, val, 43)
            if ans == 'Y' and not np.isclose(H1, 0):
                val = (H * Y1 - lhi * d) / H1
                self.change_value('Y', c, val, 43)
            if ans == 'Y1' and not np.isclose(H, 0):
                val = (H1 * Y + lhi * d) / H
                self.change_value('Y', c + 1, val, 43)
            if ans == 'd' and not np.isclose(lhi, 0):
                val = (H * Y1 - H1 * Y) / lhi
                self.change_value('d', c, val, 43)
            if ans == 'lhi' and not np.isclose(d, 0):
                val = (H * Y1 - H1 * Y) / d

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

    def check_if_nan(self, **kwargs):
        ans = []
        for key, val in kwargs.items():
            if np.isnan(val):
                ans.append(key)
        ans = ans[0] if len(ans) == 1 else ans
        ans = '' if len(ans) == 0 else ans
        return ans

    def plot(self):
        undo = False
        plt.ioff()
        plt.close('all')
        y = list(self.table.loc['Y'])
        h = list(self.table.loc['H'])
        f = list(self.table.loc['f'])
        d = list(self.table.loc['d', 0:self.columns - 2])
        phi = list(self.table.loc['phi'])
        if np.all(np.isnan(phi)):
            self.set_vignetting(1)
            phi = list(self.table.loc['phi'])
            undo = True
        phi = [el / 2 if not el == '' else np.nan for el in phi]
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
        plt.ylim(-ax_max - 5, ax_max + 5)
        plt.xlim(min(d1) - 1, d1[-1] + 1)
        ax.set_aspect('equal')
        a = 2 * ax_max
        b = d[-1] + 2
        c, d = figaspect(a / b)
        if np.max([c, d]) < 15:
            c, d = 2 * c, 2 * d
        fig.set_size_inches(c, d)
        plt.tight_layout()
        plt.savefig('test.png', dpi=300)
        plt.ion()
        plt.show()
        if undo:
            self.undo_changes()

    def draw_stop(self, x, y, ax):
        ax.plot((x, x), (y, y + 10), marker='_', markevery=2, color='k', markersize=10)
        ax.plot((x, x), (-y, -y - 10), marker='_', markevery=2, color='k', markersize=10)

    def draw_minus(self, x, y, ax):
        ax.plot((x, x), (y, 0), marker='1', markevery=2, color='k', markersize=10)
        ax.plot((x, x), (-y, 0), marker='2', markevery=2, color='k', markersize=10)

    def draw_plus(self, x, y, ax):
        ax.annotate('', xy=(x, y), xytext=(x, -y), arrowprops=dict(arrowstyle="<->", shrinkA=0, shrinkB=0))
