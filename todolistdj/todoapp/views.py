from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    # Handling POST request to add a new task
    if request.method == 'POST':
        task = request.POST.get('task').strip()  # Get the task input and remove leading/trailing spaces
        if task:  # Check if the task is not empty
            try:
                # Create a new todo object for the authenticated user
                new_todo = todo(user=request.user, todo_name=task)
                new_todo.full_clean()  # Perform model validation
                new_todo.save()  # Save the new todo object 
            except ValidationError as e:
                messages.error(request, e.message)  # Display validation error message
        else:
            messages.error(request, "Task cannot be empty!")  # Display error if task is empty

    # Retrieve all todos associated with the current user
    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    # Render the home page with the todo list
    return render(request, 'todoapp/todo.html', context)

# View for user registration
def register(request):
    # Redirect to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if password length is sufficient
        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        # Check if username already exists
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists. Please choose another.')
            return redirect('register')

        # Create a new user
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        messages.success(request, 'User successfully created. Please log in.')
        return redirect('login')
    
    # Render the registration page
    return render(request, 'todoapp/register.html', {})

# View for user logout
def LogoutView(request):
    logout(request)  # Log out the current user
    return redirect('login')  # Redirect to the login page

# View for user login
def loginpage(request):
    # Redirect to home page if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        # Authenticate the user
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)  # Log in the user
            return redirect('home-page')  # Redirect to the home page
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')  # Redirect back to the login page with an error message

    # Render the login page
    return render(request, 'todoapp/login.html', {})

# View to delete a task
@login_required
def DeleteTask(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.delete()  # Delete the selected todo
    return redirect('home-page')  # Redirect to the home page

# View to update the status of a task
@login_required
def Update(request, name):
    get_todo = todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True  # Mark the task as completed
    get_todo.save()  # Save the changes
    return redirect('home-page')  # Redirect to the home page
