from django.shortcuts import render

def product_list_view(request):
    return render(request, 'product_list.html')
