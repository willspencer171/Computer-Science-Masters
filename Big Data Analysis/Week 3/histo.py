import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

randoms = np.random.standard_normal(10000)
randoms *= 100 / randoms.max()

print(64.3 >= np.quantile(randoms, 0.98))

fig, ax = plt.subplots(figsize=(8, 6))
fig.set_dpi(100)

sns.histplot(x=randoms, kde=True, ax=ax)

fig.savefig("Images/histogram.png", dpi=100)
