from django.shortcuts import render, redirect, get_object_or_404
from utils import validators as va
from utils.rands import random_letters
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model


token_generator = PasswordResetTokenGenerator()


def register(request):
    context = {
        'page_settings': {
            'name': _('Cadastro de usuário'),
            'enable_button_styles': True,
            'enable_inputs_styles': True,
        }
    }

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        try:
            user = CustomUser.objects.get(email=email)
            if user.is_check:
                messages.warning(request, _('E-mail já registrado, faça login'))
                return redirect('accounts:login')
            else:
                messages.warning(request, _('E-mail já registrado, verifique seu E-mail informando o Token de acesso'))
                return redirect('accounts:check_email')
        except CustomUser.DoesNotExist:
            pass

        context.update({
            'form_values': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            }
        })

        is_valid = True

        if not va.min_characters(first_name, 2):
            is_valid = False
            messages.error(
                request,
                _('Nome precisa ter no mínimo 2 caracteres')
            )

        if not va.max_characters(first_name, 30):
            is_valid = False
            messages.error(
                request,
                _('Nome só pode ter no maximo 30 caracteres')
            )

        if not va.min_characters(last_name, 2):
            is_valid = False
            messages.error(
                request,
                _('Sobrenome precisa ter no mínimo 2 caracteres')
            )

        if not va.max_characters(last_name, 30):
            is_valid = False
            messages.error(
                request,
                _('sobreome só pode ter no maximo 30 caracteres')
            )

        try:
            validate_email(email)
        except ValidationError:
            is_valid = False
            messages.error(request, _('E-mail invalido, tente outro.'))

        is_strong_password, message = va.is_strong_password(password)
        if not is_strong_password:
            is_valid = False
            messages.error(request, _(f'Senha fraca: {message}'))


        if password != password2:
            is_valid = False
            messages.error(
                request,
                _('As senhas não conferem, tente novamente')
            )

        if is_valid:
            new_user = CustomUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            new_user.set_password(password)
            new_user.save()

            # send e-mail
            send_mail('Token de ativação de conta', f'{new_user.token}', 'super@email.com', [f'{email}',])

            messages.success(
                request,
                _('Conta criada! Verifique seu E-mail para obter o token de atentificação')
            )
            return redirect("accounts:check_email")

    return render(request, 'accounts/register.html', context)


def check_email(request):
    context = {
        'page_settings': {
            'name': _('Verificação de E-mail'),
            'enable_button_styles': True,
            'enable_inputs_styles': True,
        }
    }

    if request.method == "POST":

        email = request.POST.get('email')

        context.update({
            'form_values': {
                'email': email,
            },
        })

        d1 = request.POST.get('d1')
        d2 = request.POST.get('d2')
        d3 = request.POST.get('d3')
        d4 = request.POST.get('d4')
        d5 = request.POST.get('d5')
        d6 = request.POST.get('d6')

        token = d1 + d2 + d3 + d4 + d5 + d6
        try:
            user = CustomUser.objects.get(email=email)

            if user.is_check:
                messages.warning(request, _('E-mail já verificado, faça login'))
                return redirect('accounts:login')

            if token == user.token:
                user.is_check = True
                user.token = ''
                user.save()
                messages.success(
                    request,
                    _('E-mail confirmado com sucesso!, agora faça login')
                )
                return redirect('accounts:login')
            else:
                messages.error(request, _('Token invalido, tente novamente'))
        except CustomUser.DoesNotExist:
            messages.error(request, _('Não exitem solicitações para esse E-mail'))

    return render(request, 'accounts/check_email.html', context)


def login_view(request):
    context = {
        'page_settings': {
            'name': _('Entrar'),
            'enable_button_styles': True,
            'enable_inputs_styles': True,
        }
    }

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            if user.is_check:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, _('E-mail não validado, valide seu E-mail para continuar'))
                return redirect('accounts:check_email')
        else:
            messages.error(request, _('Credenciais invalidas'))
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def password_reset(request):
    context = {
        'page_settings': {
            'name': _('Recuperação de senha'),
            'enable_button_styles': True,
            'enable_inputs_styles': True,
        }
    }

    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user.token = random_letters(6)
            user.save()
            current_site = get_current_site(request)
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            link = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = f'http://{current_site.domain}{link}'
            
            send_mail('Recuperação de senha', f'{reset_url}', 'super@email.com', [f'{email}',])

            return redirect('accounts:password_reset_done', token=user.token)
        except CustomUser.DoesNotExist:
            messages.warning(request, _('Endereço de E-mail não cadastrado'))

    return render(request, 'accounts/password_reset_form.html', context)


def password_reset_done(request, token):
    user = get_object_or_404(CustomUser, token=token)
    email = user.email
    context = {
        'page_settings': {
            'name': _('Confirmação de envio'),
        },
        'email': email,
    }
    return render(request, 'accounts/password_reset_done.html', context)


def password_reset_confirm(request, uidb64, token):

    context = {
        'page_settings': {
            'name': _('Redefinição de senha'),
            'enable_button_styles': True,
            'enable_inputs_styles': True,
        }
    }

    UserModel = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('password2')
            is_valid = True

            is_strong_password, message = va.is_strong_password(password)
            if not is_strong_password:
                is_valid = False
                messages.error(request, _(f'Senha fraca: {message}'))
            
            if password != confirm_password:
                is_valid = False
                messages.error(request, _('As senhas não coincidem.'))

            if is_valid:
                user.set_password(password)
                user.token = ''
                user.save()
                messages.success(request, _('Sua senha foi redefinida com sucesso.'))
                return redirect('accounts:login')
                
            context.update({'validlink': True})
        return render(request, 'accounts/password_reset_confirm.html', context)
    else:
        context.update({'validlink': False})
        return render(request, 'accounts/password_reset_confirm.html', context)