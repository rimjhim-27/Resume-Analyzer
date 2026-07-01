"""
Word cloud generator for resume skills.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

try:
    from wordcloud import WordCloud
    HAS_WORDCLOUD = True
except ImportError:
    HAS_WORDCLOUD = False


def generate_wordcloud(skills: list[str]):
    """
    Generate a word cloud figure from a list of skills.
    Returns a matplotlib Figure, or None if wordcloud not available.
    """
    if not HAS_WORDCLOUD or not skills:
        return None

    text = " ".join(skills)
    wc = WordCloud(
        width=700,
        height=300,
        background_color="white",
        colormap="Blues",
        max_words=50,
        prefer_horizontal=0.9,
    ).generate(text)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout(pad=0)
    return fig
