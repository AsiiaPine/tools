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
import plotly.graph_objects as go


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Prepare directory for plot images
# os.makedirs("/figs", exist_ok=True)
colors = ["b", "g", "r", "c", "m", "y", "k", "w"]
linestyles = ["-", "--"]
linestyle_labels = ["forward", "reversed"]


def main():
    directory = os.path.dirname(os.path.realpath(__file__)) + "/tests_data"
    directories = glob.glob(directory + "/*/", recursive=True)
    dist_from_pt = 0
    for dir in directories:
        tests = glob.glob(dir + "/*/", recursive=True)
        base_test_name = dir.split("/")[-2]
        samples_list = {}
        start_mes = {}
        end_mes = {}
        figs = {}

        offset = 0
        scale = 1
        scale2 = 1
        for test in tests:
            test_name = base_test_name + "_" + test.split("/")[-2]
            is_reverse = False
            results = glob.glob(test + "result.csv", recursive=True)
            samples = pd.read_csv(results[0]).to_dict(orient="records")

            make_normalized = True
            if make_normalized:
                offset = samples[0]["mean_adc1"]
                scale = 1 / max(max(samples, key=lambda x: x["mean_adc1"])["mean_adc1"] - offset, 0.0001)
                scale2 = 1 / max((max(samples, key=lambda x: x["mean_adc2"])["mean_adc2"]), 0.0001)
        
        for test in tests:
            test_name = base_test_name + "_" + test.split("/")[-2]
            is_reverse = False
            results = glob.glob(test + "result.csv", recursive=True)
            samples = pd.read_csv(results[0]).to_dict(orient="records")

            if len(samples) < 3:
                continue
            dist_from_pt = test.split("/")[-2]
            dst = dist_from_pt
            if "reverse_" in dst:
                is_reverse = True
                dst = dst.replace("reverse_", "")
            if "base" in dst:
                continue
            dst = float(dst)
            figs[dst] = None
            samples_list[dist_from_pt] = []
            start_mes = {"y": 100, "adc": 0}
            end_mes = {"y": 100, "adc": 0}
            # offset = samples[0]["mean_adc1"]
            # max_sample = 1 / (max(samples, key=lambda x: x["mean_adc1"])["mean_adc1"])
            samples.sort(key=lambda sample: sample["y"])
            for i, sample in enumerate(samples):

                sample["mean_adc1"] = (sample["mean_adc1"]-offset) * scale
                sample["mean_adc2"] = (sample["mean_adc2"]) * scale2
                sample_ = Sample.from_dict(sample)
                samples_list[dist_from_pt].append(sample_)
                if (
                    sample_.mean_adc1 - samples_list[dist_from_pt][0].mean_adc1
                ) < 30*(scale) and start_mes["y"] > sample_.y:
                    start_mes = {
                        "y": sample_.y,
                        "adc": sample_.mean_adc1,
                    }
                if (
                    samples[-1]["mean_adc1"] - sample_.mean_adc1
                ) < 20*(scale) and end_mes["y"] > sample_.y:
                    end_mes = {
                        "y": sample_.y,
                        "adc": sample_.mean_adc1,
                    }
            for i, sample in enumerate(samples):
                sample_ = Sample.from_dict(sample)
                samples_list[dist_from_pt].append(sample_)
        i = 0
        legend_patches = []
        distances = []
        big_fig = go.Figure()
        for distance, samples in samples_list.items():
            # Your existing code here
            samples.sort(key=lambda sample: sample.y)
            is_reverse = False
            dst = distance
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

            print("len(samples)", len(samples))
            if len(samples) < 3:
                continue

            y = []
            res = []
            print(start_mes)
            print(end_mes)
            for sample in samples:
                if (sample.y >= start_mes["y"]) & (sample.y <= end_mes["y"]):
                    y.append(sample.y)
                    res.append(sample.mean_adc1)
            y = np.array(y)
            res = np.array(res)

            # Reshape the input arrays to 2D format
            y_reshaped = y.reshape(-1, 1)
            res_reshaped = res.reshape(-1, 1)
            model = LinearRegression().fit(y_reshaped, res_reshaped)

            # Get the slope and intercept of the fitted line
            slope = model.coef_[0]
            intercept = model.intercept_
            pred = model.predict(
                np.array([sample.y for sample in samples]).reshape(-1, 1)
            )
            if figs[dst] is None:
                figs[dst] = go.Figure()
            fig = figs[dst]
            # Perform linear regression
            model = LinearRegression().fit(y_reshaped, res_reshaped)
            slope = model.coef_[0]
            intercept = model.intercept_

            # Predicted values
            pred = model.predict(
                np.array([sample.y for sample in samples]).reshape(-1, 1)
            )

            # Plot the predicted values with linestyle '--'
            fig.add_trace(
                go.Scatter(
                    x=[sample.y for sample in samples],
                    y=pred.flatten(),
                    mode="lines",
                    line=dict(color="blue", dash="dash"),
                    name=f"Slope {slope}",
                )
            )

            # Plot ADC1s as a line with linestyle 'solid'
            fig.add_trace(
                go.Scatter(
                    x=[sample.y for sample in samples],
                    y=[sample.mean_adc1 for sample in samples],
                    mode="lines",
                    line=dict(color="green", dash="solid",             
                            width=max([sample.std_adc1 for sample in samples])),
                    name=f"ADC1{'_reversed' if is_reverse else ''}",
                    
                )
            )

            # Plot ADC2s as a line with linestyle 'solid'
            fig.add_trace(
                go.Scatter(
                    x=[sample.y for sample in samples],
                    y=[sample.mean_adc2 for sample in samples],
                    mode="lines",
                    line=dict(color="red", dash="solid", 
                            width=max([sample.std_adc2 for sample in samples])),
                    name=f"ADC2{'_reversed' if is_reverse else ''}",
                )
            )

            # Add vertical lines
            fig.add_vline(
                x=start_mes["y"],
                line=dict(color="cyan", width=2, dash="dash"),
                opacity=0.5,
            )
            fig.add_vline(
                x=end_mes["y"],
                line=dict(color="cyan", width=2, dash="dash"),
                opacity=0.5,

            )

            fig.update_layout(title=f"Slope: {slope}, Offset: {intercept}", 
                    xaxis_title="y, mm",
                    yaxis_title=f"{'normalized voltage' if make_normalized else 'Raw'}")


            # Plot the predicted values with linestyle '--'
            big_fig.add_trace(
                go.Scatter(
                    x=[sample.y for sample in samples],
                    y=pred.flatten(),
                    mode="lines",
                    line=dict(color="blue", dash="dash"),
                    name=f"Slope {slope} dst: {dst}",
                )
            )

            # Plot ADC1s as a line with linestyle 'solid'
            big_fig.add_trace(
                go.Scatter(
                    x=[sample.y for sample in samples],
                    y=[sample.mean_adc1 for sample in samples],
                    mode="lines",
                    line=dict(color="green", dash="solid",             
                            width=max([sample.std_adc1 for sample in samples])),
                    name=f"ADC1{'_reversed' if is_reverse else ''} {dst}",
                    
                )
            )

            # Plot ADC2s as a line with linestyle 'solid'
            big_fig.add_trace(
                go.Scatter(
                    x=[sample.y for sample in samples],
                    y=[sample.mean_adc2 for sample in samples],
                    mode="lines",
                    line=dict(color="red", dash="solid", 
                            width=max([sample.std_adc2 for sample in samples])),
                    name=f"ADC2{'_reversed' if is_reverse else ''} {dst}",
                )
            )

            # Add vertical lines
            big_fig.add_vline(
                x=start_mes["y"],
                line=dict(color="cyan", width=2, dash="dash"),
                opacity=0.5,
                name=f"start linearization window {dst}"
            )
            big_fig.add_vline(
                x=end_mes["y"],
                line=dict(color="cyan", width=2, dash="dash"),
                opacity=0.5,
                name=f"end linearization window {dst}"
            )

            big_fig.update_layout(title=f"Slope: {slope}, Offset: {intercept}", 
                    xaxis_title="y, mm",
                    yaxis_title=f"{'normalized voltage' if make_normalized else 'Raw'}")


            print("Slope:", slope)
            print("Intercept:", intercept)
        for dist, fig in figs.items():
            fig.write_html(
                f"{BASE_DIR}/model/{'scaled/' if make_normalized else ''}plot_{base_test_name}{'(V)'}_{dist}.html"
            )
        big_fig.write_html(
                f"{BASE_DIR}/model/{'scaled/' if make_normalized else ''}plot_{base_test_name}{'(V)'}.html"
            )
if __name__ == "__main__":
    main()
