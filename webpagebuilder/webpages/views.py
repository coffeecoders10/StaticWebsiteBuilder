from django.shortcuts import render
from .models import Webpages
from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
import re
import os

def login(request):
    if request.method == "POST":
        password = request.POST.get('password')
        next = request.POST.get('next')
        if password != "council":
            return render(request,'webpages/login.html', {"all_webpages": all_webpages,"error": "Wrong Password"})
        if next == "create":
            webpage_name = request.POST.get('webpage_name')
            if webpage_name == "":
                return render(request,'webpages/login.html', {"all_webpages": all_webpages,"error": "Enter Valid Website Name"})
            render_path = "webpages/websites/" + webpage_name + ".html"
            path = "webpages/templates/" + render_path
            new_webpage = Webpages(name=webpage_name, path=path, render_path=render_path)
            new_webpage.save()
            request.session["curr_webpage"] = webpage_name
            return HttpResponseRedirect('/webpages/editor')
        elif next == "edit":
            curr_webpage = request.POST.get('curr_webpage')
            if curr_webpage == None:
                return render(request,'webpages/login.html', {"all_webpages": all_webpages,"error": "Select Valid Website Name"})
            request.session["curr_webpage"] = curr_webpage
            return HttpResponseRedirect('/webpages/editor')
    all_webpages = Webpages.objects.all()
    return render(request,'webpages/login.html', {"all_webpages": all_webpages})

def editor(request):
    if request.method == "POST":
        next = request.POST.get('next')
        if next == "save":
            curr_webpage = request.session["curr_webpage"]
            webpage = Webpages.objects.filter(name=curr_webpage)
            code = request.POST.get('code')
            soup = BeautifulSoup(code, 'html.parser')
            html = soup.prettify()
            # For Testing
            # with open(webpage[0].path, 'w') as file:
            with open("/home/coffeecoders/CoffeeCodersWebsite/CoffeeCodersWebsite/cc_projects/" + webpage[0].path, 'w') as file:
                file.write(html)
        else:
            webpage = Webpages.objects.filter(name=next)[0]
            try:
                os.remove(webpage.path)
            except:
                print("file not found")
            webpage.delete()
            request.session.pop('curr_webpage')
            return HttpResponseRedirect('/webpages')
    if 'curr_webpage' not in request.session:
            return HttpResponseRedirect('/webpages')
    curr_webpage = request.session["curr_webpage"]
    link = "coffeecoders.pythonanywhere.com/webpages/webpage?page="+curr_webpage
    webpage = Webpages.objects.filter(name=curr_webpage)
    try:
        # For Testing
        # with open(webpage[0].path, 'r') as file:
        with open("/home/coffeecoders/CoffeeCodersWebsite/CoffeeCodersWebsite/cc_projects/" + webpage[0].path, 'r') as file:
            code = file.read()
    except:
        return render(request,'webpages/editor.html', {"webpage_name": curr_webpage, "link":link})
    code = re.sub(r'\n+', '\n', code)
    soup = BeautifulSoup(code, 'html.parser')
    html = soup.prettify()
    return render(request,'webpages/editor.html', {"code": html, "webpage_name": curr_webpage, "link":link})

def webpage(request):
    curr_webpage = request.GET.get('page', '')
    if curr_webpage == "":
        if 'curr_webpage' in request.session:
            curr_webpage = request.session["curr_webpage"]
        else:
            return HttpResponseRedirect('/webpages')
    webpage = Webpages.objects.filter(name=curr_webpage)
    if len(webpage) == 0:
        return HttpResponseRedirect('/webpages')
    return render(request, webpage[0].render_path)
