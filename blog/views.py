from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _



def posts(request):
    posts = Post.objects.get_posts()
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_settings': {
            'name': 'Blog',
            'enable_inputs_styles': True,
            'enable_button_styles': True,
        },
        'not_found_text': _('Ops... Parece que ainda não tem posts aqui'),
        'page_obj': page_obj,
    }

    return render(request, "blog/posts.html", context)


@login_required(login_url='accounts:login')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if not post.published:
        raise Http404("Post not found")
    
    context = {
        'page_settings': {
            'name': f'Post: {post.title}',
        },
        'post': post,
    }

    return render(request, 'blog/post_detail.html', context)


def search_posts(request):
    if 'search_value' in request.GET:
        search_value = request.GET.get('search_value')
        posts = Post.objects.get_search(search_value)
        paginator = Paginator(posts, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_settings': {
                'name': f'pesquisa: {search_value[0:6]}...',
                'enable_inputs_styles': True,
                'enable_button_styles': True,
            },
            'not_found_text': _('Ops... Parece que ainda não tem posts aqui'),
            'search_value': search_value,
            'page_obj': page_obj,
        }

        return render(request, "blog/posts.html", context)

    return render(request, "blog/posts.html", context)