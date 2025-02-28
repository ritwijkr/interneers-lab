from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    
    """
    API that returns a greeting message with a name.
    Supports additional parameters:
    - 'greeting' (optional): Custom greeting message
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")

    message=f'hello, {name}'
    return JsonResponse({"message": message})

def condition1(age):
    if not age.isdigit():
        return True
    else:
        return False
def condition2(gender):
    if gender!='Female' and gender!='Male' and gender!="Other":
        return True
    else:
        return False


def introduction(request):
    """
    API that returns information about a individual.
    name, age, gender (let's say)
    """
    name=request.GET.get("name","Raj")#setting ritwij as default
    age=request.GET.get("age","19")
    gender=request.GET.get("gender","Other")
    if condition1(age) and condition2(gender):
        return JsonResponse({"error": "Invalid age and gender."}, status=400)
    elif condition1(age):
        return JsonResponse({"error": "Invalid age."}, status=400)
    elif condition2(gender):
        return JsonResponse({"error": "Invalid gender."}, status=400)
    
    message=f'name: {name}, age: {age}, gender: {gender}'

    return JsonResponse({"message": message})
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', introduction),
]
