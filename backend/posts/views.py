from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from businesses.models import Business
from posts.models import Post
from posts.serializers import PostSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show(request):
    business = Business.objects.filter(owner=request.user).first()

    if not business:
        return Response({"error": "Business not found"}, status=404)

    posts = Post.objects.filter(business=business)
    serialized_posts = PostSerializer(posts, many=True).data

    response_data = {
        "posts": serialized_posts,
    }

    return Response(response_data)