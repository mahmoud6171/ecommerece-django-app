from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.auth.models import User

from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html', {
            
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            
            })

            user.email_user(subject=subject, message=message)

            messages.success(request, 'Account was created successfully')
            return redirect('email-verification-sent')
    
    context = {'form': form}
    return render(request, 'account/registration/register.html', context)

def email_verification(request, uidb64, token):

    # uniqueid

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)
    
    # Success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')


    # Failed 

    else:

        return redirect('email-verification-failed')


def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')



def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')


def my_login(request):
    
    form = LoginForm()
    if request.method =='POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login successful')
                return redirect("dashboard")
            else:
                messages.error(request, 'Username or password is incorrect')
    context = {'form': form}
    return render(request, 'account/my-login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('store')



@login_required(login_url='my-login')
def dashboard(request):


    return render(request, 'account/dashboard.html')


@login_required(login_url='my-login')
def profile_management(request):

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Account was updated successfully')
            return redirect('dashboard')
    

    user_form = UpdateUserForm(instance=request.user)

    context = {'user_form': user_form}

    return render(request, 'account/profile-management.html', context)


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Account was deleted successfully')
        return redirect('dashboard')

    return render(request, 'account/delete-account.html')


# Shipping view
@login_required(login_url='my-login')
def manage_shipping(request):

    try:
        shipping = ShippingAddress.objects.get(user = request.user.id)

    except ShippingAddress.DoesNotExist:
        shipping = None

    form = ShippingAddressForm(instance=shipping)

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping)
        if form.is_valid():
            shipping_user = form.save(commit = False)
            shipping_user.user = request.user
            shipping_user.save()

            messages.success(request, 'Shipping address was updated successfully')
            return redirect('dashboard')
    
    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context)
        

