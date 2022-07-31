from django.shortcuts import render
import os 
import json 
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages
# Create your views here.

def index(request):

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preference = None 

    if exists:
        user_preference = UserPreferences.objects.get(user=request.user)
    
    context = {'currencies': currency_data, 'user_preference': user_preference}
    if request.method=='POST':

        currency = request.POST['currency']

        if exists:
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)

        messages.success(request, "Currency Change has been Saved")
    
    return render(request, 'userpreferences/index.html', context) # Get Requests will only Render this. 




    
    


    return render(request, 'userpreferences/index.html', {'currencies': currency_data})


    return render(request, 'userpreferences/index.html')