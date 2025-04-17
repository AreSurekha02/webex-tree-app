import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.lines import Line2D
import numpy as np

st.set_page_config(layout="centered")
st.title("🌳 Webex Tree of Releases (Real Data)")

# ✅ Load your Excel dataset directly (must be in same GitHub repo)
df = pd.read_excel("webex_chunk_5.xlsx")

# 🧠 Classify sentiment based on content and score
def classify_sentiment(text, score):
    text = str(text).lower()
    if any(word in text for word in ["excellent", "great", "love", "amazing", "good", "nice", "useful"]) or score >= 4:
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
fig, ax = plt.subplots(figsize=(10, y_position + 3))
ax.set_xlim(-7, 7)
ax.set_ylim(0, y_position + 3)
ax.axis("off")

# Draw trunk
trunk_base = [[-0.6, 0], [0.6, 0], [0.3, y_position + 1], [-0.3, y_position + 1]]
trunk = Polygon(trunk_base, closed=True, color='saddlebrown')
ax.add_patch(trunk)

# Draw branches and leaves
for v in versions:
    y = v["y"]
    x_end = v["dir"] * 4.5
    ax.plot([0, x_end * 0.7, x_end], [y, y + 0.8, y + 1.2], color="sienna", linewidth=4)
    ax.text(x_end + 0.5 * v["dir"], y + 1.3, f"v{v['ver']}", fontsize=12, ha='left' if v["dir"] > 0 else 'right')

    # Leaves
    leaf_colors = (["green"] * v["pos"]) + (["orange"] * v["neu"]) + (["red"] * v["neg"])
    for color in leaf_colors:
        leaf_x = x_end + np.random.uniform(-0.8, 0.8)
        leaf_y = y + 1.2 + np.random.uniform(-0.6, 0.6)
        ax.add_patch(Circle((leaf_x, leaf_y), 0.25, color=color, ec='black', lw=0.5))

    # Blossoms or wilts
    if v["highlight"] == "positive":
        ax.scatter(x_end, y + 2, s=300, color="pink", edgecolors="deeppink", marker="*")
    elif v["highlight"] == "negative":
        ax.scatter(x_end, y + 2, s=150, color="brown", marker="x")

# Timeline markers (optional)
for label, ypos in zip(["Jan 2022", "Jul 2022", "Jan 2023", "Jul 2023", "Jan 2024"], range(2, int(y_position + 1), 2)):
    ax.text(0, ypos, label, fontsize=10, ha='center', va='bottom', color='gray')

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Positive Review', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Neutral Review', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Negative Review', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='*', color='pink', label='🌸 Blossom (High Praise)', markerfacecolor='pink', markersize=15),
    Line2D([0], [0], marker='x', color='brown', label='🥀 Wilted (High Criticism)', markersize=10)
]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2)

# Show it!
st.pyplot(fig)
st.caption("This tree is built from your actual Webex review data. Branches = versions, Leaves = reviews (colored by sentiment), and blossoms/wilts show overall version impact.")
