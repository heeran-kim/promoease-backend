# config/constants.py
# User Roles (Used in users/models.py & users/managers.py)
ROLE_CHOICES = [
    {"key": "admin", "label": "Admin"},
    {"key": "business_owner", "label": "Business Owner"},
]

DEFAULT_ROLE = "business_owner"
DEFAULT_LOGO_URL = "/static/images/default_logo.png"

# Social Media Platforms (Used in social/models.py & posts/models.py)
SOCIAL_PLATFORMS = [
    {"key": "instagram", "label": "Instagram"},
    {"key": "facebook", "label": "Facebook"},
    {"key": "twitter", "label": "Twitter / X"},
    {"key": "threads", "label": "Threads"},  # Fixed from "thread" to "threads"
]

# Post Categories (Used in posts/models.py)
POST_CATEGORIES_OPTIONS = [
    {"key": "brand_story", "label": "Brand Story"},
    {"key": "product_highlight", "label": "Product Highlight"},
    {"key": "deal_discount", "label": "Deals & Discounts"},
    {"key": "limited_time", "label": "Limited-Time Offer"},
    {"key": "business_update", "label": "Business Update"},
]

POST_STATUS_OPTIONS = [
    ('scheduled', 'Scheduled'),
    ('posted', 'Posted'),
    ('failed', 'Failed'),
]

# Promotion Categories (Used in posts/models.py)
PROMOTION_CATEGORIES_OPTIONS = [
    {"key": "discount", "label": "Deals & Discounts"},
    {"key": "bundle", "label": "Combos & Bundles"},
    {"key": "trend", "label": "Trending Now"},
    {"key": "menu", "label": "New Menu Ideas"},
    {"key": "social", "label": "Social Media Content"},
]
