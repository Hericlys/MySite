from django.shortcuts import redirect
from accounts.models import CustomUser
from django.contrib import messages
from utils.rands import random_letters
from .models import Budget
from django.utils.translation import gettext_lazy as _


def create_budget(request) -> redirect:
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        project_type = request.POST.get('project-type')
        description = request.POST.get('project-description')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                phone=phone_number,
                email=email,
            )
            password = random_letters(k=8)
            user.set_password(password)
            user.save()

        Budget(
            user=user,
            category=project_type,
            description=description,
            status='Recebido'
        ).save()

        messages.success(request, _('Seu pedido foi recebido com sucesso! Entraremos em contato em breve'))
    
    return redirect('pages:home')
