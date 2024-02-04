from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth import get_user_model

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from orders.models import Order, OrderItem
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart


User = get_user_model()

def authenticate_user(email=None, password=None):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None


def login(request):
    if request.method == 'POST':
        print('post')
        form = UserLoginForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            print('post_valid')
            email = request.POST['email']
            password = request.POST['password']
            print('authenticate')
            user = authenticate_user(email=email, password=password)

            session_key = request.session.session_key
            
            if user:
                auth.login(request, user)
                messages.success(request, 'Ви успішно увійшли в акаунт')

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('main:index'))
    else:
        print('get')
        form = UserLoginForm()
        
    context = {
        'title': 'VELOS - Авторизація',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f'{user.username}, Ви успішно зареєстровані та увійшли в акаунт')
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'VELOS - Регістрація',
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профайл успішно обновлений')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    orders = (
        Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'orderitem_set',
            queryset=OrderItem.objects.select_related('bicycle'),
        )
    ).order_by('id')
    )

    context = {
        'title': 'VELOS - Кабінет',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)


def users_cart(request):
    return render(request, 'users/users_cart.html')


@login_required
def logout(request):
    messages.success(request, f'{request.user.username}, Ви вийшли')
    auth.logout(request)
    return redirect('main:index')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = "Змініть свій пароль"
            message = render_to_string('users/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send() 

            messages.success(request, 'Посилання для зміни пароля було надіслане на ваш email') 
            return redirect('user:login')        

        else:
            messages.error(request, 'Такого Акаунту не існує')
            return redirect("user:forgotPassword")
        
    return render(request, 'users/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Будь-ласка, змініть свій пароль")
        return redirect("user:resetPassword")
    else:
        messages.error(request, "This link has been expired!")
        return redirect("user:login")
    

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Пароль змінено успішно!")
            return redirect("user:login")

        else:
            messages.error(request, "Паролі не співпадають!")
            return redirect("resetPassword")
    else:
        return render(request, 'users/resetPassword.html')
