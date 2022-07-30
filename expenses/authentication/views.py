from curses.ascii import isalnum
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from validate_email import validate_email

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
        
        messages.success(request, 'Registration is Successful')
        messages.info(request, 'gggg')

        return render(request, 'authentication/register.html')

