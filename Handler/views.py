from django.shortcuts import render, redirect
import qrcode
from datetime import datetime
import cv2
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from .forms import *
import webbrowser
from django.http import HttpResponse


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


def video_qr_code(request):
    x = camera()
    print(type(x))
    return redirect('result', x, 'text')


def detection(cam):
    try:
        a = ''
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cam.read()
            data, bbox, _ = detector.detectAndDecode(img)
            if data:
                a = data
                cv2.imwrite("testfilename.jpg", img)
                print(a)
                cam.release
                return a
            else:
                return "Something went wrong"
    except:
        return HttpResponse("Failed to open camera")


def camera():
    qr_text = 'Failed to open camera'
    for i in range(-5, 5):
        cam = cv2.VideoCapture(i)
        if cam is None or not cam.isOpened():
            if i == 5:
                return "Failed to open camera"
        else:
            qr_text = detection(cam)
            if qr_text:
                x = str(qr_text).split('/')
                if x[0] == 'http:' or x[0] == 'https:' or x[0] == 'www':
                    return webbrowser.open(qr_text)
                else:
                    qr_text.replace('', '#')
                    return redirect('result', qr_text, 'text')
    return qr_text


def result(request, data, form):
    if form == 'img':
        data = '/media/qr_images/' + data
    context = {
        'data': data,
        'format': form
    }
    return render(request, 'result.html', context)
