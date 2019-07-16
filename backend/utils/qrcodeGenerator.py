import qrcode,math
from qrcode.image.pil import PilImage
from StringIO import StringIO
from PIL import Image,ImageOps
def make_qrcode(name,party,pin,err='M',bxsize=5):

	#error correction constants
	if err=='L':
		err_c=qrcode.constants.ERROR_CORRECT_L
	elif err=='M':
		err_c=qrcode.constants.ERROR_CORRECT_M
	else:
		err_c=qrcode.constants.ERROR_CORRECT_H

	#qrcode constants
	qr=qrcode.QRCode(
		version=None,
		error_correction=err_c,
		box_size=bxsize,
		border=1,
                image_factory=PilImage
		)

	#qrcode creation
	text=name+'\n'+party+'\n'+pin
	qr.add_data(text)
	qr.make(fit=True)
	obj=StringIO()
	img=qr.make_image()
	img.save(obj,format='PNG') #do this because the qrcode is not genrated as a pil object
	obj.seek(0)

	return Image.open(obj)# return it as a PIL object

def consise_rect_translation(a,r):
        x=round(math.sqrt(a)*math.sqrt(r))
        y=round(math.sqrt(a)/math.sqrt(r))
        return int(x),int(y)

def add_logo(qr,logo,perc=5):
	qr_width,qr_height=qr.size
	lg_width,lg_height=logo.size
	qr_area,lg_area=[qr_width*qr_height,
                        lg_width*lg_height]

	perc_area=(qr_area*perc*1.0)/100
	w_h_ratio=round((lg_width*1.0)/lg_height)
	perc_width,perc_height=consise_rect_translation(
                                    perc_area,w_h_ratio)

	logo=logo.resize((perc_width,perc_height),Image.ANTIALIAS)
	master_img=Image.new('RGBA', (qr_width, qr_height), 'black')
	master_img.paste(qr,(0,0))

	lg_width,lg_height=logo.size
	center=((qr_width/2)-lg_width/2,(qr_height/2)-lg_height/2)
 	logo=ImageOps.expand(logo,border=1,fill='orange')
	master_img.paste(logo,center)
	return master_img

def init(name,party='',pin='',url='qrcode.png',logo='logo.png',as_pil=True):
	logo=Image.open('logo.png')
	qr=make_qrcode(name,party,pin)
	out=add_logo(qr,logo)
	if not as_pil:
		out.show()
		out.save(url)
		return url
	else:
		return out
#demo: just run this or remove the '#'
#put'logo.png' in the working directory
#when using init it produces the qrcode, correctly adjust the logo and save or return a pil object/class
#init("kigali International Comedy Festival Reserved Ticket ",'Code:KCF1CT ','tike.co.rw')
#here you create the qrcode only returned as a pil object/class
#qr=make_qrcode('https://thepiratebay.org/torrent/12667686/KMSpico_10.1.8_FINAL___Portable_(Office_and_Windows_10_Activator','','')
#qr.save('sweet_music_link.png')
#qr.show()

