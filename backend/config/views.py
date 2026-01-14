"""
Views for the AI Blog Generator application
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import BlogPost


def index(request):
    """Serve the main index.html page"""
    return render(request, 'index.html')


def login_view(request):
    """Handle login page display and authentication"""
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def signup_view(request):
    """Handle signup page display and user registration"""
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('index')
    
    errors = {}
    form_data = {}
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeatPassword', '')
        
        # Store form data to repopulate form on error
        form_data = {
            'username': username,
            'email': email,
        }
        
        # Validation
        if not username:
            errors['username'] = 'Username is required.'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters long.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists. Please choose another.'
        
        if not email:
            errors['email'] = 'Email is required.'
        elif '@' not in email or '.' not in email:
            errors['email'] = 'Please enter a valid email address.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered. Please use another email.'
        
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'
        
        if not repeat_password:
            errors['repeatPassword'] = 'Please confirm your password.'
        elif password != repeat_password:
            errors['repeatPassword'] = 'Passwords do not match.'
        
        # If no errors, create user and log them in
        if not errors:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                # Automatically log in the user
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome, {username}!')
                return redirect('index')
            except Exception as e:
                errors['general'] = f'An error occurred during registration: {str(e)}'
    
    # Render template with errors and form data
    context = {
        'errors': errors,
        'form_data': form_data,
    }
    return render(request, 'signup.html', context)


@login_required
def all_blog_posts(request):
    """Display all blog posts for the logged-in user"""
    blog_posts = BlogPost.objects.filter(author=request.user)
    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'all_blog_posts.html', context)


@login_required
def blog_details(request, blog_id=None):
    """Display details of a specific blog post"""
    if blog_id:
        blog_post = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    else:
        # For demo purposes, get the first blog post if no ID provided
        blog_post = BlogPost.objects.filter(author=request.user).first()
        if not blog_post:
            messages.info(request, 'No blog posts found. Create your first blog post!')
            return redirect('index')
    
    context = {
        'blog_post': blog_post,
    }
    return render(request, 'blog-details.html', context)
