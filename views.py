from django.shortcuts import render, redirect
from django.http import HttpResponse
from Base_App.models import  Items, ItemList, Feedback, AboutUs, BookTable, Order, OrderItem, Payment
from django.utils.timezone import now

# Create your views here.

def HomeView(request):
    items = Items.objects.all()
    list_items = ItemList.objects.all()
    reviews = Feedback.objects.all()
    return render(request, 'home.html', {'items': items, 'list': list_items, 'review': reviews})

def AboutView(request):
    data = AboutUs.objects.all()
    return render(request, 'about.html', {'data': data})

def MenuView(request):
    items = Items.objects.all()
    list_items = ItemList.objects.all()
    return render(request, 'menu.html', {'items': items, 'list': list_items})
 
def BookTableView(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('user_email')
        total_person = request.POST.get('total_person')
        booking_date = request.POST.get('booking_date')

        # Validate inputs
        if (
            name and 
            len(phone_number) == 10 and 
            email and 
            total_person.isdigit() and 
            int(total_person) > 0 and 
            booking_date
        ):
            data = BookTable(
                Name=name,
                Phone_number=phone_number,
                Email=email,
                Total_person=int(total_person),
                Booking_date=booking_date
            )
            data.save()
    
    return render(request, 'book_table.html')

def FeedbackView(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        description = request.POST.get('description')
        rating = request.POST.get('rating')
        image = request.FILES.get('image')  # Handle uploaded image

        # Validate and save feedback
        if user_name and description and rating.isdigit() and 1 <= int(rating) <= 5:
            feedback = Feedback(
                User_name=user_name,
                Description=description,
                Rating=int(rating),
                Image=image
            )
            feedback.save()
            return redirect('home')  # Redirect to home or thank-you page
    return render(request, 'feedback.html')

def OrderView(request):
    if request.method == 'POST':
        items = request.POST.getlist('items')  # IDs of selected items
        quantities = request.POST.getlist('quantities')  # Corresponding quantities

        if items and quantities:
            order = Order(customer_name=request.POST.get('customer_name'), order_date=now())
            order.save()  # Save the order to generate an ID
            
            total_price = 0
            for item_id, quantity in zip(items, quantities):
                try:
                    item = Items.objects.get(id=item_id)
                    quantity = int(quantity)
                    if quantity > 0:
                        order_item = OrderItem(
                            order=order,
                            item=item,
                            quantity=quantity,
                            price=item.Price * quantity
                        )
                        order_item.save()
                        total_price += order_item.price
                except Items.DoesNotExist:
                    continue
            
            return render(request, 'order_confirmation.html', {'order': order, 'total_price': total_price})

    items = Items.objects.all()
    return render(request, 'order.html', {'items': items})

def PaymentView(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')
        amount = request.POST.get('amount')

        try:
            order = Order.objects.get(id=order_id)
            amount = float(amount)

            # Check if the order already has a payment
            existing_payment = Payment.objects.filter(order=order).first()

            if existing_payment:
                # If payment already exists, you can either return a message or update the payment
                return render(request, 'payment_failure.html', {'error': 'This order already has a payment.'})

            if amount >= order.get_total_cost():  # Check if the payment is sufficient
                payment = Payment(
                    order=order,
                    payment_method=payment_method,
                    payment_status='Completed',  # Mark the payment as completed
                    payment_date=now()
                )
                payment.save()

                # Mark the order as paid
                order.is_paid = True
                order.save()

                return render(request, 'payment_success.html', {'payment': payment, 'order': order})
            else:
                return render(request, 'payment_failure.html', {'error': 'Insufficient payment amount.'})

        except Order.DoesNotExist:
            return render(request, 'payment_failure.html', {'error': 'Order not found.'})

    orders = Order.objects.all()
    return render(request, 'payment.html', {'orders': orders})
 