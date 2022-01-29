from fileinput import filename
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .detector import detect
import os
from datetime import datetime
from .models import Image
from django.http.response import JsonResponse
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/signin/')
@csrf_exempt
def index(request):
    return render(request, 'lai_detector_app/index.html')

@login_required(login_url='/signin/')
@csrf_exempt
def predict_lai(request):
    fileName, fileExtension = os.path.splitext(request.POST.get('filename'))

    now = datetime.now()
    date_time = now.strftime("%d_%m_%Y_%H_%M_%S")
    image = Image(path = "images/%s/"%date_time, image_file=request.FILES['file'])
    image.save()

    uploaded_path = image.image_file.url

    try:
        detected_output_image_path, output_image_path, LAI, FVC, coords = detect(uploaded_path, image.id)

        # image = Image.objects.get(path=detected_path)
        return JsonResponse({
            'imageID': image.id,
            'LAI': LAI,
            'FVC': FVC,
            'error': 'no',
            'destination': uploaded_path,
            'detectedOutputImage': detected_output_image_path,
            'outputImage': output_image_path,
            'meta': list(coords),
        })
    except Exception as e:
        import traceback, sys
        print(traceback.format_exc())
        # print(sys.exc_info()[2])
        return JsonResponse({'error': 'err', 'message': 'Internal server error'})

    return render(request, 'lai_detector_app/index.html')

def signin(request):
    return render(request, 'lai_detector_app/login.html')

def login(request):
    username = request.POST['login']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        authlogin(request, user)

        return redirect('index')

    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    return render(request, 'lai_detector_app/login.html', {'error': 'Incorrect username or password'})

def logout(request):
    authlogout(request)

    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            authlogin(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()


    return render(request, 'lai_detector_app/signup.html', {'form': form})
