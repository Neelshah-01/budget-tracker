from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm, Transaction
from django.http import HttpResponseNotAllowed
from .models import Category
# Create your views here.
def redirect_to_home(request):
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def view_transactions(request):
    transactions = Transaction.objects.all().order_by('-date')
    categories = Category.objects.all()

    # Apply filters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    amount_gt = request.GET.get('amount_gt')
    amount_lt = request.GET.get('amount_lt')
    amount_eq = request.GET.get('amount_eq')
    search_text = request.GET.get('search_notes')
    category = request.GET.get('categories')
    t_type = request.GET.get('type')

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if amount_gt:
        transactions = transactions.filter(amount__gt=amount_gt)
    if amount_lt:
        transactions = transactions.filter(amount__lt=amount_lt)
    if amount_eq:
        transactions = transactions.filter(amount=amount_eq)
    if search_text:
        transactions = transactions.filter(notes__icontains=search_text)
    if t_type:
        transactions = transactions.filter(type=t_type)
    if category:
        transactions = transactions.filter(category=category)

    total_income, total_expenses = Transaction.total_income_expenses(transactions)

    return render(request, 'view_transactions.html', {
        'categories': categories,
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'search_text': search_text,
    })

def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_transactions')
    else:
        form = TransactionForm()
    return render(request, 'new_transaction.html', {'form': form})

def delete_transaction(request, pk):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, pk=pk)
        transaction.delete()
        return redirect('view_transactions')
    else:
        return HttpResponseNotAllowed(['POST'])