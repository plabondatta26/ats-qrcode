from django.shortcuts import render, redirect
from datetime import datetime
import cv2
from .forms import *
import webbrowser
import ast
from segno import helpers
from PIL import Image
from pyzbar.pyzbar import decode
import codecs
import ast
import vobject


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
    # try:
    return_data = {}
    dirs = 'media/qr_up_images/' + dirs
    data = decode(Image.open(dirs))
    vcard_data = ''
    for i in data[0]:
        vcard_data: str = codecs.decode(i, 'UTF-8')
        break
    vcard = vobject.readOne(vcard_data)
    return_data["Name"] = vcard.contents['fn'][0].value
    telephone = {}
    for tel in vcard.contents['tel']:
        i = dict((key, getattr(tel, key)) for key in dir(tel) if key not in dir(tel.__class__))
        if len(i["params"]) > 0:
            for j, k in i["params"].items():
                print(k[0])
                if k[0] == "FAX" and i["value"]:
                    return_data["FAX"] = i["value"]
                elif k[0] == "VIDEO" and i["value"]:
                    return_data["Video"] = i["value"]
        else:
            return_data["Phone"] = i["value"]

    return_data["Email"] = vcard.contents['email'][0].value
    return_data["Birthday"] = vcard.contents['bday'][0].value
    return_data["Nickname"] = vcard.contents['nickname'][0].value
    return_data["Address"] = vcard.contents['adr'][0].value
    return_data["Website"] = vcard.contents['url'][0].value
    return return_data
    # except:
    #     return "There is some error"


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
            return render(request, 'qr_to_text_view.html', {'data': dt})
    return render(request, 'qr_to_text_view.html', {'data': ''})


#
# def video_qr_code(request):
#     x = camera()
#     print(type(x))
#     # return redirect('result', x, 'text')
#     return HttpResponse(x)
#
#
# def detection(cam):
#     try:
#         a = ''
#         detector = cv2.QRCodeDetector()
#         while True:
#             _, img = cam.read()
#             # print(_, img)
#             cv2.imshow('frame', img)
#             cv2.waitKey(1000)
#             cv2.destroyAllWindows()
#             data, bbox, _ = detector.detectAndDecode(img)
#             if data:
#                 a = data
#                 cv2.imwrite("testfilename.jpg", img)
#                 print(a)
#                 cam.release
#                 return a
#             else:
#                 pass
#                 # return "Error"
#     except:
#         return 'Failed to open camera'
#
#
# def camera():
#     qr_text = 'Failed to open camera'
#     for i in range(-5, 5):
#         cam = cv2.VideoCapture(i)
#         if cam is None or not cam.isOpened():
#             if i == 5:
#                 return "Failed to open camera"
#         else:
#             qr_text = detection(cam)
#             if qr_text:
#                 x = str(qr_text).split('/')
#                 if x[0] == 'http:' or x[0] == 'https:' or x[0] == 'www':
#                     return webbrowser.open(qr_text)
#                 else:
#                     # return redirect('result', qr_text, 'text')
#                     return HttpResponse(qr_text)
#     return qr_text


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
