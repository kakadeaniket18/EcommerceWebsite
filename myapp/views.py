from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product, Cart, Order
from django.db.models import Q
import random
import razorpay

def register(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'Register.html')
    else:
        fn = request.POST['fname']
        ln = request.POST['lname']
        n = request.POST['uname']
        p = request.POST['upass']
        cp = request.POST['ucpass']
        if n=='' or p=='' or cp=='' or fn=='' or ln=='':
            context["errmsg"]="Fields cannot be blank"
            return render(request,"Register.html",context)
        elif p!=cp:
            context["errmsg"]="Passwords do not match"
            return render(request,"Register.html",context)
        elif len(p)<8 or len(p)>15:
            context["errmsg"]="Password must be 8 characters"
            return render(request,"Register.html",context)
        else:
            try:
                u=User.objects.create(username=n,password=p,email=n,first_name=fn,last_name=ln)
                u.set_password(p)
                u.save()
                context['success']="User Created Successfully..."
                return render(request, 'Register.html', context)
            except Exception:
                context["errmsg"]="Username already Exists, please Login"
                return render(request,'Register.html',context)
    return render(request, 'Register.html')

def user_login(request):
    if request.method=='GET':
        return render(request, 'Login.html')
    else:
        n = request.POST['uname']
        p = request.POST['upass']
        u=authenticate(username=n,password=p)
        if u is not None:
            login(request,u)
            return redirect('/products')
        else:
            context={}
            context["errmsg"]="Invalid Username or Password.."
            return render(request, 'Login.html', context)
    return render(request,'Login.html')

def user_logout(request):
    logout(request)
    return redirect('/login')

def products(request):
    uid=request.user.id
    p=Product.objects.filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'Index.html',context)

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1&q2)
    context={}
    context['data']=p
    return render(request,'Index.html',context)

def sort(request,sv):
    if sv=='1':
        p=Product.objects.order_by("-price").filter(is_active=True)
    else:
        p=Product.objects.order_by("price").filter(is_active=True)
    context={}
    context['data']=p
    return render(request,'Index.html',context)

def filterbyprice(request):
    min=request.GET["min"]
    max=request.GET["max"]
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Product.objects.filter(q1&q2)
    context={}
    context['data']=p
    return render(request,'Index.html',context)

def product_details(request,pid):
    p=Product.objects.filter(id=pid)
    context={}
    context['data']=p
    return render(request,'ProductDetails.html',context)

def cart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context={}
        context["data"]=p
        if n==1:
            context['msg']='Product already exist in cart'
            return render(request,'Productdetails.html',context)  
        else:
            c=Cart.objects.create(userid=u[0],pid=p[0])
            c.save
            context['msg']='Product added Successfully'
            return render(request,'Productdetails.html',context)        
    else:
        return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(userid=request.user.id)
    sum=0
    for x in c:
        sum=sum + x.pid.price * x.qty
    context={}
    context['data']=c
    context['total']=sum
    return render(request,'Cart.html',context)

def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/viewcart')

def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty*x.pid.price
        o=Order.objects.create(order_id=orderid,qty=x.qty,pid=x.pid,userid=x.userid,amount=amount)
        o.save()   
    return redirect('/fetchorder')

def fetchorder(request):
    user=User.objects.filter(id=request.user.id)
    orders=Order.objects.filter(userid=request.user.id)
    sum=0
    for x in orders:
        sum=sum+x.pid.price*x.qty
    context={}
    context['user']=user
    context['data']=orders
    context['n']=len(orders)+(x.qty-1)
    context['total']=sum 
    return render(request, 'Placeorder.html', context)

def removeorder(request,pid):
    o=Order.objects.filter(id=pid)
    o.delete()
    return redirect('/fetchorder')

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_bPe35x94k3fvXy", "rVxCIEeGXGKsUriyWW4ydI31"))
    order=Order.objects.filter(userid=request.user.id)
    sum=0
    for x in order:
        sum=sum+x.amount
        oid=x.order_id
    data = { "amount": sum*100, "currency": "INR", "receipt": oid}
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['payment']=payment
    return render(request,"Pay.html",context)
    return redirect('/fetchorder')
    
def about(request):
    return render(request,"About.html")

def contact(request):
    return render(request,"Contact.html")

def paymentsuccess(request):
    return render(request,"Paymentsuccess.html")

def search(request):
    context={}
    query=request.GET['query']
    name=Product.objects.filter(name__icontains=query)
    pdetails=Product.objects.filter(pdetails__icontains=query)
    cat=Product.objects.filter(cat__icontains=query)
    allproducts=name.union(pdetails,cat)
    if allproducts.count()==0:
        context['errmsg']="No Products Found"
        return render(request,'Index.html',context)
    else:
        context['data']=allproducts
        return render(request,'Index.html',context)