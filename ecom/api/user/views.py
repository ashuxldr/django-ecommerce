import re
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import CustomUser
from rest_framework import viewsets
from django.http import JsonResponse
from .serializers import UserSerializer
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
# Create your views here


def generate_session_token(length=10):
    list1 = [chr(i) for i in range(65, 91)]
    list2 = [str(i) for i in range(10)]
    list3 = ''.join(random.SystemRandom().choice(list1 + list2) for _ in range(length))
    return list3


@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'send a post request with valid parameter'})
    username = request.POST['email']
    password = request.POST['password']
    print(username)
    print(password)

    if not re.match("/\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b/gi", username):
        return JsonResponse({'error': 'Enter a valid email'})
    if len(password) < 3:
        return JsonResponse({'error': 'Enter Password greater than equal to three characters'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password')

            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error': "previous session exists"})

            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': usr_dict})
        else:
            return JsonResponse({'error': 'Invalid Password'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})


def signout(request, id):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'
        user.save()
        logout(request)
    except UserModel.DoesNotExist:
        return JsonResponse({
            'error': 'Invalid User ID'
        })
    return JsonResponse({
        'success': "Logout success"
    })


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
        
#
# class ProfileView(View, LoginRequiredMixin):
#
#     def get(self, request):
#             return render(request, 'index/profile.html')
#
#     def post(self, request):
#             user = User.objects.get(id=request.user.id)
#             user.username = request.POST.get('username')
#             user.email = request.POST.get('email')
#             profile_pic, created = models.Profile.objects.get_or_create(owner=request.user)
#             f = request.FILES.get('profilepic')
#             if isinstance(f, InMemoryUploadedFile):
#                 bytearr = f.read()
#                 profile_pic.content_type = f.content_type
#                 profile_pic.picture = bytearr
#                 print(profile_pic)
#             profile_pic.save()
#
#             password = request.POST.get('password')
#             if password:
#                 user.set_password(password)
#                 user.save()
#                 return redirect('login')
#             user.save()
#             return redirect('profile')
#
#     def stream_file(request):
#         pic, created = models.Profile.objects.get_or_create(owner = request.user)
#         response = HttpResponse()
#         response['Content-Type'] = pic.content_type
#         response['Content-Length'] = len(pic.picture)
#         response.write(pic.picture)
#         return response














