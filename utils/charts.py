"""
Chart generators for the Resume Analyzer dashboard.
All return matplotlib Figure objects for st.pyplot().
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


COLORS = {
    "primary":   "#4F46E5",   # indigo
    "success":   "#10B981",   # emerald
    "danger":    "#EF4444",   # red
    "warning":   "#F59E0B",   # amber
    "neutral":   "#6B7280",   # gray
    "bg":        "#F9FAFB",
    "text":      "#111827",
}


def create_ats_gauge(score: int):
    """Circular gauge chart for ATS score."""
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw={"projection": "polar"})
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    # Determine color based on score
    if score >= 70:
        color = COLORS["success"]
    elif score >= 45:
        color = COLORS["warning"]
    else:
        color = COLORS["danger"]

    # Background arc
    theta = np.linspace(np.pi, 0, 200)
    ax.plot(theta, [1] * 200, linewidth=18, color="#E5E7EB", solid_capstyle="round")

    # Score arc
    score_theta = np.linspace(np.pi, np.pi - (score / 100) * np.pi, 200)
    ax.plot(score_theta, [1] * 200, linewidth=18, color=color, solid_capstyle="round")

    ax.set_ylim(0, 1.5)
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)
    ax.axis("off")

    # Score text
    ax.text(0, 0.05, f"{score}%", ha="center", va="center",
            fontsize=28, fontweight="bold", color=color,
            transform=ax.transData)
    ax.text(0, -0.4, "ATS Score", ha="center", va="center",
            fontsize=10, color=COLORS["neutral"],
            transform=ax.transData)

    plt.tight_layout(pad=0.5)
    return fig


def create_breakdown_radar(breakdown: dict):
    """Radar chart for ATS dimension breakdown."""
    labels = list(breakdown.keys())
    values = [breakdown[k] for k in labels]
    N = len(labels)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles_plot = angles + [angles[0]]
    labels_short = [l.replace(" Match", "").replace("/", "/\n") for l in labels]

    fig, ax = plt.subplots(figsize=(4.5, 4.5), subplot_kw={"polar": True})
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    # Grid rings
    for r in [20, 40, 60, 80, 100]:
        ax.plot(angles_plot[:-1] + [angles_plot[0]],
                [r] * N + [r], color="#E5E7EB", linewidth=0.8, linestyle="--")

    ax.fill(angles_plot[:-1], values, alpha=0.25, color=COLORS["primary"])
    ax.plot(angles_plot, values_plot, color=COLORS["primary"], linewidth=2)
    ax.scatter(angles, values, color=COLORS["primary"], s=40, zorder=5)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels_short, fontsize=8, color=COLORS["text"])
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=6, color=COLORS["neutral"])
    ax.set_ylim(0, 100)
    ax.spines["polar"].set_color("#E5E7EB")

    plt.tight_layout(pad=0.5)
    return fig


def create_skill_bar_chart(matched_skills: list, missing_skills: list):
    """Horizontal grouped bar showing matched vs missing."""
    if not matched_skills and not missing_skills:
        return None

    fig, ax = plt.subplots(figsize=(6, max(3, (len(matched_skills[:8]) + len(missing_skills[:8])) * 0.35 + 1)))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    items = (
        [(s, "Matched") for s in matched_skills[:8]] +
        [(s, "Missing") for s in missing_skills[:8]]
    )
    labels = [i[0] for i in items]
    colors = [COLORS["success"] if i[1] == "Matched" else COLORS["danger"] for i in items]
    values = [1] * len(items)

    y = range(len(labels))
    bars = ax.barh(list(y), values, color=colors, height=0.5, edgecolor="none")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9, color=COLORS["text"])
    ax.set_xticks([])
    ax.spines[["top", "right", "bottom", "left"]].set_visible(False)
    ax.invert_yaxis()

    legend_elements = [
        mpatches.Patch(facecolor=COLORS["success"], label=f"Matched ({len(matched_skills)})"),
        mpatches.Patch(facecolor=COLORS["danger"],  label=f"Missing ({len(missing_skills)})"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8, framealpha=0.7)
    ax.set_title("Skills Match Overview", fontsize=11, fontweight="bold",
                 color=COLORS["text"], pad=10)

    plt.tight_layout(pad=0.8)
    return fig


def create_role_confidence_chart(roles: list):
    """Horizontal bar chart for role confidence scores."""
    if not roles:
        return None

    labels = [r[0] for r in roles]
    values = [r[1] for r in roles]

    bar_colors = []
    for v in values:
        if v >= 60:
            bar_colors.append(COLORS["success"])
        elif v >= 35:
            bar_colors.append(COLORS["warning"])
        else:
            bar_colors.append(COLORS["neutral"])

    fig, ax = plt.subplots(figsize=(5, 2.5))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    y = range(len(labels))
    ax.barh(list(y), values, color=bar_colors, height=0.5, edgecolor="none")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=9, color=COLORS["text"])
    ax.set_xlim(0, 110)
    ax.set_xlabel("Confidence %", fontsize=8, color=COLORS["neutral"])
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#E5E7EB")

    for i, v in enumerate(values):
        ax.text(v + 2, i, f"{v}%", va="center", fontsize=8.5,
                fontweight="bold", color=COLORS["text"])

    ax.set_title("Predicted Role Fit", fontsize=10, fontweight="bold",
                 color=COLORS["text"], pad=8)
    ax.invert_yaxis()
    plt.tight_layout(pad=0.8)
    return fig


def create_section_checklist_fig(found: list, missing: list):
    """Visual checklist of resume sections."""
    all_sections = found + missing
    if not all_sections:
        return None

    fig, ax = plt.subplots(figsize=(4, max(2.5, len(all_sections) * 0.42)))
    fig.patch.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.axis("off")

    for i, section in enumerate(found + missing):
        is_found = section in found
        icon = "[+]" if is_found else "[ ]"
        color = COLORS["success"] if is_found else COLORS["danger"]
        y_pos = 1 - (i / max(len(all_sections), 1)) * 0.85 - 0.08
        marker = "●" if is_found else "○"
        ax.text(0.05, y_pos, f"{marker}  {section}", transform=ax.transAxes,
                fontsize=10, va="center", color=color)

    ax.set_title("Resume Sections", fontsize=10, fontweight="bold",
                 color=COLORS["text"], pad=6)
    plt.tight_layout(pad=0.5)
    return fig
