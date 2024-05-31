from matplotlib import pyplot as plt
import numpy as np


res = {
    # "black":
    # {
    # "x_min": 2896,
    # "x_max": 2904,
    # },
    # "broken_optical_pair_metalic_barrier_with_black_rubber_from_1.1_to_2.0":
    # {
    #     "x_min": 3592,
    #     "x_max": 3918,
    # },
    # "gray_barrier":
    # {
    #     "x_min": 790,
    #     "x_max": 2892,
    # },
    # "gray_with_black_rubber":
    # {
    #     "x_min": 1341,
    #     "x_max": 2890,
    # },
    "metal":
    {
        "x_min": 3646,
        "x_max": 3952,

    },
    # "broken_optical_pair_metalic_barrier_with_black_rubber":
    # {
    #     "x_min": 1235,
    #     "x_max": 3920,
    # },
    "metal with black rubber":
    {
        "x_min": 3616,
        "x_max": 3912,
    },
    "acrylic with black rubber":
    {
        "x_min": 3658,
        "x_max": 3902,
    },
    "acrylic with black pvc":
    {
        "x_min": 3658,
        "x_max": 3902,
    },
    "acrylic":
    {
        "x_min": 3756,
        "x_max": 3910,
    },
    "acrylic with marker":
    {
        "x_min": 3644,
        "x_max": 3906,
    }
}
for test, data in res.items():
    diff = data["x_max"] - data["x_min"]
    res[test]["diff"] = diff

my_cmap = plt.get_cmap("viridis")

diffs = list([data["diff"] for key, data in res.items()])
norm_diffs = np.array(diffs)/(max(diffs))
plt.bar(list(res.keys()), diffs, color=my_cmap(norm_diffs))
plt.xticks(list(res.keys()), list(res.keys()), rotation=10, fontsize=8)
plt.title("Measurement range for different barriers")
plt.savefig("hyst_barriers.png")
