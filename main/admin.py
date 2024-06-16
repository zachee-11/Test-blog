from django.contrib import admin

from main.models import Article

#admin.site.register(Article)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'content')
