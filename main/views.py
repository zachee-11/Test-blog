from django.utils import translation
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Article

from django.http import JsonResponse
import openai
from openai.error import RateLimitError

import time

openai.api_key = "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"

def article_list(request):
    articles = Article.objects.all()


    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)


    if 'lang' in request.GET:
        lang_code = request.GET['lang']
        if lang_code in dict(settings.LANGUAGES):
            translation.activate(lang_code)
            response = redirect('article_list')
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response
        

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

    # Je récupérer la langue actuelle depuis le cookie
    lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

    # Si la langue est spécifiée dans la requête GET, je l'active et  je met à jour le cookie
    if 'lang' in request.GET:
        lang_code = request.GET['lang']
        if lang_code in dict(settings.LANGUAGES):
            translation.activate(lang_code)
            response = redirect('article_detail', pk=pk)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response

    # Si aucune langue n'est spécifiée dans la requête, j'utilise la langue du cookie ou la langue par défaut
    if not lang:
        lang = translation.get_language()

    context = {
        'article': article,
        'lang': lang,
        'LANGUAGES': settings.LANGUAGES,
    }

    return render(request, 'main/article_detail.html', context)

def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message['content']
            return JsonResponse({'response': answer})
        except RateLimitError:
            time.sleep(5)  # 5 secodes d'attente
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response.choices[0].message['content']
                return JsonResponse({'response': answer})
            except RateLimitError:
                return JsonResponse({'response': "You have exceeded your API quota. Please try again later."})
    return render(request, 'main/chatbot.html')
