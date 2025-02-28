from django.db.models.signals import post_migrate
from django.dispatch import receiver
from posts.models import Category
from config.constants import POST_CATEGORY_OPTIONS

@receiver(post_migrate)
def populate_categories(sender, **kwargs):
    if sender.name == "posts":  # Ensure it runs only for the "posts" app
        for option in POST_CATEGORY_OPTIONS:
            Category.objects.get_or_create(key=option["key"], label=option["label"])
        print("✅ Categories populated successfully after migration!")
