from django.shortcuts import render, redirect

# Login/Register/Logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import logout

# Provisioning/deprovisioning
from .forms import AssignRoleForm, DeleteUserForm, ProvisionForm
from django.shortcuts import redirect, get_object_or_404
from .models import RBACUser
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

# RBAC Decorators
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
    
@roles_required('Admin')
def assign_role(request):
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AssignRoleForm()
    return render(request, 'assign_role.html', {'form': form})

@roles_required('Admin')
def delete_user(request):
    # Ensure the user has Admin role
    if not request.user.is_authenticated or not request.user.roles.filter(role_name='Admin').exists():
        return HttpResponseForbidden("You do not have access to this page.")
    
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            user_to_delete = form.cleaned_data['user']
            user_to_delete.delete()  # Delete the selected user
            messages.success(request, f"User {user_to_delete.username} has been deleted.")
            return redirect('home')  # Redirect after deletion
    else:
        form = DeleteUserForm()

    return render(request, 'delete_user.html', {'form': form})

@roles_required('Admin')
def user_list(request):
    users = RBACUser.objects.all() # Fetch all RBACUsers
    return render(request, 'user_list.html', {'users': users})

@roles_required('Admin')
def provision_user(request):
    if request.method == 'POST':
        form = ProvisionForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and assign roles
            messages.success(request, f"User {user.username} has been created with the assigned roles.")
            return redirect('home')  # Redirect to home or another page after success
    else:
        form = ProvisionForm()

    return render(request, 'provision_user.html', {'form': form})