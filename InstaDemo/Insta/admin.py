from django.contrib import admin
from Insta.models import Post
from Insta.models import InstaUser
from Insta.models import Like
from Insta.models import Comment
from Insta.models import UserConnection
# Register your models here.

admin.site.register(Post)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(UserConnection)
