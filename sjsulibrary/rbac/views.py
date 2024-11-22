from django.shortcuts import render, redirect

# Login/Register/Logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import logout

# Permissions
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

# Provisioning/deprovisioning
from django.contrib.admin.views.decorators import staff_member_required
from .forms import AssignRoleForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import RBACUser

# RBAC decorators
from .decorators import roles_required
# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')

def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user and their role
            return redirect('home')  # Redirect to login page after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'default.html')

@roles_required('Librarian')
def manage_inventory(request):
    return render(request, 'inventory.html')

@roles_required('Librarian', 'Student', 'Faculty')
def university_resources(request):
    return render(request, 'university_resources.html')

def public_resources(request):
    return render(request, 'public_resources.html')

@roles_required('Librarian', 'Faculty')
def place_hold(request):
    return render(request, 'place_hold.html')

@login_required
def deprovision_user(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(RBACUser, user_id=user_id)
        user.is_active=False
        user.save()
        return redirect('home')
    else:
        return render(request, 'forbidden.html')
    
@roles_required('Librarian')
def assign_role(request):
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AssignRoleForm()
    return render(request, 'assign_role.html', {'form': form})