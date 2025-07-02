from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login

@csrf_exempt 
def user_authentication_view(request):
    if request.method == 'POST':  # ✅ Use POST, not GET with body
        try:
            info = json.loads(request.body)
            username = info["username"]
            password = info["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = generate_jwt(user)  # ✅ issue JWT
                return JsonResponse({
                    "message": "Login successful",
                    "token": token,
                    "username": user.username,
                })
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)

    
        # if User.objects.filter(username=username, password=password).exists():
        #     return HttpResponse("Access granted!")
        # else:
        #     pass
        # return HttpResponse("Data Saveddddd")
# Create your views here.
@csrf_exempt
def user_creation_view(request):
    if request.method == 'POST':
        print(dir(request), request.body)
        info = json.loads(request.body)    
        username = info["username"]
        password = info["password"]
        email = info["email"]
        if User.objects.filter(username = username, email = email).exists():
            print("User Exists!")
            raise ValueError("User repeated")
        else:
            print("You think user does not exist")
            p = User(username=username, email = email)
            p.set_password(password)
            p.is_staff = True
            p.save(force_insert=True)
            
        return HttpResponse("Data Saved")

@csrf_exempt
def user_filter(request):
    if request.method == 'GET':
        return JsonResponse(User.objects.all())

from .utils import generate_jwt

# @csrf_exempt
# def login_view(request):
    
#     if user:
#         token = generate_jwt(user)  # <--- called here
#         return JsonResponse({'token': token}) 