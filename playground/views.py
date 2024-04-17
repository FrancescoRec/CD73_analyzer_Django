from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):
    # return HttpResponse("Hello, world.")
    return render(request, "hello.html", {"name" : "world"}) # render function takes the request object and the path to the template file

