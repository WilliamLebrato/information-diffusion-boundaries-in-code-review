import unittest
import pandas as pd
from datetime import timedelta
from tqdm.auto import tqdm
from tqdm.notebook import tqdm


def create_dummy():
    test_data = {'shortest': [9, 12, 13, 4, 8, 8, 4, 13, 3, 3],
                 'fastest': ['16 days 02:50:34', '14 days 06:40:03', '21 days 02:26:53', '5 days 01:27:06', '5 days 07:53:02', '7 days 23:46:43', '3 days 07:37:39', '14 days 23:20:12', '4 days 19:17:55', '7 days 20:31:59'],
                 'foremost': ['2020-02-20 05:02:59', '2020-02-18 09:48:53', '2020-02-28 08:08:56', '2020-02-13 05:45:54', '2020-02-18 01:54:14', '2020-02-27 12:39:11', '2020-02-11 08:48:44', '2020-02-26 12:00:25', '2020-02-14 01:14:48', '2020-02-14 10:35:19']}
    niv_1 = [-1000302490388055954, -1000302490388055954, -1000302490388055954, -1000302490388055954, -1000302490388055954,
             999681621755937669, 999681621755937669, 999681621755937669, 999681621755937669, 999681621755937669]
    niv_2 = [-1001028986621278490, -1001349348375309194, -1001376759116612193, -1001818555676085500, -1003437920076289658,
             997201945995039833, 997837947427984124, 998434677038352691, 998928952161399101, 999086956044825111]

    cat_niv_1 = pd.Categorical(
        niv_1, categories=[-1000302490388055954, 999681621755937669])

    index = pd.MultiIndex.from_arrays(
        [cat_niv_1, niv_2], names=['source', 'target'])
    df = pd.DataFrame(test_data, index=index)

    df['shortest'] = df['shortest'].astype('int64')
    df['fastest'] = pd.to_timedelta(df['fastest'])
    df['foremost'] = pd.to_datetime(df['foremost'])

    return df


def compute(df):

    cumulative_distribution_over_time = []
    total = len(df.index.get_level_values(0).categories)
    for source, group in tqdm(df.fastest.groupby(level=0), total=total):
        n_unique = group.reset_index(level=1).resample(pd.Timedelta(
            days=1), on='fastest', offset=-group.min()).target.nunique()
        cumulative_distribution_over_time += [n_unique.rename(source)]
    index = pd.timedelta_range(start=timedelta(
        weeks=0), end=timedelta(weeks=4), freq='D')
    return pd.concat(cumulative_distribution_over_time, axis=1).fillna(0).cumsum().reindex(index).ffill().astype(int)


df = create_dummy()


class TestNotebook(unittest.TestCase):
    def test_compute(self):
        result = compute(df)
        self.assertEqual(result.shape, (29, 2))

    def test_compute_no_unique(self):
        equal = df.copy()
        equal['shortest'] = 1
        equal['fastest'] = pd.to_timedelta('16 days 02:50:34')
        equal['foremost'] = pd.to_datetime('2020-02-20 05:02:59')
        result = compute(df)
        res = compute(equal)
        self.assertFalse(result.equals(res))

    def test_compute_zero(self):
        zero = df.copy()
        zero['shortest'] = 0
        zero['fastest'] = pd.to_timedelta('0 days 00:00:00')
        zero['foremost'] = pd.to_datetime('2020-02-20 05:02:59')
        result = compute(df)
        res = compute(zero)
        self.assertFalse(result.equals(res))

    def test_compute_negative(self):
        negative = df.copy()
        negative['shortest'] = -1
        negative['fastest'] = pd.to_timedelta('-16 days 02:50:34')
        negative['foremost'] = pd.to_datetime('2020-02-20 05:02:59')
        result = compute(df)
        res = compute(negative)
        if not result.equals(res):
            self.fail('Negative values are not allowed')
