import psycopg2 as psycopg2
from aifc import Error

from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime
from app_convert_v2.forms import *

# Database connection
try:
    connection = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="test")
    cursor = connection.cursor()
    print("database's ready")
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)


def test_decor(func):
    def wrapped(request):
        key = request.session.session_key
        print(key)
        if request.method == "POST" and 'Content-Type' in request.headers:
            return func(request)
        else:
            return HttpResponse("No Access")

    return wrapped


# main part
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/index')
    else:
        form = UserLoginForm()
    return render(request, "app_convert_v2/login.html", {"form": form})


def index(request):
    search_post_form = search_form(request.POST)
    add_post_form = add_form(request.POST)
    convert_post_form = convert_form(request.POST)
    return render(request, 'app_convert_v2/index.html',
                  {"search_post_form": search_post_form, "add_post_form": add_post_form,
                   "convert_post_form": convert_post_form})


@test_decor
def search(request):
    form = search_form(request.POST)
    if form.is_valid():
        try:
            data = form.cleaned_data
            if not data['time']:
                data['time'] = datetime.now().strftime("%d.%m.%y %H:%M")
            cursor.execute(
                f"SELECT currency, time , value FROM convert WHERE currency = %s and time <= %s ORDER BY TIME DESC "
                f"LIMIT 1;",
                (data['currency'], data['time']))
            currency, time, value = cursor.fetchone()
            ctx = {
                'currency': currency,
                'time': time,
                'value': value
            }
            return JsonResponse(ctx)
        except:
            return HttpResponse("Нет такой даты или валюты")


@test_decor
def add_data(request):
    form = add_form(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        time_data = datetime.now().strftime("%d.%m.%y %H:%M")
        cursor.execute(
            "insert into convert(currency, value, time) VALUES (%s, %s, %s)",
            (data['currency'], data['value'], time_data)
        )
        data['time'] = time_data
        connection.commit()
        return JsonResponse(data)
    return HttpResponse("Error")


@test_decor
def converter_to(request):
    form = convert_form(request.POST)
    if form.is_valid():
        try:
            data = form.cleaned_data
            if not data['time']:
                data['time'] = datetime.now().strftime("%d.%m.%y %H:%M")
            cursor.execute(
                f"SELECT currency, time , value FROM convert WHERE currency = %s and time <= %s ORDER BY TIME DESC "
                f"LIMIT 1;",
                (data['currency'], data['time']))
            currency, time, value = cursor.fetchone()
            cursor.execute(
                f"SELECT currency, time , value FROM convert WHERE currency = %s and time <= %s ORDER BY TIME DESC "
                f"LIMIT 1;",
                (data['currency2'], data['time']))
            currency2, time2, value2 = cursor.fetchone()
            res = (data['money'] * value) / value2
            ctx = {
                "currency": currency2,
                'time': data['time'],
                'result': "%.2f" % res
            }
            return JsonResponse(ctx)
        except:
            return HttpResponse("Нет такой даты или валюты")
