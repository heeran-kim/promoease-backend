from rest_framework.response import Response
from rest_framework.decorators import api_view
from businesses.models import Business
from social.models import SocialMedia
from posts.models import Post

@api_view(["GET"])
def get_dashboard_data(request):
    business = Business.objects.filter(owner=request.user).first()

    if not business:
        return Response({"error": "Business not found"}, status=404)

    social_media = SocialMedia.objects.filter(business=business)
    social_media_data = [
        {
            "platform": sm.platform,
            "link": sm.link,
            "username": sm.username,
        }
        for sm in social_media
    ]

    posts = Post.objects.filter(business=business)
    last_post = posts.order_by("-created_at").first()

    posts_summary = {
        "upcomingPosts": posts.filter(status="upcoming").count(),
        "uploadedPosts": posts.filter(status="uploaded").count(),
        "failedPosts": posts.filter(status="failed").count(),
        "lastActivity": last_post.created_at.strftime("%Y-%m-%d %H:%M:%S") if last_post else None,
        "lastPostLink": last_post.link if last_post else None,
    }

    response_data = {
        "business": {
            "name": business.name,
            "logo": business.logo.url if business.logo else "",
        },
        "socialMedia": social_media_data,
        "postsSummary": posts_summary,
    }

    return Response(response_data)