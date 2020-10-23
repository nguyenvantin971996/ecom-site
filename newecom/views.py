from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import CommentForm,CreateUserForm
from django.db.models import Q
# Create your views here.
import decimal
def storeView(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    if request.method == 'POST':
        ten = request.POST['name']
        min = decimal.Decimal(request.POST['minprice'])
        max = decimal.Decimal(request.POST['maxprice'])
        products = Product.objects.filter(Q(name__icontains=ten),Q(price__gt=min),Q(price__lt=max))
    else:
        ten=''
        min=0
        max=1000
        products = Product.objects.all()
    context = {'items': items, 'order': order,'products':products,'min':min,'max':max,'ten':ten}
    return render(request,'newecom/store.html',context)

def updateCart(request):
    if request.method == 'POST':
        customer=request.user.customer
        productId = request.POST['productId']
        quantity=request.POST['quantity']
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        orderItem,created = OrderItem.objects.get_or_create(order=order,product=product)
        orderItem.quantity=orderItem.quantity + int(quantity)
        orderItem.save()
        return redirect('store')
    elif request.method=='GET':
        customer = request.user.customer
        orderItemId = request.GET['itemId']
        soluong = request.GET['soluong']
        item = OrderItem.objects.get(id=orderItemId)
        item.quantity=soluong
        item.save()
        return redirect('cart')

def deleteCart(request):
    if request.method == 'POST':
        customer=request.user.customer
        orderItemId= request.POST['orderItemId']
        item = OrderItem.objects.get(id=orderItemId)
        item.delete()
        return redirect('cart')
    return HttpResponse('Delete successfully!')

def cartView(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    return render(request,'newecom/cart.html',context)

def productView(request,pk):
    product = Product.objects.get(id=pk)
    customer = request.user.customer
    comments = product.get_comment.all()
    comment_form = CommentForm()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            if request.POST.get("parent", None):
                new_comment.parent_id = int(request.POST.get("parent"))
            new_comment.product = product
            new_comment.customer = customer
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    context = {'product': product,'customer':customer,'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form}
    return render(request,'newecom/product.html',context)

def Signin(request):
    form = CreateUserForm()
    if request.method == "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form':form}
    return render(request, 'newecom/signin.html', context)

def Checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if request.method == "POST":
        shippingaddress, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        shippingaddress.address = request.POST['address']
        shippingaddress.city = request.POST['city']
        shippingaddress.state = request.POST['state']
        shippingaddress.zipcode = request.POST['zipcode']
        shippingaddress.save()
        return redirect('checkout')
    return render(request, 'newecom/checkout.html')