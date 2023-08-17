import pandas as pd
import multiprocessing as mp
import numpy as np


def function(a, b, c, d):
    return a+b+c+d


def wrapp_apply(df):
    return df.apply(lambda row: function(row.A, row.B, row.C, row.D), axis=1)


def apply_multi(data_frame, column_name):
    num_of_processes = mp.cpu_count()
    data_split = np.array_split(data_frame, num_of_processes)
    pool = mp.Pool(num_of_processes)
    pool_results = pool.map(wrapp_apply, data_split)
    pool.close()
    pool.join()

    results = pd.concat(pool_results, axis=0)
    data_frame_with_results = pd.concat([data_frame, results], axis=1)
    data_frame_with_results.columns = list(data_frame_with_results.columns.values)[:-1]+[column_name]
    return data_frame_with_results


if __name__ == '__main__':
    input_df = pd.DataFrame(np.random.randint(0, 100, size=(100_000, 4)), columns=list('ABCD'))
    result = apply_multi(input_df, 'OUTPUT')
    print(result)
