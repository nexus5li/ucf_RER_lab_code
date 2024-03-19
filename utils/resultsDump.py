import pickle
import pandas as pd
from pathlib import Path

def save_results(test_results: pd.DataFrame, path2ResultsDir: Path, fname, testtime, snapshot=False):
    results_fpath = path2ResultsDir.joinpath('spreadsheets', f"{fname}_{testtime}.csv")
    test_results.to_csv(results_fpath, index=False)
    
    if snapshot:
        results_snapshotpath = path2ResultsDir.joinpath('snapshots', f"{fname}_{testtime}.pkl")
        test_results.to_pickle(results_snapshotpath)
