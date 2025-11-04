from django.shortcuts import render

def about(request):
    return render(request, 'contacts/about.html')
