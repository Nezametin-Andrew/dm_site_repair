from django.contrib import admin
from .models import *


class TagAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, TagAdmin)
admin.site.register(Category, TagAdmin)
admin.site.register(AnonymousUser)
admin.site.register(Visit)
admin.site.register(ViewArticle)
admin.site.register(LikeArticle)
admin.site.register(DisLikeArticle)
admin.site.register(IpAddress)

admin.site.register(NotAccessPath)
