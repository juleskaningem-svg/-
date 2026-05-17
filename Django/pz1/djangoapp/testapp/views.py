import json
import os
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewsForm



def get_json_file_path():
    json_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(json_dir, exist_ok=True)
    return os.path.join(json_dir, 'testapp.json')


def load_news():
    file_path = get_json_file_path()

    if not os.path.exists(file_path):
        save_news([])
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            news_list = json.load(f)
            news_list.sort(key=lambda x: x.get('pub_date', ''), reverse=True)
            return news_list
    except (json.JSONDecodeError, FileNotFoundError):
        save_news([])
        return []


def save_news(news_list):
    file_path = get_json_file_path()

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)


def get_next_id(news_list):
    if not news_list:
        return 1
    return max((news['id'] for news in news_list), default=0) + 1


# Представления
def home_view(request):
    news_list = load_news()

    # Поиск
    search_query = request.GET.get('q', '')
    if search_query:
        news_list = [news for news in news_list
                     if search_query.lower() in news.get('title', '').lower()]


    paginator = Paginator(news_list, 5)
    page = request.GET.get('page', 1)

    try:
        news_page = paginator.page(page)
    except PageNotAnInteger:
        news_page = paginator.page(1)
    except EmptyPage:
        news_page = paginator.page(paginator.num_pages)

    today = date.today().isoformat()

    context = {
        'news_list': news_page,
        'today': today,
        'search_query': search_query,
    }
    return render(request, 'testapp/home.html', context)


def detail_view(request, news_id):
    news_list = load_news()

    news_item = None
    for news in news_list:
        if news.get('id') == news_id:
            news_item = news
            break

    if not news_item:
        raise Http404("Новость не найдена")

    context = {
        'news': news_item,
    }
    return render(request, 'testapp/detail.html', context)


def add_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)

        if form.is_valid():
            news_list = load_news()

            new_news = {
                'id': get_next_id(news_list),
                'title': form.cleaned_data['title'],
                'summary': form.cleaned_data['summary'],
                'content': form.cleaned_data['content'],
                'pub_date': form.cleaned_data['pub_date'].isoformat(),
            }

            news_list.append(new_news)
            save_news(news_list)

            return redirect('testapp:success')
    else:
        form = NewsForm()

    context = {
        'form': form,
    }
    return render(request, 'testapp/add.html', context)


def success_view(request):
    return render(request, 'testapp/success.html')


def delete_view(request, news_id):
    news_list = load_news()

    news_to_delete = None
    updated_news_list = []

    for news in news_list:
        if news.get('id') == news_id:
            news_to_delete = news
        else:
            updated_news_list.append(news)

    if not news_to_delete:
        raise Http404("Новость не найдена")

    if request.method == 'POST':
        save_news(updated_news_list)
        return redirect('testapp:home')

    context = {
        'news': news_to_delete,
    }
    return render(request, 'testapp/delete_confirm.html', context)


def search_view(request):
    query = request.GET.get('q', '')
    news_list = load_news()

    if query:
        news_list = [news for news in news_list
                     if query.lower() in news.get('title', '').lower()]

    paginator = Paginator(news_list, 5)
    page = request.GET.get('page', 1)

    try:
        news_page = paginator.page(page)
    except PageNotAnInteger:
        news_page = paginator.page(1)
    except EmptyPage:
        news_page = paginator.page(paginator.num_pages)

    context = {
        'news_list': news_page,
        'search_query': query,
        'today': date.today().isoformat(),
    }
    return render(request, 'testapp/home.html', context)