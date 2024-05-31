import glob
import os
import pandas as pd
from collect_results import Sample
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
linestyles = ["-", "--"]
linestyle_labels = ["forward", "reversed"]


def plot_same_dst_from_pt_plane(
    dst: float,
    samples: list[Sample],
    plot_raw_voltage: int = 0,
    test_name: str = "",
    fig=None,
    ax=None,
    to_save=False,
    linestyle=None,
    color=None,
    labels=["1", "2"],
    voltage_multiplier_val=1,
    offset=0,
    folder="combined_figs"
):
    """
    Plot a single plot with relation between ADC1 and ADC2 means for all Ys at a certain distance
    from the phototransistor plane. Also add std deviation as a Y bars for each point.
    """
    if fig is None:
        fig, ax = plt.subplots()

    voltage_multiplier = 1
    if plot_raw_voltage != 0:
        if plot_raw_voltage == 1:

            voltage_multiplier = (
                3.3 / 4095
            )  # 3.3V is the voltage reference, 4095 is the max ADC value
        else:
            voltage_multiplier = voltage_multiplier_val
    ax.fill_between(
        [sample.y for sample in samples],
        [
            (sample.mean_adc1 - sample.std_adc1 - offset) * voltage_multiplier
            for sample in samples
        ],
        [
            (sample.mean_adc1 + sample.std_adc1 - offset) * voltage_multiplier
            for sample in samples
        ],
        alpha=0.2,
        # color="red",
    )

    ax.fill_between(
        [sample.y for sample in samples],
        [
            (sample.mean_adc2 - sample.std_adc2 - offset) * voltage_multiplier
            for sample in samples
        ],
        [
            (sample.mean_adc2 + sample.std_adc2 - offset) * voltage_multiplier
            for sample in samples
        ],
        alpha=0.2,
        # color="blue",
    )

    # Plot ADC1s as a line
    ax.plot(
        [sample.y for sample in samples],
        [(sample.mean_adc1 - offset) * voltage_multiplier for sample in samples],
        color=color,
        linestyle=linestyle,
        # label=labels[0],
        # color="red",
    )

    # Plot ADC2s as a line
    ax.plot(
        [sample.y for sample in samples],
        [(sample.mean_adc2 - offset) * voltage_multiplier for sample in samples],
        color,
        linestyle=linestyle,
        # label=labels[1],
        # color="blue",
    )

    # Make grid visible
    ax.grid(True, which="both", linestyle="--")

    # ax.set_title(f"Dst from PT plane: {dst} mm")
    ax.set_xlabel("Y (mm)")
    ax.set_ylabel(f"ADC Signal {'(raw)' if plot_raw_voltage==0 else '(V)' if plot_raw_voltage==1  else ''}")
    ax.legend()
    # print(f"{BASE_DIR}/figs/plot_{test_name}_{dst}_{'(V)' if not plot_raw_voltage else '(raw)'}")
    if to_save:
        fig.savefig(
            f"{BASE_DIR}/{folder}/{'(raw)' if plot_raw_voltage==0 else '(V)' if plot_raw_voltage==1  else 'scaled'}/plot_{test_name}_{dst}_{'(V)' if not plot_raw_voltage else '(raw)'}.png"
        )
    # plt.close()
    return fig, ax


def main():
    directory = os.path.dirname(os.path.realpath(__file__)) + "/tests_data"
    print(directory + "/tests_data/")
    directories = glob.glob(directory + "/*/", recursive=True)
    dist_from_pt = 0
    for dir in directories:
        tests = glob.glob(dir + "/*/", recursive=True)
        base_test_name = dir.split("/")[-2]
        print(base_test_name)
        fig, ax = None, None
        fig1, ax1 = None, None
        fig2, ax2 = None, None
        samples_list = {}
        start_mes = {}
        end_mes = {}
        for test in tests:
            try:
                test_name = base_test_name + "_" + test.split("/")[-2]
                is_reverse = False
                results = glob.glob(test + "result.csv", recursive=True)
                samples = pd.read_csv(results[0]).to_dict(orient="records")
                dist_from_pt = test.split("/")[-2]

                samples_list[dist_from_pt] = []
                start_mes[dist_from_pt] = 0
                end_mes[dist_from_pt] = 0
                offset = samples[0]["mean_adc1"]
                max_sample = 1 / (max(samples, key=lambda x: x["mean_adc1"])["mean_adc1"])
                print(offset, max_sample)
                for i, sample in enumerate(samples):
                    sample_ = Sample.from_dict(sample)
                    samples_list[dist_from_pt].append(sample_)
                    if (
                        i > 0
                        and (
                            sample_.mean_adc1 - samples_list[dist_from_pt][i - 1].mean_adc1
                        )
                        > sample_.std_adc1
                        and start_mes[dist_from_pt] == 0
                    ):
                        start_mes[dist_from_pt] = sample_.y
                    if i < (len(samples) - 1):
                        if (
                            samples[i + 1]["mean_adc1"] - sample_.mean_adc1
                        ) > sample_.std_adc1:
                            end_mes[dist_from_pt] = sample_.y
            except:
                continue
        end_start = {"start": start_mes, "end": end_mes}
        pd.DataFrame(end_start).to_csv(dir + "end_start.csv")
        i = 0
        legend_patches = []
        distances = []
        # Create a list of linestyles

        # Create a list of labels for the linestyles

        # legend_patches.append(mpatches.Patch(linestyle="--", label="reverse"))
        # legend_patches.append(mpatches.Patch(linestyle="-", label="forward"))

        for distance, samples in samples_list.items():
            try:
                    
                samples.sort(key=lambda sample: sample.y)
                dst = distance
                is_reverse = False
                if "reverse" in dst:
                    is_reverse = True
                    dst = dst.replace("reversed_", "")
                    dst = dst.replace("reverse_", "")
                    dst=dst.replace("reversed", "")
                    dst=dst.replace("_", "")
                if "base" in dst:
                    continue
                print(dst)
                dst = float(dst)
                print(dst)
                j = i
                if dst in distances:
                    j = distances.index(dst)
                else:
                    i += 1
                    distances.append(dst)
                    legend_patches.append(mpatches.Patch(color=colors[j], label=dst))

                fig, ax = plot_same_dst_from_pt_plane(
                    dst,
                    samples,
                    plot_raw_voltage=True,
                    test_name=test_name,
                    fig=fig,
                    ax=ax,
                    to_save=False,
                    labels=[
                        f"{'reverse ' if is_reverse else ''}mes {dst}",
                        f"{'reverse ' if is_reverse else ''}ref {dst}",
                    ],
                    linestyle=f"{'--' if is_reverse else '-'}",
                    color=colors[j],
                )
                fig1, ax1 = plot_same_dst_from_pt_plane(
                    dst,
                    samples,
                    plot_raw_voltage=False,
                    test_name=test_name,
                    fig=fig1,
                    ax=ax1,
                    to_save=False,
                    labels=[
                        f"{'reverse ' if is_reverse else ''}mes {dst}",
                        f"{'reverse ' if is_reverse else ''}ref {dst}",
                    ],
                    linestyle=f"{'--' if is_reverse else '-'}",
                    color=colors[j],
                )

                fig2, ax2 = plot_same_dst_from_pt_plane(
                    dst,
                    samples,
                    plot_raw_voltage=2,
                    test_name=test_name,
                    fig=fig2,
                    ax=ax2,
                    to_save=False,
                    labels=[
                        f"{'reverse ' if is_reverse else ''}mes {dst}",
                        f"{'reverse ' if is_reverse else ''}ref {dst}",
                    ],
                    linestyle=f"{'--' if is_reverse else '-'}",
                    color=colors[j],
                    voltage_multiplier_val=max_sample,
                    offset=offset,
                )
                # vlinestyle = f"{'-.' if is_reverse else ':'}"
                # alpha = 0.5
                print(distance)
                # ax.axvline(
                #     x=start_mes[distance],
                #     label=distance,
                #     color=colors[j],
                #     linestyle=vlinestyle,
                #     alpha=alpha,
                # )
                # ax.axvline(
                #     x=end_mes[distance],
                #     label=distance,
                #     color=colors[j],
                #     linestyle=vlinestyle,
                #     alpha=alpha,
                # )
                # ax1.axvline(
                #     x=end_mes[distance],
                #     label=distance,
                #     color=colors[j],
                #     linestyle=vlinestyle,
                #     alpha=alpha,
                # )
                # ax1.axvline(
                #     x=start_mes[distance],
                #     label=distance,
                #     color=colors[j],
                #     linestyle=vlinestyle,
                #     alpha=alpha,
                # )
                # print(dst)
                # ax2.axvline(
                #     x=end_mes[distance],
                #     label=distance,
                #     color=colors[j],
                #     linestyle=vlinestyle,
                #     alpha=alpha,
                # )
                # ax2.axvline(
                #     x=start_mes[distance],
                #     label=distance,
                #     color=colors[j],
                #     linestyle=vlinestyle,
                #     alpha=alpha,
                # )
                print(dst)
            except:
                continue
        try:
            # ax.set_title(f"Dst from PT plane: {dst} mm")
            print("saving", base_test_name)
            # ax.legend(handles=legend_patches)
            legend_lines = [
                mlines.Line2D([], [], color="black", linestyle=linestyle, label=label)
                for linestyle, label in zip(linestyles, linestyle_labels)
            ]

            ax.legend(handles=legend_lines + legend_patches)
            fig.savefig(
                f"{BASE_DIR}/combined_figs/voltage/plot_{base_test_name}_{'(V)'}.png"
            )
            plt.close(fig)

            ax1.legend(handles=legend_lines + legend_patches)
            # ax1.legend(handles=legend_patches)
            fig1.savefig(
                f"{BASE_DIR}/combined_figs/raw/plot_{base_test_name}_{'raw'}.png"
            )
            plt.close(fig1)
            ax2.legend(handles=legend_lines + legend_patches)
            # ax2.legend(handles=legend_patches)
            fig2.savefig(f"{BASE_DIR}/combined_figs/scaled/plot_{base_test_name}.png")
            plt.close(fig2)
        except: continue

if __name__ == "__main__":
    main()
