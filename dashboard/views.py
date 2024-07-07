from django.shortcuts import render, redirect,get_object_or_404

from django.http import HttpResponse
from .models import Patient, Doctor, User, Blog_Post
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request,'home.html')


def login(request):
    if request.method == 'GET':
        return render(request,'login_form.html',{'show_toast':False})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}")
        print(f"Password: {password}")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            message = 'Sent'
            success = True
            return redirect('profile')             

        else:
            message = 'User not found'
            success = False
            return render(request,'login_form.html',{'message':message,'show_toast':True,'success':success})

       
    
@login_required
def profile_view(request):
    user = request.user


    if not request.user.is_authenticated:
        return redirect('')

    # Check if the user has a related Patient profile
    try:
        profile = Patient.objects.get(user=user)
        profile_type = 'patient'
        blog_posts = Blog_Post.objects.filter(draft = False)

        return render(request, 'Profile/patient_profile.html', {'profile': profile,'blog_posts':blog_posts})
    except Patient.DoesNotExist:
        # If not a Patient, check if the user has a related Doctor profile
        try:
            profile = Doctor.objects.get(user=user)
            profile_type = 'doctor'
            blog_posts = Blog_Post.objects.filter(author=profile,draft = False)
            draft_blog_posts = Blog_Post.objects.filter(author=profile,draft = True)
            return render(request, 'Profile/doctor_profile.html', {'profile': profile, 'blog_posts': blog_posts, 'draft_blog_posts':draft_blog_posts})
        except Doctor.DoesNotExist:
            profile = None
            profile_type = None

    

def logout_view(request):
    logout(request)
    return redirect('login')

        

       

def signup(request):
    if request.method == 'GET':
        return render(request,'signup_form.html',{'show_toast':False})
    elif request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        patient_profile_picture = request.FILES.get('patient_profile_picture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        speciality = request.POST.get('speciality')
        license = request.POST.get('license')
        confirm_password = request.POST.get('confirm_password')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        role = request.POST.get('role')

        # Print the form data to terminal for debugging
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Profile Picture: {profile_picture}")
        print(f"patient_profile_picture: {patient_profile_picture}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Confirm Password: {confirm_password}")
        print(f"Address Line 1: {address_line1}")
        print(f"City: {city}")
        print(f"State: {state}")
        print(f"Pincode: {pincode}")
        print(f"role: {role}")

        # Optionally, validate data (e.g., check if passwords match)
        if role == 'doctor':
            try:
                # Create a new user instance
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    # password=password,
                )
                new_user.set_password(password)
                new_user.save()

                new_doctor = Doctor(
                    user = new_user,
                    # profile_picture=profile_picture,
                    specialty = speciality,
                    license_number = license,
                    line1=address_line1,
                    city=city,
                    state=state,
                    pincode=pincode,
                )
                if profile_picture:
                    new_doctor.profile_picture = profile_picture
                else:
                    new_doctor.profile_picture = 'profile_pictures/default.png'



                new_doctor.save()
                message = 'Successfully submitted'
                success = True
            except Exception as e:
                message = 'Something went wrong!'
                success = False
                print("Something went wrong",e)
        elif role == 'patient':
            try:
                # Create a new user instance
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    # password=password,
                )
                new_user.set_password(password)

                new_user.save()

                new_patient = Patient(
                    user = new_user,
                    profile_picture=patient_profile_picture,
                    line1=address_line1,
                    city=city,
                    state=state,
                    pincode=pincode,
                )
                if patient_profile_picture:
                    new_patient.profile_picture = patient_profile_picture
                else:
                    new_patient.profile_picture = 'profile_pictures/default.png'

                new_patient.save()
                message = 'Successfully submitted'
                success = True
            except Exception as e:
                message = 'Something went wrong!'
                success = False
                print("Something went wrong",e)
        return render(request,'signup_form.html',{'message':message, 'show_toast': True,'success':success})
    

@login_required
def post_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        draft = request.POST.get('draft') 

        if draft:  
            is_draft = True
        else:
            is_draft = False
        lines = content.split('\n')
        summary = '\n'.join(lines[:2]) + "....."

        print(title, content, category, image)
        doctor = request.user
        profile = Doctor.objects.get(user=doctor)
        blog_post = Blog_Post(
            title=title,
            content=content,
            summary = summary, 
            category=category,
            image=image,
            author=profile,
            draft = is_draft

        )
        blog_post.save()
        success_message = "Your blog post has been successfully saved!"
    
    return redirect('/dash/profile/')

@login_required
def delete_post(request, post_id):
    print("inside delete")
    post = get_object_or_404(Blog_Post, id=post_id)
    
    if request.user != post.author.user:
        print("ERROR")
    if post:
        post.delete()
    return redirect('/dash/profile')

@login_required
def update_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        print("posstid", post_id)
        title = request.POST.get('title')
        print("posstitlte", title)

        content = request.POST.get('content')
        category = request.POST.get('category')
        draft = request.POST.get('draft')

        post = get_object_or_404(Blog_Post, id=post_id)

        post.title = title
        post.content = content
        post.category = category
        post.draft = True if draft == 'on' else False 
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        return redirect('/dash/profile')
    
