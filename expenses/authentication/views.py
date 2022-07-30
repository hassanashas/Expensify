from curses.ascii import isalnum
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# import Token Generator 
from .utils import token_generator

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({"email_error": "Email is not Valid"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email is already in use"}, status=409)
            
        return JsonResponse({"email_valid": True})




class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username should only contain Alpha-Numeric Characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username has already been taken. "}, status=409)
            
        return JsonResponse({"username_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # contains values, for the case that page is refreshed 

        context = {
            'fieldValues': request.POST
        }

        # Check if user exists with same username 

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'Password Length is too Short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save() 

                # Send Email For Verification 
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))


                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = 'http://' + domain + link

                email_subject = "Welcome to Expensify! Please Activate Your Account"
                email_body = "Hello " + user.username + "!\n\n"
                email_body += "We Welcome you to Expensify! Please Activate your Account using the Following Link: " + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semicolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Your Account has been created successfully')
                return render(request, 'authentication/register.html')



        return render(request, 'authentication/register.html')

        
class VerificationVIew(View):
    def get(self, request, uidb64, token):
        return render(request, 'login')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')