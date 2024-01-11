# license = Apache License, Version 2.0

class forge_setup:
    def __init__(self, cterm, checkday_list, period_list=[10, 30, 60], mode_round_number = -1, margin_value = 500, special_cnt_value = 0, period_comparison_base = [10, 30]):
        import numpy as np
        self.cterm = cterm
        self.checkday_list = checkday_list
        self.period_list = period_list
        self.mode_round_number = mode_round_number
        self.margin_value = margin_value
        self.special_cnt_value = special_cnt_value
        self.period_comparison_base = period_comparison_base
        
    def check_para(self, arr):
        import numpy as np
        limit = arr.shape[1]
        signal = True
        if self.cterm > limit:
            print('cterm value cannot be larger than time serie\'s term number!')
            signal = False
        elif np.max(self.checkday_list) > limit:
            print('checkday_list value cannot be larger than time serie\'s term number!')
            signal = False
        elif np.max(self.period_list) > limit:
            print('period_list value cannot be larger than time serie\'s term number!')
            signal = False
        elif self.margin_value > arr.max():
            print('Warning: input margin_value is larger than data\'s maximum value!')
            signal = False
        elif np.max(self.period_comparison_base*2) > limit:
            print('period_comparison_base value*2 cannot be larger than time serie\'s term number!')
            signal = False
        if signal:
            print('Parameters GOOD to go!')
            
    def maxday_check_f(self, input_list, arr):
        import numpy as np
        if np.max(input_list) < arr.shape[1]:
            return True
        else:
            print('Input period list\'s max value is ', np.max(input_list), ', but data time period only go back to ', arr.shape[1], ' terms.')
            print('Input error causes certain features could not be produced.')
            return False
    
    def period_stats_feature_f(self, period_list, arr, mode_round_number, special_cnt_value):
        import numpy as np
        from scipy import stats
        col_list = []
        col_nm = []
        if self.maxday_check_f(period_list, arr):
            for d in period_list:
                col_list.extend([arr[:, -d:].sum(axis=1), arr[:, -d:].mean(axis=1), np.median(arr[:, -d:], axis=1), arr[:, -d:].max(axis=1), arr[:, -d:].min(axis=1), arr[:, -d:].max(axis=1)-arr[:, -d:].min(axis=1), stats.mode(arr[:, -d:].round(mode_round_number), axis=1)[0], (arr[:, -d:]==special_cnt_value).sum(axis=1)])
                col_nm.extend(['recent'+str(d)+'terms_sum', 'recent'+str(d)+'terms_mean', 'recent'+str(d)+'terms_median','recent'+str(d)+'terms_max','recent'+str(d)+'terms_min','recent'+str(d)+'terms_ptp', 'recent'+str(d)+'terms_mode', 'recent'+str(d)+'terms_special_number_count'])
        return col_list, col_nm

    def checkday_value_feature_f(self, checkday_list, arr):
        import numpy as np
        col_list = []
        col_nm = []
        if self.maxday_check_f(checkday_list, arr):
            for d in checkday_list:
                col_list.append(arr[:, -d])
                col_nm.append(str(d)+'terms_ago_value')
        return col_list, col_nm

    def rollnet_sum_feature_f(self, period_list, arr):
        import numpy as np
        col_list = []
        col_nm = []
        if self.maxday_check_f(period_list, arr):
            roll_arr = arr - np.roll(arr.round(), 1, axis=1)
            for d in period_list:
                col_list.append(roll_arr[:, -d:].sum(axis=1))
                col_nm.append('recent'+str(d)+'d_roll_net')
        return col_list, col_nm

    def diff_value_feature_f(self, checkday_list, arr):
        import numpy as np
        col_list = []
        col_nm = []
        if self.maxday_check_f(checkday_list, arr):
            for d in checkday_list:
                col_list.extend([arr[:, -1] - arr[:, -d], 
                                 (arr[:, -1] == arr[:, -d]).astype(int), 
                                 ((arr[:, -d:].mean(axis=1) == arr[:,-1])&(arr[:, -d:].std(axis=1) == 0)).astype(int)])
                col_nm.extend([str(d)+'terms_ago_difference', str(d)+'terms_ago_diff_label', 'recent'+str(d)+'terms_status_change_label'])  #status_change_label 1=values have changed/0=values staye unchanged
        return col_list, col_nm

    def comparison_feature_f(self, period_comparison_base, arr, mode_round_number, margin_value, special_cnt_value):
        import numpy as np
        from scipy import stats
        col_list = []
        col_nm = []
        if self.maxday_check_f(period_comparison_base*2, arr):
            for d in period_comparison_base:
                p0 = arr[:, -d:]
                p1 = arr[:, -d*2:-d]
                col_list.extend([p0.sum(axis=1)-p1.sum(axis=1), p0.mean(axis=1)-p1.mean(axis=1), np.median(p0, axis=1)-np.median(p1, axis=1), 
                 p0.max(axis=1)-p1.max(axis=1), p0.min(axis=1)-p1.min(axis=1), (p0.max(axis=1)-p0.min(axis=1))-(p1.max(axis=1)-p1.min(axis=1)),
                 stats.mode(p0.round(mode_round_number), axis=1)[0]-stats.mode(p1.round(mode_round_number), axis=1)[0], 
                ((p0==special_cnt_value).sum(axis=1))-((p1==special_cnt_value).sum(axis=1)), (p0>=margin_value).sum(axis=1)-(p1>=margin_value).sum(axis=1),
                ])
                col_nm.extend([str(d)+'term_comparison_sum', str(d)+'term_comparison_mean', str(d)+'term_comparison_median', str(d)+'term_comparison_max', str(d)+'term_comparison_min', str(d)+'term_comparison_ptp', str(d)+'term_comparison_mode', str(d)+'term_comparison_special_value_cout', str(d)+'term_comparison_reach_margin_count'])
        return col_list, col_nm

    def pull_features(self, arr):
        import numpy as np
        from scipy import stats
        col_list = [arr[:, -1], arr[:, -self.cterm], arr[:, -1] - arr[:, -self.cterm], arr.mean(axis=1), np.median(arr, axis=1), arr.max(axis=1), arr.min(axis=1), 
                    arr.max(axis=1) - arr.min(axis=1), stats.mode(arr.round(self.mode_round_number), axis=1)[0], (arr>=self.margin_value).sum(axis=1), ((arr>90).sum(axis=1)>0).astype(int),
                   (arr[:, -self.cterm:]>=self.margin_value).sum(axis=1), ((arr[:, -self.cterm:]>90).sum(axis=1)>0).astype(int), (arr==self.special_cnt_value).sum(axis=1)
                   ]
        feature_index = ['current_value', 'cterm_value', 'cterm_current_diff', 'all_term_mean', 'all_term_median', 'all_term_max', 'all_term_min', 
                  'all_term_ptp', 'all_term_mode', 'all_term_reach_margin_count', 'all_term_reach_margin_label',
                 'cterm_reach_margin_count', 'cterm_reach_margin_label', 'all_term_special_number_count'
                 ]
        ld, nd = self.checkday_value_feature_f(self.checkday_list, arr)
        ls, ns = self.period_stats_feature_f(self.period_list, arr, self.mode_round_number, self.special_cnt_value)
        lr, nr = self.rollnet_sum_feature_f(self.period_list, arr)
        ldf, ndf = self.diff_value_feature_f(self.checkday_list, arr)
        lc, nc = self.comparison_feature_f(self.period_comparison_base, arr, self.mode_round_number, self.margin_value, self.special_cnt_value)
        col_list.extend(ld)
        col_list.extend(ls)
        col_list.extend(lr)
        col_list.extend(ldf)
        col_list.extend(lc)
        feature_index.extend(nd)
        feature_index.extend(ns)
        feature_index.extend(nr)
        feature_index.extend(ndf)
        feature_index.extend(nc)
        feature_array = np.concatenate([col_list], axis=1).T
        return feature_array, feature_index
