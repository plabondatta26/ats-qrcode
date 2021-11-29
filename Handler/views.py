from django.shortcuts import render, redirect
import qrcode
from datetime import datetime
import cv2
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from .forms import *
import webbrowser
from django.http import HttpResponse
import ast
from segno import helpers


def create_qrcode(data):
    timestamp = round(datetime.now().timestamp())
    filename = 'media/qr_images/' + str(timestamp) + '.png'
    qrcode = helpers.make_vcard(
        name=data['name'], displayname=data['name'], email=data['email'],
        phone=data['phone'], fax=data['fax'], videophone=data['videophone'], memo=data['memo'],
        nickname=data['nickname'], birthday=data['birthday'], url=data['url'],
        pobox=data['pobox'], street=data['street'], city=data['city'], region=data['region'],
        zipcode=data['zipcode'], country=data['country'], org=data['org'], lat=data['lat'], lng=data['lng'],
        title=data['title'], photo_uri=data['photo_uri']
    )
    qrcode.save(filename, scale=4)
    return str(timestamp) + '.png'


def decode_qrcode(dirs):
    dirs = 'media/qr_up_images/' + dirs
    image = cv2.imread(dirs)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(image)
    print(data)
    print(bbox)
    if data:
        x = data.split('/')
        if x[0] == 'http:' or x[0] == 'https:' or x[0] == 'www':
            return webbrowser.open(data)
        else:
            return data
    else:
        return "There was some error"


def home(request):
    if request.method == 'POST':
        dirs = create_qrcode(request.POST)
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
    # return redirect('result', x, 'text')
    return HttpResponse(x)


def detection(cam):
    try:
        a = ''
        detector = cv2.QRCodeDetector()
        while True:
            _, img = cam.read()
            # print(_, img)
            cv2.imshow('frame', img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            data, bbox, _ = detector.detectAndDecode(img)
            if data:
                a = data
                cv2.imwrite("testfilename.jpg", img)
                print(a)
                cam.release
                return a
            else:
                pass
                # return "Error"
    except:
        return 'Failed to open camera'


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
                    # return redirect('result', qr_text, 'text')
                    return HttpResponse(qr_text)
    return qr_text


def result(request, data, form):
    dict_data = ''
    if form == 'img':
        data = '/media/qr_images/' + data
    else:
        dict_data = data
        dict_data = ast.literal_eval(dict_data)
    context = {
        'data': data,
        'format': form,
        'dict_data': dict_data
    }
    return render(request, 'result.html', context)


def test(request):
    return render(request, 'test.html')
