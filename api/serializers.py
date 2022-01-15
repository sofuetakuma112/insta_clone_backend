from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # ベースとなるモデルを指定する
        fields = ("id", "email", "password")  # 取り扱いたいパラメーターを記述する
        extra_kwargs = {
            "password": {"write_only": True}
        }  # クライアントから取得した際、passwordプロパティは渡されない

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    # "%Y-%m-%d"の形式に変換する
    # timestampをクライアント側で指定することはないのでread_only=Trueにしている
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "nickName", "userProfile", "created_on", "img")
        # Django側で現在ログインしているユーザーidをuserProfileに割り当てる処理を行う（Profile新規作成時？）ので、クライアント側で指定できないようread_only=Trueにしている
        extra_kwargs = {"userProfile": {"read_only": True}}


class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "userPost", "created_on", "img", "liked")
        extra_kwargs = {
            "userPost": {"read_only": True}
        }  # Django側で現在ログインしているユーザーのidを割り当てる処理を行うのでread_only=True


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text", "userComment", "post")
        extra_kwargs = {"userComment": {"read_only": True}}
