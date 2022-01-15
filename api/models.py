from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

# instanceはProfileクラスのインスタンス
# ファイルを保存するURLを返す
# avatarsディレクトリ下に追加していく
def upload_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        [
            "avatars",
            str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext),
        ]
    )  # instance.userProfile.idは、Profileに紐付いたUserモデルのid


# postsディレクトリ下に追加していく
def upload_post_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(
        ["posts", str(instance.userPost.id) + str(instance.title) + str(".") + str(ext)]
    )


# AbstractBaseUserを拡張する場合、create_userとcreate_superuserメソッドを定義しているUserManagerというクラスも修正する必要がある
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("email is must")

        user = self.model(email=self.normalize_email(email))  # model関数でインスタンスを作成する
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Django既存のUserモデルを拡張したカスタムユーザーモデルを作る
class User(AbstractBaseUser, PermissionsMixin):
  
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # views.pyなどでUserモデルの情報を参照するときに使う

    USERNAME_FIELD = "email"

    # 組み込み関数 format(), print() を使うときに呼び出されるメソッド
    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    # CASCADEとすることで、紐付いたUserモデルが削除された際にProfileモデルも自動で削除されるようになる
    # Userモデルを紐付ける
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="userProfile", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )  # auto_now_add=Trueとすることで、インスタンス生成時にタイムスタンプを取得する
    img = models.ImageField(
        blank=True, null=True, upload_to=upload_avatar_path
    )  # blank=True, null=Trueとすると画像の登録が任意になる

    def __str__(self):
        return self.nickName


class Post(models.Model):
    title = models.CharField(max_length=100)
    # ForeignKeyでone-to-manyを表現している
    # Userモデルと紐付ける
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userPost", on_delete=models.CASCADE
    )  # 引数のUserモデルが複数のPostモデルを所有する(one-to-many)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked", blank=True
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    # 誰によるコメントか
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="userComment", on_delete=models.CASCADE
    )  # 引数のUserモデルが複数のCommentモデルを所有する(one-to-many)
    # どの投稿へのコメントか
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE  # 既存の投稿が入るからPost?
    )  # 引数のPostモデルが複数のCommentモデルを所有する(one-to-many)

    def __str__(self):
        return self.text
