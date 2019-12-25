#!/usr/bin/env python3
# !-*-coding:utf-8 -*-
import json
from utils.captcha_util import judge_captcha, build_captcha
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from migrations import models
from matplotlib import pyplot as plt
import matplotlib; matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码


def jump_page(key):
    if key == 'administer':
        return redirect('/administer/')
    if key == 'index':
        return redirect('/index/')
    if key == 'register':
        return redirect('/register/')
    if key == 'login':
        return redirect('/login/')


def login(request, captcha_dict):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)

    # 判断验证码输入是否正确
    capt = request.POST.get("captcha", None)
    key = request.POST.get("hash_key", None)
    if not judge_captcha(capt, key):
        message = "验证码错误！"
        return render(request, 'login.html', {'message': message, 'captcha': captcha_dict})
    else:
        if username and password:
            username = username.strip()
            if username == "admin" and password == "admin":
                # 管理员
                return redirect('/administer/')
            try:
                name = models.UserInfo.objects.get(user=username)
                if name.pwd == password and name.adminCheck == True:
                    request.session['username'] = username
                    return redirect('/index/')
                else:
                    message = "密码错误！"
                    return render(request, 'login.html', {'message': message, 'captcha': captcha_dict})
            except Exception as e:
                message = "该用户不存在！"
                return render(request, 'login.html', {'message': message, 'captcha': captcha_dict})
        else:
            message = "输入不能为空"
            return render(request, 'login.html', {'message': message, 'captcha': captcha_dict})


def register(request):
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    repeat_password = request.POST.get("repeat_password", None)

    if username and password and repeat_password:
        username = username.strip()
        try:
            # 查找用户名是否已经存在
            models.UserInfo.objects.get(user=username)
            message = "用户名已存在"
            return render(request, 'register.html', {'message': message})
        except Exception as e:
            if password != repeat_password:
                message = "两次输入密码不相同"
                return render(request, 'register.html', {'message': message})
            else:
                data = models.UserInfo(user=username, pwd=password)
                data.save()
                message = "注册成功"
                return render(request, 'login.html', {'message': message})


def refresh_captcha():
    return HttpResponse(json.dumps(build_captcha()), content_type='application/json')

