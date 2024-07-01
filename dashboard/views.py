from django.shortcuts import render, redirect
# import templates
# Create your views here.

from django.http import HttpResponse
from .models import Patient, Doctor, User
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
        # user = User.objects.get(username=username)
        
        if user is not None:
            # if user.password == password:
            auth_login(request, user)
            # return redirect('profile')
            message = 'Sent'
            success = True
            # return render(request,'login_form.html',{'message':message,'show_toast':True,'success':success})
            return redirect('profile') 
        # else:
        #         message = 'invalid password'
        #         success = False
        #         return render(request,'login_form.html',{'message':message,'show_toast':True,'success':success})                

        else:
            # messages.error(request, 'Invalid username or password')
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
    except Patient.DoesNotExist:
        # If not a Patient, check if the user has a related Doctor profile
        try:
            profile = Doctor.objects.get(user=user)
            profile_type = 'doctor'
        except Doctor.DoesNotExist:
            profile = None
            profile_type = None

    return render(request, 'profile.html', {'profile': profile, 'profile_type': profile_type})

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
        # Optionally, redirect to a success page or another URL
        # return redirect('signup_success')
        # return HttpResponse("success")
        return render(request,'signup_form.html',{'message':message, 'show_toast': True,'success':success})

    