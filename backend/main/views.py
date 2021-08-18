import posenet_main
from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# Create your views here.
# class index(request):
#    main.main()


def index(request):
    str = posenet_main.main()
    return HttpResponse(str)
