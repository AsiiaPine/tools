import glob
import os
import pandas as pd


class Sample:
    """
    Contains info about a single experiment with barrier located at a certain
    distance from the phototransistor plane at a particular Y coord.
    """

    dst_from_pt_plane: float
    y: float

    mean_adc1: float
    std_adc1: float
    mean_adc2: float
    std_adc2: float

    def __init__(
        self,
        dst_from_pt_plane: float,
        y: float,
        mean_adc1: float,
        std_adc1: float,
        mean_adc2: float,
        std_adc2: float,
    ):
        self.dst_from_pt_plane = dst_from_pt_plane
        self.y = y

        self.mean_adc1 = mean_adc1
        self.std_adc1 = std_adc1
        self.mean_adc2 = mean_adc2
        self.std_adc2 = std_adc2
    def from_dict(data: dict):
        return Sample(data["dst_from_pt_plane"], data["y"], data["mean_adc1"], data["std_adc1"], data["mean_adc2"], data["std_adc2"])


def calculate_mean_std(dst: float, y: float, df: pd.DataFrame):
    mean_adc_1 = df.loc[df["actuator_id"] == 0]["force"].mean()
    std_adc_1 = df.loc[df["actuator_id"] == 0]["force"].std()
    mean_adc_2 = df.loc[df["actuator_id"] == 1]["force"].mean()
    std_adc_2 = df.loc[df["actuator_id"] == 1]["force"].std()
    return Sample(
        dst_from_pt_plane=dst,
        y=y,
        mean_adc1=mean_adc_1,
        mean_adc2=mean_adc_2,
        std_adc1=std_adc_1,
        std_adc2=std_adc_2,
    )


def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    directories = glob.glob(directory + "/tests_data/*/", recursive=True)
    dist_from_pt = 0
    for dir in directories:
        tests = glob.glob(dir + "/*/", recursive=True)
        # if "new_barrier" not in dir:
        #     continue
        test_dict = {}
        for test in tests:
            test_name = test.split("/")[-1]
            results = glob.glob(test + "*.csv", recursive=True)
            samples = []
            for res in results:
                # print(res)
                if ".csv" not in res:
                    continue
                try:
                    y = res.split("/")[-1].split(".csv")[0]
                    y = y.replace("reversed_", "")
                    y = y.replace("reserve_", "")
                    y = float(y)
                except:
                    continue
                df = pd.read_csv(res)
                sample = calculate_mean_std(dist_from_pt, y, df)
                samples.append({"y": y,"dst_from_pt_plane": 0.0,"mean_adc1": sample.mean_adc1, "mean_adc2": sample.mean_adc2, "std_adc1": sample.std_adc1, "std_adc2": sample.std_adc2})

            dataframe = pd.DataFrame(samples)
            # print(dataframe.head())
            dataframe.to_csv(test + "/result.csv")

if __name__ == "__main__":
    main()