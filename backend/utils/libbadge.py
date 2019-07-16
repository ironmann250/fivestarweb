#from  tickapp.utils 
import qrcodeGenerator
from PIL import Image,ImageFont,ImageDraw,ImageOps

#why not make this into a class for a change :) (lot's of coffee lol)
#nahh speedy, no time to structure

#init vals, make it as dict to use it directly in a loop

user_vals={'pin':'No: 123456','name':'From: china, yiwu','title':'To: rwanda, kigali'}
#core vals
#messed the filesys with fonts...
#compute size from text? later now no more than 30 chars(further work more coffee)
size=(450,150)#width,height
text_pos=[125,65]#array cause it changes at somepoint
qrcode_pos=(5,20)
pin_pos=(125,25)
font_name,font_size=['Helvetica-Normal.ttf',30]
color='white' #maybe light gray? front always black


#init vals
canvas=Image.new("RGB",size,color)
font = ImageFont.truetype(font_name, font_size)
qrcode=qrcodeGenerator.init(user_vals['pin'])#or use make_qrcode 

#vals to write on image

def make_badge(bias=10):
	global canvas,font,qrcode,user_vals
	global text_pos,pin_pos,qrcode_pos
	#resize qrcode to 100 by 100 px and add it to main image
	qrcode.thumbnail((140,140),Image.ANTIALIAS)#if buggy use consise_rect algo
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

