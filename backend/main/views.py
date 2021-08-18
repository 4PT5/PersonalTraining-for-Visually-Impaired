from django.shortcuts import render
from rest_framework import generics

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import posenet_main

# Create your views here.
# class index(request):
#    main.main()

def index(request):
   posenet_main.main()
