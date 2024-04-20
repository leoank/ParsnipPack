import datetime
import pandas as pd
from pathlib import Path
import numpy as np


def main():
    bos_summary = pd.read_parquet(Path(__file__).parents[2].joinpath("data/bos_initial.parquet"))

    print(bos_summary['serves_veg'].sum() / len(bos_summary))
   
    bos_summary.sort_values(by="time", ascending=True, inplace=True)
    
    for i in range(10):
        j = 5 + i * 5
        per_veg = bos_summary.loc[[i * 5, j], 'serves_veg'].sum() / float(5) * 100
        print(str(per_veg) + "%")

    print(datetime.datetime.fromtimestamp(bos_summary['time'].values[0]))
    print(datetime.datetime.fromtimestamp(bos_summary['time'].values[-1]))


if __name__ == "__main__":
    main()