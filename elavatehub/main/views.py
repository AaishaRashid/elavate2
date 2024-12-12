from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Profile


# Create your views here.

def home(request):
    """Render the home page"""
    return render(request, 'home.html')


def login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after login
        else:
            # Add error message if authentication fails
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    """Handle user logout"""
    auth_logout(request)
    return redirect('home')


def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful, you can now log in.")
            return redirect('profile')  # Redirect to login page after successful registration
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    """Render user profile page"""
    profiles = Profile.objects.filter(user=request.user).first()  # Fetch user profile
    posts = Post.objects.filter(user=request.user)  # Fetch all posts by the user
    return render(request, 'profile_setup.html', {'profile': profile, 'posts': posts})


@login_required
def profile_edit(request):
    """Allow the user to edit their profile"""
    profiles = Profile.objects.filter(user=request.user).first()  # Get user's profile
    if request.method == 'POST':
        profile.full_name = request.POST['full_name']
        profile.bio = request.POST['bio']
        profile.business_idea = request.POST['business_idea']
        profile.location = request.POST['location']

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')  # Redirect back to profile page after saving changes

    return render(request, 'profile_edit.html', {'profile': profile})


@login_required
def dashboard(request):
    """Render the dashboard page"""
    user_posts = Post.objects.filter(user=request.user)  # Get posts made by the user
    return render(request, 'dashboard.html', {'user_posts': user_posts})


@login_required
def idea_feed(request):
    """Render idea feed page showing posts from all users"""
    posts = Post.objects.all()  # Retrieve all posts (or filter based on categories, etc.)
    return render(request, 'idea_feed.html', {'posts': posts})


@login_required
def post_create(request):
    """Allow users to create a new post"""
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        funding_pledged = request.POST['funding_pledged']
        category = request.POST['category']

        # Create new post
        post = Post(user=request.user, title=title, content=content, funding_pledged=funding_pledged, category=category)
        post.save()
        messages.success(request, "Your post has been created successfully!")
        return redirect('idea_feed')  # Redirect to idea feed page after creating a post

    return render(request, 'post_create.html')


@login_required
def post_edit(request, post_id):
    """Allow users to edit their existing post"""
    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        return redirect('idea_feed')  # Redirect if the user is not the owner of the post

    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.funding_pledged = request.POST['funding_pledged']
        post.category = request.POST['category']
        post.save()
        messages.success(request, "Your post has been updated!")
        return redirect('idea_feed')

    return render(request, 'post_edit.html', {'post': post})


@login_required
def post_delete(request, post_id):
    """Allow users to delete their posts"""
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        messages.success(request, "Your post has been deleted!")
    return redirect('idea_feed')


def mentors(request):
    """Render mentors page"""
    return render(request, 'mentors.html')


def general(request):
    """Render general page"""
    return render(request, 'general.html')

# Additional utility views can go here (e.g., for managing comments, payments, etc.)


def idea(request):
    # Your logic for the idea page
    return render(request, 'idea feed.html')  # Rendering the corresponding template
