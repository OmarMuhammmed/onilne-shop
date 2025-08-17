from django.shortcuts import render
from django.http import JsonResponse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from celery.result import AsyncResult

def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()

            # run asynchronous task
            task = order_created.delay(order.id)
            
            # Store task ID in session to check later
            request.session['email_task_id'] = task.id

            return render(request, 'orders/order/created.html', {'order': order, 'task_id': task.id})
        else:
            form = OrderCreateForm()
            return render(request,'orders/order/create.html', {'cart': cart, 'form': form})

    return render(request, 'orders/order/create.html', {'cart': cart})        
