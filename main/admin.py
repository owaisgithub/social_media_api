from django.contrib import admin

from main.models import ( User,
                         Post,
                         Comment,
                         Like,
                         Unlike,
                         Follow
                         )

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Unlike)
admin.site.register(Follow)