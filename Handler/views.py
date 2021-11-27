from django.shortcuts import render, redirect
import qrcode
from datetime import datetime
import cv2
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from .forms import *
import webbrowser


# Create your views here.

def create_qrcode(data):
    timestamp = round(datetime.now().timestamp())
    filename = 'media/qr_images/' + str(timestamp) + '.png'
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img.save(filename)
    return str(timestamp) + '.png'


def decode_qrcode(dirs):
    dirs = 'media/qr_up_images/' + dirs
    image = cv2.imread(dirs)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

    if vertices_array is not None:
        x = data.split('/')
        if x[0] == 'http:' or x[0] == 'https:' or x[0] == 'www':
            return webbrowser.open(data)
        else:
            return data
    else:
        return "There was some error"


def home(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        dirs = create_qrcode(text)
        return redirect('result', dirs, 'img')
    return render(request, 'index.html', {'dirs': ''})


def qr_to_text_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data = QrCodeModel.objects.last()
            data = str(data.image.url).split('/')[-1]
            dt = decode_qrcode(data)
            return redirect('result', dt, 'text')
    return render(request, 'qr_to_text_view.html')


def result(request, data, form):
    if form == 'img':
        data = '/media/qr_images/' + data
    context = {
        'data': data,
        'format': form
    }
    return render(request, 'result.html', context)
