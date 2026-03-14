from __future__ import annotations


STORY_STEPS = [
    {
        "slug": "Baseline",
        "title": "The Baseline - Earth Before Rapid Warming",
        "year_range": ("1951-01-01", "1970-12-01"),
        "variable": "t2m",
        "region": "Global",
        "caption": (
            "In the mid-20th century, global temperatures were relatively stable. "
            "This 20-year average acts as the baseline for later change."
        ),
        "map_type": "heatmap",
        "highlight": None,
    },
    {
        "slug": "El Nino",
        "title": "The 1998 El Nino - Nature's Warning Shot",
        "year_range": ("1997-07-01", "1998-12-01"),
        "variable": "t2m",
        "region": "Global",
        "caption": (
            "The 1997-98 El Nino pushed global temperatures sharply upward and intensified warming "
            "in the tropical Pacific."
        ),
        "map_type": "anomaly_map",
        "highlight": "Tropical Pacific - El Nino epicenter",
    },
    {
        "slug": "Arctic",
        "title": "Arctic Amplification - The North Is Warming Fastest",
        "year_range": ("2000-01-01", "2023-12-01"),
        "comparison_range": ("1951-01-01", "1970-12-01"),
        "variable": "t2m",
        "region": "Arctic",
        "caption": (
            "The Arctic is warming far faster than the global average. This difference view shows why "
            "polar change is one of the clearest climate signals on Earth."
        ),
        "map_type": "difference_map",
        "highlight": "Arctic region - fastest warming zone",
    },
    {
        "slug": "2023",
        "title": "2023 - The Hottest Year in Human History",
        "year_range": ("2023-01-01", "2023-12-01"),
        "variable": "t2m",
        "region": "Global",
        "caption": (
            "2023 shattered records across the calendar year. The warming trend that looked gradual in "
            "the 20th century becomes impossible to ignore here."
        ),
        "map_type": "anomaly_map",
        "highlight": None,
    },
]
