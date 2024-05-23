results = {
    "0.0": {
        "x_max": 1.05,
        "x_min": 1.85,
        "y_mn": 0.385,
        "y_mp": 0.622659,
        "y_min": 0,
        "y_max": 1,
    },
    "new_0.1": {
        "x_max": 2.3,
        "x_min": 1.5,
        "y_mn": 0.5699,
        "y_mp": 0.5115,
        "y_min": 0,
        "y_max": 1,
    }
}
hysteresis = {}
for dist, data in results.items():
    hyst = abs((data["y_mn"] - data["y_mp"] / (data["y_max"] - data["y_min"])))
    hysteresis[dist] = hyst
print(hysteresis)
