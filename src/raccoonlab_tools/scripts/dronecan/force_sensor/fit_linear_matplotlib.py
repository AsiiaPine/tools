import glob
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from collect_results import Sample
from plot_results import plot_same_dst_from_pt_plane
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Prepare directory for plot images
# os.makedirs("/figs", exist_ok=True)
colors = ["b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", "k", "w"]
linestyles = ["-", "--"]
linestyle_labels = ["forward", "reversed"]


def main():
    directory = os.path.dirname(os.path.realpath(__file__)) + "/tests_data"
    # directory = os.path.join([directory, 'tests_data'])
    # print(directory + "/tests_data/")
    directories = glob.glob(directory + "/*/", recursive=True)
    dist_from_pt = 0
    # print(directories)
    for dir in directories:
        tests = glob.glob(dir + "/*/", recursive=True)
        base_test_name = dir.split("/")[-2]
        # print(base_test_name)
        samples_list = {}
        start_mes = {}
        end_mes = {}
        # print(dir)
        for test in tests:
            test_name = base_test_name + "_" + test.split("/")[-2]
            # print(test_name)
            is_reverse = False
            results = glob.glob(test + "result.csv", recursive=True)
            samples = pd.read_csv(results[0]).to_dict(orient="records")
            dist_from_pt = test.split("/")[-2].replace("base_", "")
            dst = dist_from_pt
            if "reverse_" in dst:
                is_reverse = True
                dst = dst.replace("reverse_", "")
            try:
                dst = float(dst)
            except: continue
            samples_list[dist_from_pt] = []
            start_mes[dst] = 0
            end_mes[dst] = 0
            make_normalized = False

            offset = 0
            max_sample = 1
            max_sample2 = 1
            if make_normalized:
                    
                offset = samples[0]["mean_adc1"]
                max_sample = 1 / (max(samples, key=lambda x: x["mean_adc1"])["mean_adc1"] - offset)
                max_sample2 = 1 / (max(samples, key=lambda x: x["mean_adc2"])["mean_adc2"])
            # print(offset, max_sample)

            for i, sample in enumerate(samples):
                sample["mean_adc1"] = (sample["mean_adc1"]-offset) * max_sample
                sample["mean_adc2"] = (sample["mean_adc2"]) * max_sample2
                sample_ = Sample.from_dict(sample)
                samples_list[dist_from_pt].append(sample_)
                
                if (
                    i > 0
                    and (
                        sample_.mean_adc1 - samples_list[dist_from_pt][i - 1].mean_adc1
                    )
                    > sample_.std_adc1
                    and start_mes[dst] == 0
                ):
                    start_mes[dst] = {
                        "y": sample_.y,
                        "adc": sample_.mean_adc1,
                    }
                if i < (len(samples) - 1):
                    if (
                        samples[i + 1]["mean_adc1"] - sample_.mean_adc1
                    ) > 2 * sample_.std_adc1 and start_mes[dst] == 0:
                        end_mes[dst] = {
                            "y": sample_.y,
                            "adc": sample_.mean_adc1,
                        }
            for i, sample in enumerate(samples):
                sample_ = Sample.from_dict(sample)
                samples_list[dist_from_pt].append(sample_)
        i = 0
        legend_patches = []
        distances = []
        fig_big, ax_big = plt.subplots()

        for distance, samples in samples_list.items():
            
            samples.sort(key=lambda sample: sample.y)
            dst = distance
            is_reverse = False
            if "reverse_" in dst:
                is_reverse = True
                dst = dst.replace("reverse_", "")
            if "base" in dst:
                continue
            # print(dst)
            dst = float(dst)
            j = i
            if dst in distances:
                j = distances.index(dst)
            else:
                i += 1
                distances.append(dst)
                legend_patches.append(mpatches.Patch(color=colors[j], label=dst))
            y = np.array([sample.y for sample in samples])
            # print(start_mes, distance)
            # split_y = y[
            #     (y >= (start_mes[dst]["y"])) & (y <= (end_mes[dst]["y"]))
            # ]


            # res = np.array([sample.mean_adc1 for sample in samples])
            # split_res = res[
            #     (res >= start_mes[dst]["adc"]) & (res <= end_mes[dst]["adc"])
            # ]

            # # Reshape the data
            # y_reshaped = split_y.reshape(-1, 1)
            # res_reshaped = split_res.reshape(-1, 1)
            # Perform linear regression
            # model = LinearRegression().fit(y_reshaped, res_reshaped)
            # Get the slope and intercept of the fitted line
            # slope = model.coef_[0]
            # intercept = model.intercept_

            fig, ax = plt.subplots()

            # pred = model.predict(
            #     np.array([sample.y for sample in samples]).reshape(-1, 1)
            # )
            # ax.plot(
            #     [sample.y for sample in samples],
            #     pred,
            #     color=colors[1],
            #     linestyle="--",
            #     label=f"slope {slope}",
            # )
            # Plot ADC1s as a line
            ax.plot(
                [sample.y for sample in samples],
                [(sample.mean_adc1) for sample in samples],
                color=colors[2],
                # label="ADC1"
            )
            # Plot ADC1s as a line
            ax.plot(
                [sample.y for sample in samples],
                [(sample.mean_adc2) for sample in samples],
                color=colors[3],
                # label="ADC2"
            )
            # alpha = 0.5
            # ax.axvline(
            #     x=start_mes[distance]["y"],
            #     label=distance,
            #     color=colors[4],
            #     alpha=alpha,
            # )
            # ax.axvline(
            #     x=end_mes[distance]["y"],
            #     label=distance,
            #     color=colors[4],
            #     alpha=alpha,
            # )

            # ax.set_title(f"slope:{slope}, offset:{intercept}")
            legend_lines = [
            mlines.Line2D([], [], color="black", linestyle=linestyle, label=label)
            for linestyle, label in zip(linestyles, linestyle_labels)
            ]
            ax.legend(handles=legend_lines + legend_patches)
            print(f"{BASE_DIR}/model/plot_{base_test_name}{'_reversed_' if is_reverse else ''}{'(V)'}_{dst}.png")
            ax.set_xlabel("Y (mm)")
            ax.set_ylabel("ADC value")
            fig.legend()
            fig.savefig(f"{BASE_DIR}/model/plot_{base_test_name}{'_reversed_' if is_reverse else ''}{'(V)'}_{dst}{'_normalized' if make_normalized else ''}.png")
            vlinestyle = f"{'-.' if is_reverse else ':'}"
            alpha = 0.5
            # print(distance)
            plt.close(fig)


            # Plot ADC1s as a line
            ax_big.plot(
                [sample.y for sample in samples],
                [(sample.mean_adc1) for sample in samples],
                color=colors[j],
                linestyle=f"{linestyles[1] if is_reverse else linestyles[0]}"
                # label="ADC1"

            )
            # Plot ADC2s as a line
            ax_big.plot(
                [sample.y for sample in samples],
                [(sample.mean_adc2) for sample in samples],
                color=colors[j],
                linestyle=f"{linestyles[1] if is_reverse else linestyles[0]}"
                # label="ADC2"

            )
            # print("Slope:", slope)
            # print("Intercept:", intercept)
        ax_big.legend(handles=legend_lines + legend_patches)
    
        fig_big.legend()

        fig_big.savefig(f"{BASE_DIR}/model/combined/plot_{base_test_name}{'_reversed_' if is_reverse else ''}{'(V)'}_{dst}{'_normalized' if make_normalized else ''}.png")


if __name__ == "__main__":
    main()
