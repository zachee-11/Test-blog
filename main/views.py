from django.utils import translation
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Article

def article_list(request):
    articles = Article.objects.all()

    # Récupérer la langue actuelle depuis le cookie
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

    # Si la langue est spécifiée dans la requête GET, l'activer et mettre à jour le cookie
    if 'lang' in request.GET:
        lang_code = request.GET['lang']
        if lang_code in dict(settings.LANGUAGES):
            translation.activate(lang_code)
            response = redirect('article_list')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response

    # Si aucune langue n'est spécifiée dans la requête, utiliser la langue du cookie ou la langue par défaut
    if not lang:
        lang = translation.get_language()

    context = {
        'articles': articles,
        'lang': lang,
        'LANGUAGES': settings.LANGUAGES
    }

    return render(request, 'main/article_list.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # Récupérer la langue actuelle depuis le cookie
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

    # Si la langue est spécifiée dans la requête GET, l'activer et mettre à jour le cookie
    if 'lang' in request.GET:
        lang_code = request.GET['lang']
        if lang_code in dict(settings.LANGUAGES):
            translation.activate(lang_code)
            response = redirect('article_detail', pk=pk)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response

    # Si aucune langue n'est spécifiée dans la requête, utiliser la langue du cookie ou la langue par défaut
    if not lang:
        lang = translation.get_language()

    context = {
        'article': article,
        'lang': lang,
        'LANGUAGES': settings.LANGUAGES,
    }

    return render(request, 'main/article_detail.html', context)
