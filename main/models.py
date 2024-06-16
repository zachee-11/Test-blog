from django.db import models
#from modeltranslation.translator import TranslationOptions, register
#from modeltranslation.fields import TranslationField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100) 
    def __str__(self):
        return self.title
'''''
@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'publication_date',)
    '''