
from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import PasswordResetForm
# from .models import PasswordResetToken
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, login
# from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import EmailMessage


User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('/forgot-password/')

        # Create a password reset token and send an email to the user
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        mail_subject = 'Reset your password'

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        password_reset_url = f"http://{request.get_host()}/reset-password/{uid}/{token}/"

        # import pdb; pdb.set_trace()
        # Send the email
        context= {
            'user': user.first_name,
            'password_reset_url': password_reset_url,
        }
        mail_subject = 'Password Reset Request'
        message = render_to_string('account/password_reset_email.html',context=context )


        # send_mail(mail_subject, message, 'kaushik11cool@gmail.com', [email])

        msg = EmailMessage(mail_subject, message, 'kaushik11cool@gmail.com',  [email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

        messages.success(request, 'An email has been sent with instructions to reset your password.')
        return redirect('/')
    return render(request, 'account/forgot_password.html')



def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password = request.POST['password']
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('/')
            return render(request, 'account/reset_password.html', {'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, 'Invalid password reset link.')
            return redirect('/')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('/')




def home_1(request):
    # return render(request, 'account/login_old.html')
    return render(request, 'account/login.html')


def home(request):

    if request.method == 'POST':

        # import pdb; pdb.set_trace()
        # username = request.POST['username']
        email_id = request.POST['email_id']
        password = request.POST['password']
        # import pdb;
        # pdb.set_trace()
        if request.user.is_authenticated:
            return redirect('bsn_card/')
        else:

            user = auth.authenticate(request, username=email_id, password=password)
            # user = authenticate(request, email=email_id, password=password)

            if user is not None:
                login(request, user)
                print('inside autherncate.')
                messages.success(request,'Welcome to Business card application')
                return redirect('bsn_card/')
            else:
                # messages.info(request, 'invalid credentials')
                print("Ravi..31.....not authencater.")
                # messages.success(request, 'Data submitted successfully!')
                messages.error(request, 'User does not exist.')
                print("Ravi...33....not authencater.")

                return redirect('/')
                # return render(request,'account/login.html')
    else:
     # return redirect('/')
     return render(request, 'account/login.html')
# # print('........outside')
    # return render(request, 'account/login.html')
    #



def register(request):
    if request.method == 'POST':
        # try:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        email = request.POST['email']
        # except Exception as e:
        #     messages.warning(request, 'Please fill first ,last name, email id and password')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'User name is already registered.')
                return redirect('/registration')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email id is already registered.')
                return redirect('/registration')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                messages.success(request,'user is successfully created.')
                print('70............','user is successfully created.')
                return render(request,'account/login.html')

        else:
            # messages.error(request, 'This is an error message.')
            print('70............', 'password not matching.')
            messages.error(request,'Password are not matching.')
            return redirect('/registration')
             # return redirect('/')

    else:
        return render(request, 'account/registration.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

