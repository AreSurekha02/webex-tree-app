import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np

st.set_page_config(layout="centered")
st.title("🌳 Webex visualization")

# ✅ Load your Excel dataset directly (must be in same GitHub repo)
df = pd.read_excel("webex_chunk_5.xlsx")

# 🧠 Classify sentiment based on content and score
def classify_sentiment(text, score):
    text = str(text).lower()
    if any(word in text for word in ["excellent", "great", "love", "amazing", "good", "nice", "useful",]) or score >= 4:
        return "Positive"
    elif any(word in text for word in ["bad", "issue", "bug", "terrible", "worst", "poor"]) or score <= 2:
        return "Negative"
    else:
        return "Neutral"

df['Sentiment'] = df.apply(lambda row: classify_sentiment(row['content'], row['score']), axis=1)

# 📊 Group sentiment counts per version
sentiment_counts = df.groupby(['Release Version', 'Sentiment']).size().unstack(fill_value=0).reset_index()

# 📦 Convert to tree data
versions = []
y_position = 2.5
direction = -1

for _, row in sentiment_counts.iterrows():
    versions.append({
        "ver": row['Release Version'],
        "y": y_position,
        "dir": direction,
        "pos": row.get('Positive', 0),
        "neu": row.get('Neutral', 0),
        "neg": row.get('Negative', 0),
        "highlight": "positive" if row.get('Positive', 0) > (row.get('Negative', 0) + row.get('Neutral', 0))
                     else "negative" if row.get('Negative', 0) > (row.get('Positive', 0) + row.get('Neutral', 0))
                     else None
    })
    y_position += 2
    direction *= -1

# 🎨 Begin drawing the tree
fig, ax = plt.subplots(figsize=(12, y_position + 3))
fig.patch.set_facecolor('#e8f5e9')  # light green background
ax.set_xlim(-8, 8)
ax.set_ylim(0, y_position + 3)
ax.axis("off")

# Draw textured trunk using rounded box
trunk = FancyBboxPatch(
    (-0.6, 0), 1.2, y_position + 1,
    boxstyle="round,pad=0.02",
    ec="saddlebrown", fc="saddlebrown", linewidth=3
)
ax.add_patch(trunk)

# Draw curved branches and leaves
for v in versions:
    y = v["y"]
    x_end = v["dir"] * 4.5
    ctrl_x = v["dir"] * 2.5
    ctrl_y = y + 1.5

    # Curved branch using Bezier path
    path_data = [
        (Path.MOVETO, (0, y)),
        (Path.CURVE3, (ctrl_x, ctrl_y)),
        (Path.CURVE3, (x_end, y + 1.2))
    ]
    codes, verts = zip(*path_data)
    path = Path(verts, codes)
    patch = PathPatch(path, facecolor='none', edgecolor='sienna', lw=4)
    ax.add_patch(patch)

    # Version label (bold, larger, higher, clearer)
    ax.text(x_end + 0.5 * v["dir"], y + 1.6, f"v{v['ver']}", fontsize=14, fontweight='bold', color='darkgreen', ha='left' if v["dir"] > 0 else 'right')

    # Custom leaf shapes
    leaf_colors = [("green", v["pos"]), ("orange", v["neu"]), ("red", v["neg"])]
    for color, count in leaf_colors:
        for _ in range(count):
            leaf_x = x_end + np.random.uniform(-0.8, 0.8)
            leaf_y = y + 1.2 + np.random.uniform(-0.6, 0.6)
            leaf = Polygon([
                (leaf_x, leaf_y),
                (leaf_x + 0.2, leaf_y + 0.3),
                (leaf_x, leaf_y + 0.6),
                (leaf_x - 0.2, leaf_y + 0.3)
            ], closed=True, facecolor=color, edgecolor='black', lw=1, zorder=10)
            ax.add_patch(leaf)

    # Blossoms or wilts
    if v["highlight"] == "positive":
        ax.scatter(x_end, y + 2, s=300, color="pink", edgecolors="deeppink", marker="*")
    elif v["highlight"] == "negative":
        ax.scatter(x_end, y + 2, s=150, color="brown", marker="x")

# Timeline markers
for label, ypos in zip(["Jan 2022", "Jul 2022", "Jan 2023", "Jul 2023", "Jan 2024"], range(2, int(y_position + 1), 2)):
    ax.text(0, ypos, label, fontsize=10, ha='center', va='bottom', color='black')

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Positive Review', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Neutral Review', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Negative Review', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='*', color='pink', label='🌸 Blossom (High Praise)', markerfacecolor='pink', markersize=15),
    Line2D([0], [0], marker='x', color='brown', label='🥀 Wilted (High Criticism)', markersize=10)
]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

# Show the tree
st.pyplot(fig)
