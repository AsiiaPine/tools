import numpy as np
import pandas as pd
import glob 
import os
from collect_results import Sample

def main():
    directory = os.path.dirname(os.path.realpath(__file__)) + "/tests_data"
    # directory = os.path.join([directory, 'tests_data'])
    print(directory + "/tests_data/")
    directories = glob.glob(directory + "/*/", recursive=True)
    dist_from_pt = 0
    # print(directories)
    for dir in directories:
        tests = glob.glob(dir + "/*/", recursive=True)
        base_test_name = dir.split("/")[-2]
        fig, ax = None, None
        fig1, ax1 = None, None
        fig2, ax2 = None, None
        samples_list = {}
        start_mes = {}
        end_mes = {}
        normalization = glob.glob(dir + "both_0.00.csv", recursive=True)
        if len(normalization) == 0:
            continue
        print(normalization)
        norm = pd.read_csv(normalization[0])
        means = norm.groupby(["actuator_id"])["force"].mean()
        offsets = {"adc1": means[0], "adc2": means[1]}
        for test in tests:
            test_name = base_test_name + "_" + test.split("/")[-2]
            # print(test_name)
            is_reverse = False
            results = glob.glob(test + "result.csv", recursive=True)
            samples = pd.read_csv(results[0]).to_dict(orient="records")
            max_adc1 = 0
            max_adc2 = 0
            for sample in samples:
                sample["mean_adc1"] -= offsets["adc1"]
                sample["mean_adc2"] -= offsets["adc2"]
                if sample["mean_adc1"] > max_adc1:
                    max_adc1 = sample["mean_adc1"]
                if sample["mean_adc2"] > max_adc2:
                    max_adc2 = sample["mean_adc2"]
            for sample in samples:
                sample["mean_adc1"] /= max_adc1
                sample["mean_adc2"] /= max_adc2
            print("Hi")
            pd.DataFrame(samples).to_csv(test+"normalized.csv", index=False)
                # samples_list[sample["dst_from_pt_plane"]].append(Sample.from_dict(sample))

if __name__ == "__main__":
    main()
