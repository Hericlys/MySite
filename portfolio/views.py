from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from .models import Project


def projects(request):
    projects = Project.objects.get_projects()
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_settings': {
            'name': _('Portfólio'),
            'enable_inputs_styles': True,
            'enable_button_styles': True,
        },
        'not_found_text': _('Ops... Parece que ainda não tem projects aqui'),
        'page_obj': page_obj,
    }

    return render(request, "portfolio/projects.html", context)


def search_projects(request):
    if 'search_value' in request.GET:
        search_value = request.GET.get('search_value')
        projects = Project.objects.get_search(search_value)
        paginator = Paginator(projects, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_settings': {
                'name': f'pesquisa: {search_value[0:6]}...',
                'enable_inputs_styles': True,
                'enable_button_styles': True,
            },
            'not_found_text': _('Ops... Parece que ainda não tem projects aqui'),
            'search_value': search_value,
            'page_obj': page_obj,
        }

        return render(request, "portfolio/projects.html", context)
    
    return render(request, "portfolio/projects.html", context)
