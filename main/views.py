import posenet_main
from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def index(request):
    # posenet_main.main()
    return render(request, 'main/main.html')
