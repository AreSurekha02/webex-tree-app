import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import numpy as np

st.set_page_config(layout="centered")
st.title("🌳 Webex Tree of Releases (Realistic Tree Style)")

# Tree data
versions = [
    {"ver": "42.0", "y": 2.5, "dir": -1, "pos": 4, "neu": 1, "neg": 1, "highlight": "positive"},
    {"ver": "42.5", "y": 4.5, "dir": 1, "pos": 3, "neu": 2, "neg": 4, "highlight": "mixed"},
    {"ver": "43.0", "y": 6.5, "dir": -1, "pos": 2, "neu": 1, "neg": 0, "highlight": None},
    {"ver": "43.6", "y": 8.5, "dir": 1, "pos": 0, "neu": 2, "neg": 5, "highlight": "negative"},
    {"ver": "44.0", "y": 10.5, "dir": -1, "pos": 6, "neu": 1, "neg": 0, "highlight": "positive"}
]

fig, ax = plt.subplots(figsize=(10, 13))
ax.set_xlim(-7, 7)
ax.set_ylim(0, 14)
ax.axis("off")

# Draw tree trunk (tapered)
trunk_base = [[-0.6, 0], [0.6, 0], [0.3, 12], [-0.3, 12]]
trunk = Polygon(trunk_base, closed=True, color='saddlebrown')
ax.add_patch(trunk)

# Draw branches, leaves, blossoms/wilts
for v in versions:
    y = v["y"]
    x_end = v["dir"] * 4.5
    angle = 25 if v["dir"] > 0 else -25
    branch_x = [0, x_end * 0.7, x_end]
    branch_y = [y, y + 0.8, y + 1.2]
    ax.plot(branch_x, branch_y, color="sienna", linewidth=4)
    ax.text(x_end + 0.5 * v["dir"], y + 1.3, f"v{v['ver']}", fontsize=12, ha='left' if v["dir"] > 0 else 'right')

    # Leaves
    leaf_colors = (["green"] * v["pos"]) + (["orange"] * v["neu"]) + (["red"] * v["neg"])
    for color in leaf_colors:
        leaf_x = x_end + np.random.uniform(-0.8, 0.8)
        leaf_y = y + 1.2 + np.random.uniform(-0.6, 0.6)
        ax.add_patch(Circle((leaf_x, leaf_y), 0.25, color=color, ec='black', lw=0.5))

    # Blossoms or wilted flowers
    if v["highlight"] == "positive":
        ax.scatter(x_end, y + 2, s=300, color="pink", edgecolors="deeppink", marker="*")
    elif v["highlight"] == "negative":
        ax.scatter(x_end, y + 2, s=150, color="brown", marker="x")

# Timeline
for label, ypos in zip(["Jan 2022", "Jul 2022", "Jan 2023", "Jul 2023", "Jan 2024"], [2, 4, 6, 8, 10]):
    ax.text(0, ypos, label, fontsize=10, ha='center', va='bottom', color='gray')

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Positive Review', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Neutral Review', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Negative Review', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='*', color='pink', label='🌸 Blossom (High Praise)', markerfacecolor='pink', markersize=15),
    Line2D([0], [0], marker='x', color='brown', label='🪰 Wilted (High Criticism)', markersize=10)
]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

st.pyplot(fig)

st.caption("This tree shows Webex versions growing like real branches — with leaves as user reviews (green = positive, red = negative, orange = neutral), and blossoms/wilts based on majority sentiment.")
