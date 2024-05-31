from matplotlib import pyplot as plt

results = {
    "1": {
        "0.0": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.37483,
            "y_mp": 0.37073,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.11": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3707,
            "y_mp": 0.3747,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.22": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746,
            "y_mp": 0.3706,
            "y_min": 0.3600,
            "y_max": 0.3880,
        },
        "0.33": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3707,
            "y_mp": 0.3746,
            "y_min": 0.3602,
            "y_max": 0.3880,
        },
        "0.44": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746,
            "y_mp": 0.37083,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.55": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3708,
            "y_mp": 0.3746,
            "y_min": 0.3599,
            "y_max": 0.3880,
        },
        "0.67": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746,
            "y_mp": 0.3711,
            "y_min": 0.3596,
            "y_max": 0.3881,
        },
        "0.78": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746,
            "y_mp": 0.3711,
            "y_min": 0.3593,
            "y_max": 0.3881,
        },
        "0.89": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.37455,
            "y_mp": 0.3712,
            "y_min": 0.3596,
            "y_max": 0.3880,
        },
        "1.0": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746,
            "y_mp": 0.3713,
            "y_min": 0.3606,
            "y_max": 0.3880,
        },
    },
    # "0.0": {
    #     "x_max": 1.05,
    #     "x_min": 1.85,
    #     "y_mn": 0.385,
    #     "y_mp": 0.622659,
    #     "y_min": 0,
    #     "y_max": 1,
    # },
    # "new_0.1": {
    #     "x_max": 2.3,
    #     "x_min": 1.5,
    #     "y_mn": 0.5699,
    #     "y_mp": 0.5115,
    #     "y_min": 0,
    #     "y_max": 1,
    # },
    "test": {
        "new_sensor_0.77": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.756,
            "y_mp": 3.703,
            "y_min": 3.576,
            "y_max": 3.849,
        },
        "new_sensor_0.55": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.743,
            "y_mp": 3.697,
            "y_min": 3.576,
            "y_max": 3.849,
        },
        "new_sensor_0.33": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.682,
            "y_mp": 3.719,
            "y_min": 3.576,
            "y_max": 3.849,
        },
        "new_sensor_0.11": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.700,
            "y_mp": 3.664,
            "y_min": 3.576,
            "y_max": 3.849,
        },
        "new_sensor_0.00": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.700926,
            "y_mp": 3.666813,
            "y_min": 3.578,
            "y_max": 3.850,
        },
    },
    "test_1": {
        "new_sensor_1_0.77": {
            "x_max": 2.4,
            "x_min": 1.4,
            "y_mn": 3.710,
            "y_mp": 3.794668,
            "y_min": 3.576,
            "y_max": 3.845,
        },
        "new_sensor_1_0.55": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.779,
            "y_mp": 3.708,
            "y_min": 3.576,
            "y_max": 3.845,
        },
        "new_sensor_1_0.33": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.759,
            "y_mp": 3.703,
            "y_min": 3.576,
            "y_max": 3.845,
        },
        "new_sensor_1_0.11": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.756,
            "y_mp": 3.707,
            "y_min": 3.576,
            "y_max": 3.845,
        },
        "new_sensor_1_0.00": {
            "x_max": 2.2,
            "x_min": 1.4,
            "y_mn": 3.746,
            "y_mp": 3.709,
            "y_min": 3.576,
            "y_max": 3.845,
        },
    },
    "5":
    {
      "0.0": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3748,
            "y_mp": 0.3707,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.11": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3707272,
            "y_mp": 0.37485,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.22": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746,
            "y_mp": 0.3705,
            "y_min": 0.3600,
            "y_max": 0.3880,
        },
        "0.33": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3705282,
            "y_mp": 0.3746,
            "y_min": 0.3602,
            "y_max": 0.3880,
        },
        "0.44": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3744,
            "y_mp": 0.3707,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.55": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3707,
            "y_mp": 0.3744,
            "y_min": 0.3599,
            "y_max": 0.3880,
        },
        "0.67": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3744,
            "y_mp": 0.3707983,
            "y_min": 0.3596,
            "y_max": 0.3881,
        },
        "0.78": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3744,
            "y_mp": 0.3709581,
            "y_min": 0.3593,
            "y_max": 0.3881,
        },
        "0.89": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3744,
            "y_mp": 0.3710,
            "y_min": 0.3596,
            "y_max": 0.3880,
        },
        "1.0": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3744,
            "y_mp": 0.371165,
            "y_min": 0.3606,
            "y_max": 0.3880,
        },
    },  
    "6":
    {
      "0.0": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3748292,
            "y_mp": 0.3703678,
            "y_min": 0.3602,
            "y_max": 0.3880,
        },
        "0.11": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.37055,
            "y_mp": 0.37475,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.22": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.37456,
            "y_mp": 0.370393,
            "y_min": 0.3600,
            "y_max": 0.3880,
        },
        "0.33": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.37034,
            "y_mp": 0.374569,
            "y_min": 0.3602,
            "y_max": 0.3880,
        },
        "0.44": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3744,
            "y_mp": 0.3707,
            "y_min": 0.3601,
            "y_max": 0.3880,
        },
        "0.55": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3705599,
            "y_mp": 0.374445,
            "y_min": 0.3600,
            "y_max": 0.3880,
        },
        "0.67": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.374356,
            "y_mp": 0.3707432,
            "y_min": 0.3596,
            "y_max": 0.3881,
        },
        "0.78": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3746544,
            "y_mp": 0.37094,
            "y_min": 0.3595,
            "y_max": 0.3881,
        },
        "0.89": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.37445,
            "y_mp": 0.37095,
            "y_min": 0.3596,
            "y_max": 0.3880,
        },
        "1.0": {
            "x_max": 2.28,
            "x_min": 1.27,
            "y_mn": 0.3743,
            "y_mp": 0.37114,
            "y_min": 0.3606,
            "y_max": 0.3880,
        },
    },  
}
hysteresis = {}
dst = {}
res = {}
results = results
for test, samples in results.items():
    dst[test] = []
    res[test] = []

    for dist, data in samples.items():
        hyst = 100 * abs(
            (data["y_mn"] - data["y_mp"]) / (data["y_max"] - data["y_min"])
        )
        hysteresis[dist] = hyst
        dst[test].append(float(dist.split("_")[-1]))
        res[test].append(hyst)
print(hysteresis)
for test, samples in results.items():
    plt.plot(dst[test], res[test], label=test)
plt.xlabel("Distance from PT, mm")
plt.ylabel("Hysteresis value, %")
plt.legend()
plt.savefig("hyst.png")
