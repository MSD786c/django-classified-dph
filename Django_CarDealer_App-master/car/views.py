import os
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Car, Client, Privacy, Ads
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.core.management import call_command
from django.conf import settings
from .models import CarImage
from django.core.mail import send_mail
from . models import *
from PIL import Image, ImageDraw, ImageFont

# installed rate limit
# from ratelimit.decorators import ratelimit

import random




# Home page
def index(request):
    allcars = Car.objects.all().prefetch_related('images')
    total_vehicles = allcars.count()
    featured_cars = random.sample(list(allcars), min(3, total_vehicles))
    
    cars_with_images = []
    for car in featured_cars:
        car_images = car.images.all()
        main_image = car_images.first()  # Remove the filter for is_main
        cars_with_images.append({
            'car': car,
            'main_image': main_image
        })
    
    context = {
        'allcars': allcars,
        'total_vehicles': total_vehicles,
        'featured_cars': cars_with_images
    }
    return render(request, 'index-3.html', context)

# list all cars on the used car page
def listing_classic(request):
    
    allcars = Car.objects.all()

    paginator = Paginator(allcars, 8) # Show 8 contacts per page.

    page_number = request.GET.get('page')
    allcars= paginator.get_page(page_number)
    total_vehicles = Car.objects.count()
    context = {'allcars':allcars, 'total_vehicles':total_vehicles}
    return render(request, 'listing-classic.html', context)

# display car details
def listing_detail(request, myid):
    car = Car.objects.filter(id=myid).prefetch_related('images').first()

    if not car:
        return HttpResponseRedirect('/')  # Redirect to home if car not found

    # using django sessions
    # is otp verified or not?
    otp_verified = False
    if request.session.get('otp_verified') != None:
        otp_verified = True
    else:
        otp_verified = False
    
    car_images = car.images.all()
    
    context = {
        'car': car,
        'car_images': car_images,
        'otp_verified': otp_verified
    }

    return render(request, 'listing-detail.html', context)

# search page function
def search(request):
    if request.method=='GET':
        car_city = request.GET.get('city')
        vehicle_type = request.GET.get('vehicle_type')
        slider_range = request.GET.get('slider')
        range_list = slider_range.split(",")
        min = range_list[0]
        max = range_list[1]
        price_result = Car.objects.filter(expected_selling_price__range=(min, max))
        # price_result = Car.objects.raw('select expected_selling_price from car_car where expected_selling_price between "'+min+'" and "'+max+'" ')
        
        allcars = Car.objects.all()
        # vehicle_type=vehicle_type
        if car_city == "Select Location" and vehicle_type == "Select Vehicle Type" :
            result = Car.objects.all()
        elif car_city == "Select Location" :
            result = Car.objects.all().filter(vehicle_type= vehicle_type)
        elif vehicle_type == "Select Vehicle Type":
            result = Car.objects.all().filter(car_city = car_city)
        else:
            result = Car.objects.all().filter(car_city = car_city, vehicle_type= vehicle_type)
        
        # intersecting two dictionaries

        final_dict = result & price_result
        
        total_vehicles = len(final_dict)
      
        context = {'result':final_dict, 'allcars':allcars, 'total_vehicles':total_vehicles}


        return render(request, 'search.html', context)

# All cars sorting by price
def sort(request):
    if request.method=='GET':
        sort = request.GET.get('sort')
        sorted = Car.objects.all()
        if sort == "Price (low to high)" :
            sorted = Car.objects.order_by("expected_selling_price")
            
            # set a variable so that sort.html change its choice according to the previous choice 
            low_to_high = True

        elif sort == "Price (high to low)" :
            sorted = Car.objects.order_by("-expected_selling_price")

            # set a variable so that sort.html change its choice according to the previous choice 
            low_to_high = False

        total_vehicles = sorted.count()
        allcars = Car.objects.all()
        context = {'sorted':sorted,'allcars':allcars, 'total_vehicles':total_vehicles, 'low_to_high': low_to_high}

        return render(request, 'sort.html', context)


#Search page sorting by price
def search_sort(request):
    if request.method=='GET':
        sort = request.GET.get('sort')
        
        # use session to get allcars from search page 
        all_search_page_cars = request.session.get('allcars')
        
        if sort == "Price (low to high)" :
            sorted = Car.objects.order_by("expected_selling_price")
            
        elif sort == "Price (high to low)" :
            sorted = Car.objects.order_by("-expected_selling_price")

        total_vehicles = sorted.count()
        allcars = Car.objects.all()
        context = {'sorted':sorted,'allcars':allcars, 'total_vehicles':total_vehicles}

        return render(request, 'sort.html', context)


 # Add a Car
@login_required(login_url='/#loginModal')
def post_vehicle(request):
    if request.method == 'POST':
        car_data = {
            'car_city': request.POST.get('emirate'),
            'car_manufacturer': request.POST.get('makeModel').split()[0],
            'car_model': ' '.join(request.POST.get('makeModel').split()[1:]),
            'trim': request.POST.get('trim'),
            'regional_spec': request.POST.get('regionalSpec'),
            'make_year': request.POST.get('year'),
            'kilometer_driven': request.POST.get('kilometers'),
            'body_type': request.POST.get('bodyType'),
            'is_insured': request.POST.get('insured') == 'Yes',
            'expected_selling_price': request.POST.get('price'),
            'car_owner_phone_number': request.POST.get('phoneNumber'),
            'listing_title': request.POST.get('title'),
            'tour_url': request.POST.get('tourURL'),
            'car_description': request.POST.get('description'),
            'fuel_type': request.POST.get('fuelType'),
            'transmission_type': request.POST.get('transmissionType'),
            'seating_capacity': request.POST.get('seatingCapacity'),
            'horsepower': request.POST.get('horsepower'),
            'engine_capacity': request.POST.get('engineCapacity'),
            'steering_side': request.POST.get('steeringSide'),
            'car_location': request.POST.get('locateCar'),
            'user': request.user,
            'vehicle_type': 'Car',
            
        }
        

        # Convert numeric fields
        for field in ['make_year', 'kilometer_driven', 'expected_selling_price', 'car_owner_phone_number']:
            try:
                car_data[field] = int(car_data[field])
            except (ValueError, TypeError):
                car_data[field] = None

        # Handle extras
        extras = request.POST.getlist('extras[]')
        for extra in ['climate_control', 'dvd_player', 'keyless_entry', 'navigation_system', 
                      'premium_sound_system', 'cooled_seats', 'front_wheel_drive', 
                      'leather_seats', 'parking_sensors', 'rear_view_camera']:
            car_data[extra] = extra in extras

        car = Car(**car_data)
        car.save()
        # Handle car images
        car_images = request.FILES.getlist('carImages')
        for image in car_images:
            car_image = CarImage(car=car, image=image)
            car_image.save()

      # Attempt to send an email notification
        try:
            send_mail(
                'New Ad Submitted',
                'Dear Admin, a new ad has been posted by {}'.format(request.user.email),
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Your vehicle has been successfully posted.")
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")

        return redirect('/')

    
    return render(request, 'post-vehicle.html')

from django.db.models import Q
from django.shortcuts import render
from .models import Car

def filter_cars(request):
    if request.method == 'GET':
        # Start with all cars
        cars = Car.objects.all()

        # Create an empty Q object to build our query
        query = Q()

        # Get filter parameters from the GET request
        make = request.GET.get('make')
        model = request.GET.get('model')
        min_year = request.GET.get('minYear')
        max_year = request.GET.get('maxYear')
        min_price = request.GET.get('minPrice')
        max_price = request.GET.get('maxPrice')
        max_kilometers = request.GET.get('maxKilometers')
        min_kilometers = request.GET.get('minKilometers')
        
        steering_side = request.GET.get('steeringSide')
        cylinders = request.GET.get('cylinders')
        color = request.GET.get('color')
        seats = request.GET.get('seats')
        regional_spec = request.GET.get('regionalSpecs')
        fuel_type = request.GET.get('fuelType')
        transmission_type = request.GET.get('gearbox')
        car_city = request.GET.get('locationCity')
        is_insured = request.GET.get('wr')
        # Print all values coming from the GET request
        print("Filtering parameters:")
        for key, value in request.GET.items():
            print(f"{key}: {value}")
        # Apply filters using Q objects
        if make:
            query &= Q(car_manufacturer__icontains=make)
        if model:
            query &= Q(car_model__icontains=model)
        if min_year and max_year:
            query &= Q(make_year__range=(min_year, max_year))
        elif min_year:
            query &= Q(make_year__gte=min_year)
        elif max_year:
            query &= Q(make_year__lte=max_year)
        if min_price and max_price:
            query &= Q(expected_selling_price__range=(min_price, max_price))
        elif min_price:
            query &= Q(expected_selling_price__gte=min_price)
        elif max_price:
            query &= Q(expected_selling_price__lte=max_price)
        if min_kilometers and max_kilometers:
            query &= Q(kilometer_driven__range=(min_kilometers, max_kilometers))
        elif min_kilometers:
            query &= Q(kilometer_driven__gte=min_kilometers)
        elif max_kilometers:
            query &= Q(kilometer_driven__lte=max_kilometers)
        if steering_side:
            query &= Q(steering_side__icontains=steering_side)
        if cylinders:
            query |= Q(engine_capacity__icontains=cylinders)
        if color:
            query |= Q(body_type__icontains=color)
        if seats:
            query |= Q(seating_capacity=seats)
        if regional_spec:
            query |= Q(regional_spec=regional_spec)
        if fuel_type:
            query |= Q(fuel_type=fuel_type)
        if transmission_type:
            query |= Q(transmission_type=transmission_type)
        if car_city:
            query |= Q(car_city=car_city)
        if is_insured:
            query |= Q(is_insured=True)
        # Apply the query to filter the cars
        cars = cars.filter(query)
        print(cars)
        # Prefetch related images for each car
        cars = cars.prefetch_related('images')
        print(cars)
        # Prepare cars with images for the template
        cars_with_images = []
        for car in cars:
            car_images = car.images.all()
            main_image = car_images.first()
            cars_with_images.append({
                'car': car,
                'main_image': main_image
            })

        # Return filtered results
        context = {
            'cars': cars_with_images,
            'filter_applied': True
        }
        return render(request, 'filtered-cars.html', context)

    # If it's not a GET request, just render the form
    return render(request, 'filter-form.html')



#Display users vehicles
@login_required(login_url='/#loginModal')
def my_vehicles(request):
    cars = Car.objects.filter(user = request.user)
    context = {'cars':cars}
    
    return render(request, 'my-vehicles.html', context)

#Delete user vehicle
@login_required(login_url='/#loginModal')
def delete_vehicles(request, myid):
    obj = get_object_or_404(Car, id=myid)
    try:
        call_command('dbbackup')
    except:
        pass
    if request.method == "POST":
        obj.delete()
        return redirect('/my-vehicles.html')
    
    return render(request, 'my-vehicles.html', {})

#User profile setting
@login_required(login_url='/#loginModal')
def profile_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'Please retry for password change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile-settings.html', {
        'form': form
    })
    

#About us page
# @ratelimit(key='ip', rate='3/m', block=True)
def about_us(request):
    return render(request, 'about-us.html', {})



#Signup page
# @ratelimit(key='ip', rate='10/h', block=True)
def signup(request):
    if request.method == 'POST':
        #get the form parameters
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        

        #checks
        if len(username)>15:
            messages.error(request, "Username must be under 15 characters")
            # return redirect('/')
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            # return redirect(request.META['HTTP_REFERER'])
            return redirect(signup_url)
        
        # unique username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            # return redirect('/')
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        # unique email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            # return redirect(request.META['HTTP_REFERER'])
            return redirect(signup_url)
        
        if pass1 != pass2:
            messages.error(request, "Password do Not match")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)
        
        if len(pass1)<6:
            messages.error(request, "Password length must be greater than 6")
            signup_url = request.META['HTTP_REFERER'] + "#signupModal"
            return redirect(signup_url)




        # create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request, "Your account has been created")
        
        
        # login with same details
        user = authenticate(username=username, password =pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid Credentials")
            # return redirect(request.META['HTTP_REFERER'])
            login_url = request.META['HTTP_REFERER'] + "#loginModal"
            return redirect(login_url)

        # return redirect('/')
        return redirect(request.META['HTTP_REFERER'])
    
    else:
        return HttpResponse('404- Not Found')


#User Login Modal
# @ratelimit(key='ip', rate='10/h', block=True)  
def login_model(request):
    if request.method == 'POST':
        #get the form parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        
        user = authenticate(username=loginusername, password =loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            # return redirect('/')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, "Invalid Credentials")
            # return redirect('/')
            # return redirect(request.META['HTTP_REFERER'])
            login_url = request.META['HTTP_REFERER'] + "#loginModal"
            return redirect(login_url)
    return HttpResponse("404- Not Found")

#User Logout Modal
def logout_model(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    # return redirect('/')
    return redirect(request.META['HTTP_REFERER'])

# Privacy Page
def privacy(request):
    # return HttpResponse("this is homepage")
    
    policy = Privacy.objects.all()
    context = {'policy':policy[0]}
    
    
    return render(request, 'privacy.html', context)


# Submit phone number to access details
# @ratelimit(key='ip', rate='10/h', block=True)
def submit_number(request):
    global message
    global ph_number
    global otp_car_id
    if request.method == 'POST':
        #get the form parameters
        ph_number = request.POST['phone_number']
        ph_number = int(ph_number)
        request.session['session_phone_number'] = ph_number
        ph_name = request.POST['phone_name']
        request.session['session_phone_name'] = ph_name
        
        otp_car_id = request.POST['car_id']
        request.session['session_otp_car_id'] = otp_car_id
        
        # session for phone number which is already in database
        if  Client.objects.filter(phone_number=int(request.session['session_phone_number'])).exists():
            request.session['otp_verified'] = True
            # rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#get_details'
            rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])

            return redirect(rel_url)
        else:
            
            request.session['session_otp']=generate_otp_message(request)
            
            # return HttpResponseRedirect(request.path_info)
            re_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#submit_otp'
            # return render(request, re_url, context)
            return redirect(re_url)

    else:
        return HttpResponse("404- Not Found for submit number")

#Submit the OTP
def submit_otp(request):
    if request.method == 'POST':
        #get the form parameters
        get_otp = request.POST['get_otp']
        if int(get_otp) == int(request.session['session_otp']):
            
            client = Client(name=request.session['session_phone_name'], phone_number=int(request.session['session_phone_number']))
            client.save()
            # sessions for otp verified person
            request.session['otp_verified'] = True

            # rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#get_details'
            rel_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])

            return redirect(rel_url)

        else:
            r_url = 'listing-detail.html/'+str(request.session['session_otp_car_id'])+'/#submit_otp'
            return redirect(r_url)
        
    return HttpResponse("404- Details Not Found for submit otp")



# Desclaimer page
def disclaimer(request):
    return render(request, 'Disclaimer.html')

def contact_us(request):
    return render(request, 'contact-us.html')

def privacy(request):
    return render(request, 'privacy.html')
# License plates page

from .models import LicensePlate
from decimal import Decimal


def license_plates(request):
    """
    Single view function to handle displaying and filtering license plates.
    """
    # If GET request, parse query params:
    if request.method == 'GET':
        # Retrieve form inputs from GET parameters
        city         = request.GET.get('city', '').strip()
        code         = request.GET.get('code', '').strip()
        digits       = request.GET.get('digits', '').strip()
        contains     = request.GET.get('contains', '').strip()
        starts_with  = request.GET.get('starts_with', '').strip()
        ends_with    = request.GET.get('ends_with', '').strip()
        plate_format = request.GET.get('plate_format', '').strip()
        min_price    = request.GET.get('min_price', '').strip()
        max_price    = request.GET.get('max_price', '').strip()

        # Start with all license plates
        query = LicensePlate.objects.all()

        # Filter by city
        if city:
            query = query.filter(city__icontains=city)

        # Filter by code
        if code:
            query = query.filter(code__icontains=code)

        # Filter by digits
        if digits:
            query = query.filter(digits=digits)

        # Filter by substring anywhere
        if contains:
            query = query.filter(number__icontains=contains)

        # Filter by "starts with"
        if starts_with:
            query = query.filter(number__startswith=starts_with)

        # Filter by "ends with"
        if ends_with:
            query = query.filter(number__endswith=ends_with)

        # Filter by plate_format
        if plate_format:
            query = query.filter(plate_format__icontains=plate_format)

        # Filter by min_price
        if min_price:
            try:
                min_price_val = Decimal(min_price)
                query = query.filter(price__gte=min_price_val)
            except (ValueError, TypeError):
                pass  # Ignore or log error

        # Filter by max_price
        if max_price:
            try:
                max_price_val = Decimal(max_price)
                query = query.filter(price__lte=max_price_val)
            except (ValueError, TypeError):
                pass  # Ignore or log error

        # Debugging line (optional)
        print("Filtered query:", query.query)

        return render(request, 'license-plates.html', {
            'license_plates': query
        })

    # If not a GET request, just show all plates (you can decide how to handle POST)
    all_plates = LicensePlate.objects.all()
    return render(request, 'license-plates.html', {
        'license_plates': all_plates
    })


def submit_ad(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        code = request.POST.get('code')
        digits = request.POST.get('digits')
        number = request.POST.get('number')
        price = request.POST.get('price')
        plate_format = request.POST.get('plate_format')

        try:
            new_plate = LicensePlate(
            city=city,
            code=code,
            digits=digits,
            number=number,
            price=price if price else None,  # Ensure this matches the model definition
            plate_format=plate_format
            )
            new_plate.save()
            messages.success(request, "License plate added successfully!")
            return redirect('license_plates')
        except Exception as e:
            messages.error(request, f"Error submitting ad: {e}")
            return redirect('numberplate')

    else:
        return render(request, 'numberplateform.html')

def numberplates(request):
    return render(request, 'numberplateform.html')

