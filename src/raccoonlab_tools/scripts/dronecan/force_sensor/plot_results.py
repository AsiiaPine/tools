import glob
import os
import pandas as pd
from collect_results import Sample
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Prepare directory for plot images
# os.makedirs("/figs", exist_ok=True)


def plot_same_dst_from_pt_plane(
    dst: float,
    samples: list[Sample],
    plot_raw_voltage: bool = False,
    test_name: str = "",
):
    """
    Plot a single plot with relation between ADC1 and ADC2 means for all Ys at a certain distance
    from the phototransistor plane. Also add std deviation as a Y bars for each point.
    """

    fig = plt.figure()
    voltage_multiplier = 1
    if not plot_raw_voltage:
        voltage_multiplier = (
            3.3 / 4095
        )  # 3.3V is the voltage reference, 4095 is the max ADC value
    plt.fill_between(
        [sample.y for sample in samples],
        [
            (sample.mean_adc1 - sample.std_adc1) * voltage_multiplier
            for sample in samples
        ],
        [
            (sample.mean_adc1 + sample.std_adc1) * voltage_multiplier
            for sample in samples
        ],
        alpha=0.2,
        color="red",
    )

    plt.fill_between(
        [sample.y for sample in samples],
        [
            (sample.mean_adc2 - sample.std_adc2) * voltage_multiplier
            for sample in samples
        ],
        [
            (sample.mean_adc2 + sample.std_adc2) * voltage_multiplier
            for sample in samples
        ],
        alpha=0.2,
        color="blue",
    )

    # Plot ADC1s as a line
    plt.plot(
        [sample.y for sample in samples],
        [sample.mean_adc1 * voltage_multiplier for sample in samples],
        label="ADC1",
        color="red",
    )

    # Plot ADC2s as a line
    plt.plot(
        [sample.y for sample in samples],
        [sample.mean_adc2 * voltage_multiplier for sample in samples],
        label="ADC2",
        color="blue",
    )

    # Make grid visible
    plt.grid(True, which="both", linestyle="--")

    plt.title(f"Dst from PT plane: {dst} mm")
    plt.xlabel("Y (mm)")
    plt.ylabel(f"ADC Voltage {'(V)' if not plot_raw_voltage else '(raw)'}")
    plt.legend()
    # print(f"{BASE_DIR}/figs/plot_{test_name}_{dst}_{'(V)' if not plot_raw_voltage else '(raw)'}")
    fig.savefig(
        f"{BASE_DIR}/figs/{'voltage' if not plot_raw_voltage else 'raw'}/plot_{test_name}_{dst}_{'(V)' if not plot_raw_voltage else '(raw)'}.png"
    )
    plt.close()


def main():
    directory = os.path.dirname(os.path.realpath(__file__)) + "/tests_data"
    # directory = os.path.join([directory, 'tests_data'])
    print(directory + "/tests_data/*/")
    directories = glob.glob(directory + "/*/", recursive=True)
    dist_from_pt = 0
    # print(directories)
    for dir in directories:
        tests = glob.glob(dir + "/*/", recursive=True)
        base_test_name = dir.split("/")[-2]
        print(base_test_name)
        test_dict = {}
        for test in tests:
            test_name = base_test_name + "_"+test.split("/")[-2]
            # print(test_name)
            results = glob.glob(test + "result.csv", recursive=True)
            samples = pd.read_csv(results[0]).to_dict(orient="records")
            samples_list = {dist_from_pt: []}
            for sample in samples:
                # print(sample["mean_adc1"])
                samples_list[dist_from_pt].append(Sample.from_dict(sample))
            # print(samples_list)
            # print(samples)
            for dst, samples in samples_list.items():
                samples.sort(key=lambda sample: sample.y)
                plot_same_dst_from_pt_plane(dst, samples, plot_raw_voltage=True, test_name=test_name)
                plot_same_dst_from_pt_plane(dst, samples, plot_raw_voltage=False, test_name=test_name)


if __name__ == "__main__":
    main()
