import qrcode
from django.http import HttpResponse
from datetime import datetime
import cv2
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


# Create your views here.

def create_qrcode(data):
    timestamp = round(datetime.now().timestamp())
    filename = 'media/qr_images/' + str(timestamp) + '.png'
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img.save(filename)
    return filename


def decode_qrcode(dirs):
    image = cv2.imread(dirs)
    detector = cv2.QRCodeDetector()
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)
    if vertices_array is not None:
        return data
    else:
        return "There was some error"


def home(request):
    text = 'The install worked successfully! Congratulations!'
    dirs = create_qrcode(text)
    dt = decode_qrcode(dirs)
    return HttpResponse(dt)
