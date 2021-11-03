from django.shortcuts import render

# Create your views here.
def home(request):
    context = {'hello': 'calc'}
    return render(request, 'index.html', context)