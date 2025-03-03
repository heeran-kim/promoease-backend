from django.db.models.signals import post_migrate
from django.dispatch import receiver
from promotions.models import PromotionCategories
from config.constants import PROMOTION_CATEGORIES_OPTIONS

@receiver(post_migrate)
def populate_promotion_categories(sender, **kwargs):
    if sender.name == "promotions":
        for option in PROMOTION_CATEGORIES_OPTIONS:
            PromotionCategories.objects.get_or_create(key=option["key"], label=option["label"])
        print("✅ Promotion Categories populated successfully after migration!")