from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CanvasImage
from PIL import Image
import base64
from django.core.files.base import ContentFile
from .LeNet import LeNet5
from torch import load, device
from torchvision import transforms
from numpy import argmax
from pathlib import Path

# Create your views here.

img_url = None
pred_number = None

def get_image_from_data_url(data_url):
    _format, _dataurl = data_url.split(';base64,')
    _filename, _extension = 'digit_picture', 'png'
    file = ContentFile( base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")
    return file 

@csrf_exempt
def home(request):
    
    if request.method == 'POST':
        
        if 'submit-canvas' in request.POST:
            global img_url
            img_url = request.POST.get('image')
            imgdata = get_image_from_data_url(img_url)
            
            PATH = Path.cwd()

            model = LeNet5(10)
            model.load_state_dict(load(PATH / 'base/LeNet.pt', map_location=device('cpu')))

            data = Image.open(imgdata).convert("L")

            resize_transform = transforms.Compose(
                [transforms.Resize((32, 32)),
                transforms.ToTensor(),
                transforms.Normalize((0,), (1,))  # standarize data with zero means and unit variance
                ]
            )
            data = resize_transform(data)

            if data.sum() == 0:
                context = {'result': "Blank canvas - No prediction", 'img_url': img_url}
            else:
                data = data.unsqueeze(0)
                _, output = model(data)
                prediction = argmax(output.detach().numpy())
                
                global pred_number
                pred_number = prediction
                
                context = {'result': "Your image produces number " + str(prediction), 'img_url': img_url}
            return render(request, 'base/home.html', context)
        
        elif 'error-detect' in request.POST:
            return render(request, 'base/detect.html', {'img_url': img_url})
        
        elif 'confirm-detect' in request.POST:
            # global img_url
            imgdata = get_image_from_data_url(img_url)
            img = CanvasImage.objects.create(
                image = imgdata,
                result = request.POST.get("correct_number"),
                predict = str(pred_number)
            )
            img.save()
            return redirect('home')
    else:
        context = {}
        return render(request, 'index.html', context)

