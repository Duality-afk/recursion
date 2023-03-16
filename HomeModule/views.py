from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from HomeModule.models import ProdCat, Category

# Create your views here.
def home(request):
    return render(request,'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            print("Success!")
            return redirect("/")
        else:
            messages.info(request,'Invalid cedentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
    

def productCatalog(request):
    allProd = ProdCat.objects.all()
    print(allProd)
    
    allCat = Category.objects.all()
    context = {'allProd': allProd,'allCat':allCat}
    return render(request,'productCatalog.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, password=password1, email=email)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'Password not matching..')
            return redirect('register')

    else:         
       return render(request, 'register.html')
    
def logout(request):
   auth.logout(request)
   return redirect('/')


def filter(request):
    if request.method == "POST":
        allCat = Category.objects.all()
        check = request.POST.getlist('checks[]')
        filters = []
        for value in check:
            filteredcat = Category.objects.filter(id=value)
            for f in filteredcat:
                
                filtercatname = f.name
                filters.append(filtercatname)
                print(filters)

        allProd = ProdCat.objects.all()
        results = []
        for prod in allProd:
            for fil in filters:
                if prod.category.name == fil:
                    results.append(prod)
        return render(request,"productCatalog1.html",{"results":results,"allCat":allCat})
        

    

def cart(request):
    return render(request,'cart.html')