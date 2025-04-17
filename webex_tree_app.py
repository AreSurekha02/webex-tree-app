import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, Circle
from matplotlib.lines import Line2D
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np

st.set_page_config(layout="wide")
st.title("🌳 Webex Tree of Releases — Artful Visualization")

# Load the dataset
df = pd.read_excel("webex_chunk_5.xlsx")

# Sentiment classification
def classify_sentiment(text, score):
    text = str(text).lower()
    if any(word in text for word in ["excellent", "great", "love", "amazing", "good", "nice", "useful"]) or score >= 4:
        return "Positive"
    elif any(word in text for word in ["bad", "issue", "bug", "terrible", "worst", "poor"]) or score <= 2:
        return "Negative"
    else:
        return "Neutral"

df['Sentiment'] = df.apply(lambda row: classify_sentiment(row['content'], row['score']), axis=1)

sentiment_counts = df.groupby(['Release Version', 'Sentiment']).size().unstack(fill_value=0).reset_index()

# Tree layout setup
y_base = 2.5
direction = -1
versions = []
for _, row in sentiment_counts.iterrows():
    versions.append({
        "ver": row['Release Version'],
        "y": y_base,
        "dir": direction,
        "pos": row.get('Positive', 0),
        "neu": row.get('Neutral', 0),
        "neg": row.get('Negative', 0),
        "highlight": "positive" if row.get('Positive', 0) > (row.get('Neutral', 0) + row.get('Negative', 0))
                     else "negative" if row.get('Negative', 0) > (row.get('Positive', 0) + row.get('Neutral', 0))
                     else None
    })
    y_base += 2
    direction *= -1

fig, ax = plt.subplots(figsize=(16, y_base + 4))
fig.patch.set_facecolor('#f0fdf4')
ax.set_xlim(-10, 10)
ax.set_ylim(0, y_base + 4)
ax.axis("off")

# Tree trunk
trunk = FancyBboxPatch(
    (-0.5, 0), 1.0, y_base + 1.5,
    boxstyle="round,pad=0.02", linewidth=4, fc='#8B5A2B', ec='#5c4033', zorder=1
)
ax.add_patch(trunk)

# Branches and leaves
for v in versions:
    y = v['y']
    x_end = v['dir'] * 5
    ctrl_x = v['dir'] * 2.5
    ctrl_y = y + 1.2

    path_data = [
        (Path.MOVETO, (0, y)),
        (Path.CURVE3, (ctrl_x, ctrl_y)),
        (Path.CURVE3, (x_end, y + 1.5))
    ]
    path = Path(*zip(*path_data))
    ax.add_patch(PathPatch(path, lw=3, edgecolor='#A0522D', facecolor='none', zorder=2))

    # Version label
    ax.text(x_end + 0.6 * v['dir'], y + 1.7, f"v{v['ver']}", fontsize=14, fontweight='bold', color='#2E8B57', ha='left' if v['dir'] > 0 else 'right')

    # Draw leaves (diamond shape with some rotation)
    leaf_data = [("green", v["pos"]), ("orange", v["neu"]), ("red", v["neg"])]
    for color, count in leaf_data:
        for _ in range(count):
            lx = x_end + np.random.uniform(-0.7, 0.7)
            ly = y + 1.5 + np.random.uniform(-0.7, 0.7)
            leaf = Polygon([
                (lx, ly),
                (lx + 0.15, ly + 0.2),
                (lx, ly + 0.4),
                (lx - 0.15, ly + 0.2)
            ], closed=True, facecolor=color, edgecolor='black', lw=0.7, zorder=3)
            ax.add_patch(leaf)

    # Highlight bloom/wilt
    if v['highlight'] == "positive":
        ax.scatter(x_end, y + 2.2, s=250, marker="*", color='deeppink', zorder=4)
    elif v['highlight'] == "negative":
        ax.scatter(x_end, y + 2.2, s=150, marker="x", color='brown', zorder=4)

# Timeline markers
for label, ypos in zip(["Jan 2022", "Jul 2022", "Jan 2023", "Jul 2023", "Jan 2024"], range(2, int(y_base + 2), 2)):
    ax.text(0, ypos, label, fontsize=10, ha='center', va='bottom', color='gray')

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Positive Review', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Neutral Review', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Negative Review', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='*', color='deeppink', label='🌸 Blossom (High Praise)', markersize=15),
    Line2D([0], [0], marker='x', color='brown', label='🥀 Wilted (High Criticism)', markersize=10)
]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

# Display final tree
st.pyplot(fig)
st.caption("An organic tree design with curved branches, leaf clusters, and version blossoms. Real review sentiment now flourishes visually.")
