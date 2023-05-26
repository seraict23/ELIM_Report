from django.shortcuts import render


def Cover(req):
    return render(req, 'mockup/cover.html')