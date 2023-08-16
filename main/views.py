from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User
from main.models import Follow
from main.models import Comment
from main.models import Post
from main.models import Like
from main.models import Unlike

from main.serializers import UserSerializer
from main.serializers import PostSerializer
from main.serializers import CommentSerializer


def get_token_for_user(user):
    token = RefreshToken.for_user(user)
    return {
        'token': str(token.access_token)
    }

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = auth.authenticate(email = email, password = password)
        if user is not None:
            auth_token = get_token_for_user(user)
            data = {
                'token': auth_token['token']
            }
            return Response(data)
        return Response({'detail': 'invalid credentials'})


class UserView(APIView):
    def get(self, request):
        user_serializer = UserSerializer(request.user)
        email = user_serializer.data.get('email')
        user_id = user_serializer.data.get('id')
        user = User.objects.get(id = user_id)

        followers = user.follower_set.all()
        following = user.following_set.all()

        data = {
            'username': email,
            'followers': len(following),
            'following': len(followers)
        }
        return Response(data)
    

class FollowView(APIView):
    def post(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        user_serializer = UserSerializer(request.user)
        follower = User.objects.get(id = user_serializer.data.get('id'))
        following = User.objects.get(id = id)
        follow = Follow.objects.create(follower = follower, following = following)
        follow.save()
        return Response({'msg': 'Followed'})


class UnfollowView(APIView):
    def post(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        user_serializer = UserSerializer(request.user)
        follow = Follow.objects.get(follower_id = user_serializer.data.get('id'), following_id=id)
        follow.delete()
        return Response({'msg': 'Unfollowed'})
    
class PostView(APIView):
    def get(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        data = {}
        post = Post.objects.get(id = id)
        post_serializer = PostSerializer(post)
        likes = len(Like.objects.filter(post = post))
        data = {
            'post': post_serializer.data,
            'likes': likes
        }
        comments = Comment.objects.filter(post = post).order_by('created_at')
        comment_list = []
        for comment in comments:
            comment_list.append(CommentSerializer(comment).data)
        
        
        data['comments'] = comment_list
        return Response(data)


    def post(slef, request):
        user_serializer = UserSerializer(request.user)
        user = User.objects.get(id = user_serializer.data.get('id'))
        title = request.data.get('title')
        description = request.data.get('description')

        if title is None:
            return Response({'error': 'Title is Missing'})
        if description is None:
            return Response({'error': 'Description is Missing'})
        

        post = Post.objects.create(title = title, description = description, user = user)
        post.save()
        data = {
            'PostID': post.id,
            'Title': post.title,
            'Description': post.description,
            'Created': post.created_at
        }

        return Response(data)
    
    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        post = Post.objects.get(id = id)
        comment = Comment.objects.filter(post = post)
        like = Like.objects.filter(post = post)
        unlike = Unlike.objects.filter(post = post)
        if post is not None:
            post.delete()
        if comment is not None:
            comment.delete()
        if like is not None:
            like.delete()
        if unlike is not None:
            unlike.delete()

        return Response({"msg": "deleted"})
    
class AllPostView(APIView):
    def get(self, request):
        data = []
        user_serializer = UserSerializer(request.user)
        user = User.objects.get(id = user_serializer.data.get('id'))
        posts = Post.objects.filter(user = user).order_by('created_at')
        for post in posts:
            item = {}
            item['post'] = PostSerializer(post).data
            # item.append({'post': PostSerializer(post).data})
            item['likes'] = len(Like.objects.filter(post = post))
            comment_list = Comment.objects.filter(post = post)
            comments = []
            for comment in comment_list:
                comments.append(CommentSerializer(comment).data)
            item['comments'] = comments

            data.append(item)
        return Response(data)
    

class LikeView(APIView):
    def post(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        user_serializer = UserSerializer(request.user)
        user = User.objects.get(id = user_serializer.data.get('id'))
        post = Post.objects.get(id = id)
        like = Like.objects.create(like = True, user = user, post = post)
        like.save()
        return Response({'msg':'Liked'})
    
class UnlikeView(APIView):
    def post(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        user_serializer = UserSerializer(request.user)
        user = User.objects.get(id = user_serializer.data.get('id'))
        post = Post.objects.get(id = id)
        unlike = Unlike.objects.create(unlike = True, user = user, post = post)
        unlike.save()
        return Response({'msg':'Unliked'})
    
class CommentView(APIView):
    def post(self, request, id=None):
        if id is None:
            return Response({'error': 'URL not found'})
        
        user_serializer = UserSerializer(request.user)
        user = User.objects.get(id = user_serializer.data.get('id'))
        post = Post.objects.get(id = id)
        comment = request.data.get('comment')

        comment_obj = Comment.objects.create(comment = comment, user = user, post = post)
        comment_obj.save()

        return Response({'CommentID': comment_obj.id})

