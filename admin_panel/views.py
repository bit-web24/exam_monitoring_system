from django.shortcuts import render

def home_view(request):
    return render(request, 'admin_panel/dashboard.html')
