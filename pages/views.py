from django.shortcuts import render
from portfolio.models import Project


def home(request) -> render:
    """
        view responsible for rendering the home page
    """
    context = {
        'page_settings': {
            'name': 'Home',
            'enable_button_styles': True,
            'enable_inputs_styles': True,
        }
    }
    projects = Project.objects.get_projects()[:2]
    
    if projects:
        context.update({'projects':projects})
    
    return render(request, 'pages/home.html', context)