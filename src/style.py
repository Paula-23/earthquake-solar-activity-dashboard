import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.io as pio

# =====================================
# Custom palettes
# =====================================

solar_palette = [
    "#2563EB",
    "#3B82F6",
    "#F97316",
    "#FB923C",
    "#FACC15",
]

earthquake_palette = [
    "#1B6133", # Deep Forest Green (The grounding base)
    "#2E682A", #: Mossy Olive (Transitional seasonal green)
    "#1A8B60", #: Sage Earth (Soft, dusty bridge color)
    "#50B450", 
    "#B2FF66",
    "#F7F749", 
    "#D9A13F", #: Burnt Orange (Autumn leaves & tectonic heat)
    '#B26315', #: Oxidized Copper (Raw mineral & earth crust)
    "#A22F08" #: Deep Umber (The heavy, dark soil)
]


kp_palette = [
    "#FFFFB2",         # pale yellow
    "#FFD700",     # golden yellow
    "#FFA500",        # orange
    "#FF69B4",   # pink
    "#FF1493",# deep pink
    "#8B0058",  # dark magenta
    "#1303A4"   # indigo / reddish-purple
]

# =====================================
# Style configuration
# =====================================

def set_style():
    sns.set_theme(style="whitegrid")
    sns.set_palette(solar_palette)  # default palette
    plt.rcParams.update({
        "figure.figsize": (10,6),
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.titleweight": "bold"
    })
    pio.templates.default = "plotly_white"