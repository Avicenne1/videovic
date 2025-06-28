from django.shortcuts import redirect

def accueil(request):
    return redirect('dashboard')  
