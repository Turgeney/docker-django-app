from django.shortcuts import render, redirect
from .forms import UsersForm
from .models import Users

# Create your views here.
def index_page(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()  # Сохранение данных в базу данных
            return redirect('all_users')  # Перенаправление на другую страницу
    else:
        form = UsersForm()
    return render(request, 'index.html', {'form': form})

def all_users(request):
    users = Users.objects.all()
    return render(request, 'all_users.html', {'users':users})