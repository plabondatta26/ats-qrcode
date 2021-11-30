from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = QrCodeModel
        fields = '__all__'

#
# n
# fn
# org
# email
# tel
# url
# title
# photo
# nickname
# adr
# bday
# geo
# note

# def decode_qrcode(dirs):
#     return_data = {}
#     try:
#         dirs = 'media/qr_up_images/' + dirs
#         data = decode(Image.open(dirs))
#         key_list = {'Name': 'Name', 'Phone': 'Phone', 'FAX': 'FAX', 'org': 'Company', 'email': 'Email',
#                     'nickname': 'Nickname', 'adr': 'Address', 'bday': 'Birthday', 'url':'Website'}
#         vcard_data = ''
#         for i in data[0]:
#             vcard_data: str = codecs.decode(i, 'UTF-8')
#             break
#         vcard = vobject.readOne(vcard_data)
#         return_data["Name"] = vcard.contents['fn'][0].value
#
#         for tel in vcard.contents['tel']:
#             i = dict((key, getattr(tel, key)) for key in dir(tel) if key not in dir(tel.__class__))
#             if len(i["params"]) > 0:
#                 for j, k in i["params"].items():
#                     print(k[0])
#                     if k[0] == "FAX" and i["value"]:
#                         return_data["FAX"] = i["value"]
#                     elif k[0] == "VIDEO" and i["value"]:
#                         return_data["Video"] = i["value"]
#             else:
#                 return_data["Phone"] = i["value"]
#         for keys in vcard.contents:
#             if vcard.contents[keys][0].value and keys == key_list[keys]:
#                 return_data[key_list[keys]] = vcard.contents[keys][0].value
#         # if vcard.contents['bday'][0].value:
#         #     return_data["Birthday"] = vcard.contents['bday'][0].value
#         # if vcard.contents['nickname'][0].value:
#         #     return_data["Nickname"] = vcard.contents['nickname'][0].value
#         # if vcard.contents['adr'][0].value:
#         #     return_data["Address"] = vcard.contents['adr'][0].value
#         # if vcard.contents['url'][0].value:
#         #     return_data["Website"] = vcard.contents['url'][0].value
#         return return_data
#     except KeyError as ke:
#         return return_data
#
