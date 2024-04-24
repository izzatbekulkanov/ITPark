from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Muvaffaqiyatli kirdingiz.')
            return redirect('admin_view')  # Foydalanuvchi muvaffaqiyatli kirdi bo'lsa, admin paneliga yo'naltirish
        else:
            messages.error(request, 'Noto\'g\'ri foydalanuvchi nomi yoki parol.')
            return redirect('login')  # Foydalanuvchi kiritishi xatosi bo'lsa, qayta kirish sahifasiga yo'naltiriladi
    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('index')  # Foydalanuvchi avtorizatsiyadan chiqqandan so'ng o'tkaziladigan URL
