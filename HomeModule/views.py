from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from HomeModule.models import ProdCat, Category,Track, UserActivity
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
import json
from shopX.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay


page_tags = {
    'fc-barcelona-limited-edition-jersey': ['football', 'sports','soccer'],
    'adidas-x-speedportal-firm-ground-boots': ['sports', 'soccer','shorts'],
    'oceaunz-pro-football': ['football', 'soccer'],
    'argentina-22-home-shorts': ['sports', 'shorts'],
    'messi-club-shin-guards' : ['football', 'sports'],
    'babolat-pure-strike-vs' :['football', 'sports'],
    'asics-court-ff-3-novak-mens-shoe-tuna-blue-wh' :['football', 'sports'],
    'yonex-tour-platinum-balls-dozen-3-cans-of-4-ball' :['cricket', 'sports'],
    'babolat-powergy-16-string-reel-200-m' :['football', 'sports'],
    'mcdavid-shoulder-wrap-black' :['football', 'sports'],

    }    

# page_tags = {
#     'cricket': ['sports', 'male','female'],
#     'tennis': ['male', 'female','tall'],
#     'badminton': ['sports', 'female'],
#     'basketball': ['male', 'tall'],
#     'football' : ['sports', 'male'],
# }    
allUsers = UserActivity.objects.all()

userlists = {}
uniqueusers = []

for aluser in allUsers:
    if aluser.user not in uniqueusers:
        uniqueusers.append(aluser.user)

for users in uniqueusers:
    for aluser in allUsers:
        if users == aluser.user:
            userlists[users] = [aluser.activity_details]

# Define a function to calculate similarity between pages based on tags
def calculate_similarity(page_tags):
    tag_list = []
    for tags in page_tags.values():
        tag_list += tags
    unique_tags = sorted(list(set(tag_list)))
    tag_vectors = []
    for tags in page_tags.values():
        vector = [tags.count(tag) for tag in unique_tags]
        tag_vectors.append(vector)
    similarity_matrix = cosine_similarity(tag_vectors)
    print(similarity_matrix)
    return similarity_matrix

#Calculate page similarity matrix
page_similarity = calculate_similarity(page_tags)

# Define a function to recommend pages to a user based on their visits and page similarity
def recommend_pages(user_visits, page_similarity):
    user_list = list(userlists.keys())
    num_users = len(userlists)
    page_list = list(page_tags.keys())
    num_pages = len(page_list)
    user_matrix = np.zeros((num_users, num_pages))
    for i, user in enumerate(userlists):
        for page in userlists[user]:
            j = page_list.index(page)   
            user_matrix[i,j] = 1

    recommendations = []


    for i, user in enumerate(user_list):
        user_vector = user_matrix[i,:]
        scores = np.dot(user_vector, page_similarity)
        ranked_pages = np.argsort(-scores)
        recommended_pages = [page_list[idx] for idx in ranked_pages]
        recommendations.append((user, recommended_pages))
    return recommendations

# Create your views here.
def home(request):
    print(request.path)
    if request.user.is_authenticated:
        all_entries = UserActivity.objects.filter(user = request.user)
        recommendations = recommend_pages(userlists, page_similarity)
        recomProds = recommendations[0][1]
      
        recom = list(page_tags.keys())
        
        allProducts = ProdCat.objects.all()
        
        #recommendations = list(recommendations)
        recomProds1 = ProdCat.objects.filter(name__in=recomProds)
        
        #recomProds = ProdCat.objects.filter(name__icontains='home')
        context ={'recom':recom,'allProducts':allProducts}
        return render(request,'home.html', context)

    return render(request,'home.html')

def search(request):
    query=request.GET['query']
    allProd= ProdCat.objects.filter(name__icontains=query)
    
    allCat = Category.objects.all()
    context = {'allProd': allProd,'allCat':allCat}
    return render(request, 'search.html', context)

def iframe(request):
    return render(request,'iframe.html')

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
        

    
def track(request):
    orderStatus = Track.objects.filter(username = request.user.username)
    noorder = False
    if len(orderStatus)<1:
        noorder = True
    context = {"orderStatus":orderStatus,"noorder":noorder}
    return render(request,'track.html', context)

client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
def productDetail(request, slug):
    reg = ProdCat.objects.filter(slug = slug).first()
    
    amount = reg.price*100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'

    payment_order = client.order.create(dict(amount=amount,currency = order_currency,receipt = order_receipt, payment_capture = 1))
    payment_order_id = payment_order['id']

    orderdetails = Track()
    orderdetails.username = request.user.username
    orderdetails.orderTitle = reg.name
    orderdetails.orderDesc = reg.desc
    orderdetails.orderPrice = reg.price
    orderdetails.image = reg.image.url

    orderdetails.save()

    context = {'reg': reg, 'amount':amount,'api_key':RAZORPAY_API_KEY,'order_id':payment_order_id}
    return render(request,'productDetail.html', context)

def pastOrders(request):
    allOrders = Track.objects.filter(username = request.user.username)
    nopastorders = False
    if len(allOrders)<1:
        nopastorders = True
    context = {"allOrders":allOrders,"nopastorders":nopastorders}
    return render(request,'pastOrders.html',context)

def add_to_cart(request):
    if request.method == "POST":
        productid = request.POST.get('product-id')
        print("productid",productid)
    '''if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = ProdCat.objects.get(id=prod_id)

            if(product_check):
                if(Cart.objects.filter(user=request.user.id,product = prod_id)):
                    return JsonResponse({"status":"Product already in cart"})
                else:
                    Cart.objects.create(user = request.user,product = prod_id)
                    return JsonResponse({"status":"Product added successfully"})
            else:
                return JsonResponse({"status":"No such product found"})

        else:
            return JsonResponse({"status":"Login to Continue"})'''

def payment(request):
    
    client = razorpay.Client(auth=("rzp_test_yOgTa9YwwHLKDR", "qDmtqkDq7Rs3OIpFDd7JDtRR"))
    DATA = {
    "amount": 60000,
    "currency": "INR",
    "receipt": "receipt#1",
    }
    payment_order = client.order.create(data=DATA)
    payment_order_id = payment_order['id']
    prod = ProdCat.objects.filter().firs
    print(prod)
    context = {
        'prod': prod,
        'api_key': RAZORPAY_API_KEY,
        'order_id': payment_order_id,
        }
  
    return render(request , 'payment.html', context)


    


