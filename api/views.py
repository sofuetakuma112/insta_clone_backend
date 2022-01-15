from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment

# ユーザーを新規作成する
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer  # 対象となるシリアライザ（データの入出力を扱うクラス）を指定する
    permission_classes = (AllowAny,)  # JWTの認証無しでもアクセスできるようにしている


# プロフィールの新規作成、更新
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()  # Profileを全部取得
    serializer_class = serializers.ProfileSerializer

    # Profileを新規作成する際に呼ばれるメソッド
    def perform_create(self, serializer):
        serializer.save(
            userProfile=self.request.user
        )  # request.userで現在ログインしているユーザーの情報を取得できる


# ログインしているユーザーのプロフィール情報を返してくれる
class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()  # Profileを全部取得
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        # ログインしているユーザーのみを返すようにする
        return self.queryset.filter(userProfile=self.request.user)


# Postの新規作成、更新？
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # Postの全オブジェクトを取得する
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # Commentの全オブジェクトを取得する
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)
