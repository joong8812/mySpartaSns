from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 데이터베이스 안에 있는 검사하는 함수
from django.contrib import auth


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            # 기존에 있는 유저인지 확인
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')

            UserModel.objects.create_user(
                username=username, password=password, bio=bio)
            # new_user = UserModel()
            # new_user.username = username
            # new_user.password = password
            # new_user.bio = bio
            # new_user.save()

        return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, username=username, password=password)
        # me = UserModel.objects.get(username=username)
        if me is not None:
            auth.login(request, me)
            # request.session['user'] = me.username
            return HttpResponse(me.username)  # 로그인 후 유저네임을 응답한다
        else:
            return redirect('/sign-in')
    elif request.method == 'GET':
        return render(request, 'user/signin.html')
