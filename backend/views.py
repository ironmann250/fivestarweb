# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from backend.models import *
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import string,random
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from backend.utils import qrcodeGenerator
from StringIO import StringIO
from PIL import Image,ImageFont,ImageDraw,ImageOps
# Create your views here.


def save_to_string(img):
    obj=StringIO()
    img.save(obj,format='JPEG',quality=90)
    obj.seek(0)
    return obj.read() 

def render_qrcode(request,text):#text is pin #this is considered a helper function not really a view func
    text=web_url+'result?pin='+text
    qrcode=save_to_string(qrcodeGenerator.init(text)) #render and save it in mem
    response=HttpResponse(qrcode,content_type='image/jpeg') 
    return response


def make_badge(user_vals,qrcode, bias=10):
	size=(450,150)#width,height
	text_pos=[125,65]#array cause it changes at somepoint
	qrcode_pos=(5,20)
	pin_pos=(125,25)
	font_name,font_size=['Helvetica-Normal.ttf',30]
	color='white' #maybe light gray? front always black
	canvas=Image.new("RGB",size,color)
	font = ImageFont.truetype(font_name, font_size)

	#resize qrcode to 100 by 100 px and add it to main image
	qrcode.thumbnail((100,100),Image.ANTIALIAS)#if buggy use consise_rect algo
	canvas.paste(qrcode,qrcode_pos)
	# text stuffs now
	drawHandler = ImageDraw.Draw(canvas)
	#write line get dimensions to compute newline
	#name
	drawHandler.text(text_pos, user_vals['name'], (0,0,0), font=font)
	textlen=font.getsize(user_vals['name'])
	text_pos[1]=text_pos[1]+textlen[1]+bias#adjust the bias as needed
	#title
	drawHandler.text(text_pos, user_vals['title'], (0,0,0), font=font)
	#code
	drawHandler.text(pin_pos, user_vals['pin'], (0,0,0), font=font)
	#show
	return canvas

def get_packagenum(size=8, chars=string.ascii_uppercase + string.digits):
    """
    generate a 6 character pi that is unique in db
    """
    pin=''.join(random.choice(chars) for _ in range(size))
    if PACKAGE.objects.filter(packagenum=pin).count() !=0:
        id_generator()
    else:
        return pin

def postprocess(request,fields,exc=['',None]):
	'''
	process post variables and return a list
	'''
	data=[]
	for f in fields:
		if request.POST[f].strip() not in exc:
			data.append(request.POST[f])
		else:
			return None
	return data

def getprocess(request,fields,exc=['',None]):
	'''
	process post variables and return a list
	'''
	data=[]
	for f in fields:
		if request.GET[f].strip() not in exc:
			data.append(request.GET[f])
		else:
			return None
	return data
def add_status(request,code,action=''):
	if code in [0,1,2,3,4]:
		known_actions=['package created','package paid', 'package departed'
		 , 'package arrived', 'package picked up']
		action=known_actions[code]
	if request.user.is_authenticated:
		user=request.user
	else:
		raise SyntaxError
	stat=STATUS(user=user,code=code,action=action)
	stat.save()
	return stat

def index(request):
	if request.user.is_authenticated:
		user=request.user
	else:
		user=None
	return render(request,'index.html',locals())

#@login_required
def add(request):
	try:
		sender_name, sender_phone, receiver_name, receiver_phone, destination, weight, price, description=postprocess(request,['sender_name', 'sender_phone', 'receiver_name', 'receiver_phone', 'destination', 'weight', 'price', 'description'])
		stat=add_status(request,0)
		package=PACKAGE(sender_name = sender_name, sender_phone =  sender_phone,
		 receiver_name =  receiver_name, receiver_phone =  receiver_phone,
		  destination =  destination, init_weight =  weight,packagenum=get_packagenum(),
		   init_price =  price, description =  description,status=stat)
		package.save()
		#put in db and redirect to added
		return HttpResponseRedirect('/added/'+package.packagenum)

	except Exception as e:
		print e
		return render(request,'add.html',locals())

#@login_required
def added(request,packagenum):
	package=get_object_or_404(PACKAGE, packagenum=packagenum)
	return render(request,'added.html',locals())

def package(request,packagenum):
	package=get_object_or_404(PACKAGE, packagenum=packagenum)
	return render(request,'package.html',locals())

def search(request):
	data=[]
	try:
		keyword=getprocess(request,['keyword'])[0]
		print keyword
		if keyword not in ["","null"," "]:
			sch=SEARCH(isregistered=request.user.is_authenticated, keyword=keyword, creation_date=now())
			sch.save()
		fields=["sender_name",'sender_phone','receiver_phone','destination','packagenum']
		query_keywords=Q(sender_name__contains = keyword) | Q(sender_phone__contains = keyword) | Q(receiver_phone__contains = keyword) | Q(destination__contains = keyword) | Q(packagenum = keyword)
		print query_keywords
		packages=PACKAGE.objects.filter(query_keywords)
		return render(request,'search.html',locals())

	except Exception as e:
		print e
		packages=PACKAGE.objects.all()[:100]
		return render(request,'search.html',locals())

def renderTicket(request,packagenum):
	packagenum=packagenum.split('.')[0]
	package=PACKAGE.objects.get(packagenum=packagenum)
	#libbadge.init()
	#core vals
	#messed the filesys with fonts...
	#compute size from text? later now no more than 30 chars(further work more coffee)
	
	print packagenum
	url="http://127.0.0.1:8000/package/"
	user_vals={
	'pin':'No: '+package.packagenum,
	'name':"From: "+package.destination,
	'title':'To: '+package.receiver_phone
	}
	#init vals
	
	qrcode=qrcodeGenerator.init(url+package.packagenum)#or use make_qrcode 

	#vals to write on image
	badge_img=save_to_string(make_badge(user_vals, qrcode))
	response= HttpResponse(badge_img,content_type='image/jpeg')
	return response