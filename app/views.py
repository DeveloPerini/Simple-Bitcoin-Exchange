from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, OrderForm
from .models import User, Order , Trade
import random
from django.contrib import messages
from django.db.models import Q 




def home(request):
    return render(request, 'app/index.html')




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                bitcoin_balance=random.uniform(1, 10),
                dollars_balance = 10000000,
            )
            return redirect('confirmed')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', {'form': form})




def registration_confirmed(request):
    return render(request, 'app/confirmed.html')




def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            ).first()
            if user:
                request.session['user_id'] = user.id
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})    





def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = User.objects.get(id=request.session['user_id'])
    orders = Order.objects.filter(executed=False)
    profit_loss_btc, profit_loss_dollar = calculate_profit_loss(request.session['user_id'])
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            if user.bitcoin_balance < form.cleaned_data['quantity'] and form.cleaned_data['type'] == 'SELL':
                messages.error(request, 'You have not enough balance to sell this order')
                return redirect('dashboard')
            
            new_order = Order.objects.create(
                user=user,
                type=form.cleaned_data['type'],
                quantity=form.cleaned_data['quantity'],
                price=form.cleaned_data['price']
            )
            match_orders(request, new_order.id)
    else:
        form = OrderForm()
    return render(request, 'app/dashboard.html', {'user': user, 'orders': orders, 'form': form, 'profit_loss_btc':profit_loss_btc, 'profit_loss_dollar' : profit_loss_dollar})






def match_orders(request, order_id):
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=request.session['user_id'])
    if order.type == 'BUY':
        sell_orders = Order.objects.filter(type='SELL', price__lte=order.price, executed=False)
        for sell_order in sell_orders:
            trade_quantity = min(order.quantity, sell_order.quantity)
            if user.dollars_balance - sell_order.price * trade_quantity < 0:
                messages.error(request, 'You have not enough balance to buy this order')
                return redirect('dashboard')
            if sell_order.user.bitcoin_balance < trade_quantity:
                messages.error(request, 'Seller does not have enough balance')
                other_open_orders = Order.objects.filter(user=sell_order.user, type='SELL', executed=False)
                for open_order in other_open_orders:
                    if sell_order.user.bitcoin_balance - open_order.quantity < 0:
                        open_order.executed = True
                        open_order.save()
                continue
            if sell_order.user.id == user.id:
                messages.error(request, 'You cannot sell to your own buy order')
                continue
            trade = Trade(buyer=order.user, seller=sell_order.user, price=sell_order.price, quantity=trade_quantity)
            trade.save()
            order.user.bitcoin_balance += trade_quantity
            order.user.dollars_balance -= sell_order.price * trade_quantity
            sell_order.user.bitcoin_balance -= trade_quantity
            sell_order.user.dollars_balance += sell_order.price * trade_quantity
            order.user.save()
            sell_order.user.save()
            order.quantity -= trade_quantity
            sell_order.quantity -= trade_quantity
            if order.quantity == 0:
                order.executed = True
            if sell_order.quantity == 0:
                sell_order.executed = True
            order.save()
            sell_order.save()
            messages.success(request, 'Order completed')
    else:
            buy_orders = Order.objects.filter(type='BUY', price__gte=order.price, executed=False)
            for buy_order in buy_orders:
                trade_quantity = min(order.quantity, buy_order.quantity)
                if buy_order.user.id == user.id:
                    continue
                trade = Trade(buyer=buy_order.user, seller=user, price=order.price, quantity=trade_quantity)
                trade.save()
                buy_order.user.bitcoin_balance += trade_quantity
                buy_order.user.dollars_balance -= order.price * trade_quantity
                user.bitcoin_balance -= trade_quantity
                user.dollars_balance += order.price * trade_quantity
                buy_order.user.save()
                user.save()
                order.quantity -= trade_quantity
                buy_order.quantity -= trade_quantity

                if order.quantity == 0:
                    order.executed = True
                if buy_order.quantity == 0:
                    buy_order.executed = True

                order.save()
                buy_order.save()
                messages.success(request, 'Order completed')
            if order.executed == False:
                messages.success(request, 'Order placed correctly, but there is no buy order for this sell price')





def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    user = User.objects.get(id=request.session['user_id'])

    if user.id != order.user.id:
        return redirect('dashboard')

    order.delete()
    messages.success(request, 'Order deleted')
    return redirect('dashboard')





def calculate_profit_loss(user_id):
    user = User.objects.get(id=user_id)
    trades = Trade.objects.filter(Q(buyer=user) | Q(seller=user))
    btc_profit_loss = 0
    dollar_profit_loss = 0
    for trade in trades:
        if trade.buyer == user:
            btc_profit_loss += trade.quantity
            dollar_profit_loss -= (trade.price * trade.quantity)
        else:
            btc_profit_loss -= trade.quantity
            dollar_profit_loss += (trade.price * trade.quantity)
    return btc_profit_loss, dollar_profit_loss

