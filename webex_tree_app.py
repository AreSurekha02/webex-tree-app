import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

st.set_page_config(layout="centered")
st.title("🌳 Webex Tree of Releases (2022–2024)")

# Tree data
versions = [
    {"ver": "42.0", "y": 3, "dir": -1, "pos": 4, "neu": 1, "neg": 1, "highlight": "positive"},
    {"ver": "42.5", "y": 5, "dir": 1, "pos": 3, "neu": 2, "neg": 4, "highlight": "mixed"},
    {"ver": "43.0", "y": 7, "dir": -1, "pos": 2, "neu": 1, "neg": 0, "highlight": None},
    {"ver": "43.6", "y": 9, "dir": 1, "pos": 0, "neu": 2, "neg": 5, "highlight": "negative"},
    {"ver": "44.0", "y": 11, "dir": -1, "pos": 6, "neu": 1, "neg": 0, "highlight": "positive"}
]

fig, ax = plt.subplots(figsize=(10, 12))
ax.set_xlim(-10, 10)
ax.set_ylim(0, 15)
ax.axis("off")

# Draw trunk
trunk_top = 14
trunk_bottom = 1
trunk_width = 0.8
ax.add_patch(plt.Rectangle((-trunk_width/2, trunk_bottom), trunk_width, trunk_top - trunk_bottom, color='saddlebrown'))

# Draw branches, leaves, highlights
for v in versions:
    x_start, y = 0, v["y"]
    x_end = v["dir"] * 5
    ax.plot([x_start, x_end], [y, y], color="peru", linewidth=4)
    ax.text(x_end + 0.6 * v["dir"], y, f"v{v['ver']}", fontsize=12, va="center", ha="left" if v["dir"] > 0 else "right")

    leaf_colors = (["green"] * v["pos"]) + (["orange"] * v["neu"]) + (["red"] * v["neg"])
    for color in leaf_colors:
        leaf_x = x_end + np.random.uniform(-0.5, 0.5)
        leaf_y = y + np.random.uniform(-0.5, 0.5)
        ax.add_patch(Circle((leaf_x, leaf_y), 0.2, color=color, ec='black'))

    if v["highlight"] == "positive":
        ax.scatter(x_end, y + 0.7, s=300, color="pink", edgecolors="deeppink", marker="*")
    elif v["highlight"] == "negative":
        ax.scatter(x_end, y + 0.7, s=150, color="brown", marker="x")

# Add timeline
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

st.caption("Leaves represent user reviews: \\nGreen = Positive, Orange = Neutral, Red = Negative.\\nBranches are versions, and blossoms/wilts show sentiment highlights.")
