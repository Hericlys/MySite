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