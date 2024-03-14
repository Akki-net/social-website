from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, \
                    UserEditForm, ProfileEditForm, PostForm, AppointmentForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Appointment
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
import datetime
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen pasword
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.xhtml', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.xhtml', {'user_form': user_form})

@login_required
def dashboard(request):
    return render(request,
                'account/dashboard.xhtml',
                {'section': 'dashboard'})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(request, 'account/login.xhtml', {'form': form})
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
            return redirect('/account')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.xhtml',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'section': 'edit'})
@login_required                
def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Post created successfully')
            # redirect to new created post detail view
            return redirect(post.get_absolute_url())
        else:
            messages.error(request, 'Error while posting')
    else:
        form = PostForm()
    return render(request, 'account/post/create_post.xhtml',{'form': form, 'section': 'create'})

@login_required 
def post_list(request):
    if request.user.profile.type_of_user == 'DR':
        posts = request.user.blog_posts.all()
    else:
        posts = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'account/post/list.xhtml',
                 {'posts': posts, 'section': 'feed'})
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            #  status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'account/post/detail.xhtml',
                  {'post': post})
class DoctorList(ListView):
    queryset = Profile.objects.filter(type_of_user = 'DR')
    template_name = 'account/appointment/doctor_list.xhtml'
    paginate_by = 4
    context_object_name = 'doctor_list'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'm_appoint'
        return context

def add_minutes_to_time(time_obj, minutes):
    # Convert time to a full datetime object (with a dummy date)
    full_datetime = datetime.datetime(100, 1, 1, time_obj.hour, time_obj.minute, time_obj.second)

    # Add the specified minutes
    updated_datetime = full_datetime + datetime.timedelta(minutes=minutes)

    # Extract the time part
    updated_time = updated_datetime.time()

    return updated_time

@login_required
def make_appointment(request, id):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = get_object_or_404(User, id=id)
            appointment = form.save(commit=False)
            appointment.doctor_name = doctor      
            print(appointment.start_time)  
            appointment.end_time = add_minutes_to_time(appointment.start_time, 45)
            appointment.save()
            messages.success(request, 'Appointment scheduled successfully')
            return redirect(appointment.get_absolute_url())
        else:
            messages.error(request, 'Error while scheduling')
    else:
        form = AppointmentForm()
    return render(request, 'account/appointment/appointment_form.xhtml', {
        'form': form
    })

class AppointmentDetail(DetailView):
    model=Appointment
    template_name = 'account/appointment/appointment_detail.xhtml'
    context_object_name = 'appointment_object'