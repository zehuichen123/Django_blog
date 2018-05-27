from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
#from .forms import SearchForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from PIL import Image
from .dhash import DHash
import requests
import re

from keras.models import load_model
from PIL import Image
import numpy as np
import tensorflow as tf

global graph,model
curr_path=os.path.abspath('.')
graph = tf.get_default_graph()
model=load_model(os.path.join(curr_path,'my_model.h5'))


def index(request):
	return render(request,"search/index.html")

def search_result(request):
	print('get here')
	if request.method == "POST":
		print("FUCC")
		print ("input" + request.POST.get("search_words"))
	
	return render(request,"search/result.html")

def compute_dhash(origin_img,compared_one):

	compared_img=Image.open(compared_one)

	hamming_distance = DHash.hamming_distance(origin_img, compared_img)

	return hamming_distance

def sort_result(result_list,upload_image):
	origin_img=Image.open(upload_image)
	computed_list=[]
	for each_image in result_list:
		computed_list.append((each_image,\
			compute_dhash(origin_img,each_image)))
	sorted_list=sorted(computed_list,key=lambda x:x[1])
	sorted_result=[]
	for each_compute_img in sorted_list:
		sorted_result.append(each_compute_img[0])
	return sorted_result


def check_img_size(check_type,file_list):
	type_to_size=[(0,0),(390,190),(1080,720),(1920,1080)]
	check_result_list=[]
	if check_type==0:
		return file_list
	for each_file in file_list:
		each_image=Image.open(each_file)
		image_size=each_image.size
		check_size=type_to_size[check_type]
		if abs(check_size[0]-image_size[0])<20 and\
				 abs(check_size[1]-image_size[1])<20:
			check_result_list.append(each_file)
	return check_result_list

def check_img_format(check_type,file_list):
	type_to_format=['','JPEG','PNG','GIF']
	check_result_list=[]
	if check_type==0:
		return file_list
	for each_file in file_list:
		each_image=Image.open(each_file)
		image_format=each_image.format
		check_format=type_to_format[check_type]
		if image_format==check_format:
			check_result_list.append(each_file)
	return check_result_list

def get_suggestions(prediction):
	suggest_dict={
		'airplane':['plane','飞行物','UFO','aircraft','飞机'],
		'ant':['ant','蚂蚁','昆虫','insect'],
		'butterfly':['蝴蝶','昆虫','butterfly','蛾子'],
		'chair':['chair','armchair','椅子','座椅','靠椅','躺椅'],
		'crab':['螃蟹','crab','钳子'],
		'cup':['cup','water glass','水杯','杯子','茶杯'],
		'garfield':['加菲猫','comic','漫画','Garfield'],
		'lamp':['lamp','台灯','灯','床灯','light'],
		'pizza':['pizza','food','披萨','吃货'],
		'rooster':['rooster','chicken','公鸡','鸡','母鸡'],
		'wild':['cat','wild cat','猫','野猫','小猫'],
		'yin':['yin-yang symbol','silhouette chart','阴阳图','Taiji Diagram','太极图']
	}
	return suggest_dict[prediction]

def upload(request):
	if request.method=="POST":
		#print(type(image))
		file_size=request.POST.get('file_size',0)
		#print(file_size)
		source_from=int(request.POST.get('source',0))
		#print(source_from)
		file_format=request.POST.get('format',0)
		#print(source)
		image=request.FILES.get('search_img',None)
		if image==None:
			return render(request,'search/index.html')
		curr_path=os.path.abspath('.')
		path=default_storage.save(os.path.join(curr_path,image.name),\
			ContentFile(image.read()))
		
		prediction=predict_category(image.name)
		print(prediction)
		
		#prediction='rooster'
		if source_from==0 or source_from==1:
			all_imgs=os.listdir(os.path.join(curr_path,'img'))
		else:
			all_imgs=os.listdir(os.path.join(curr_path,'picture'))
		result=[]
		suggestions=get_suggestions(prediction)
		
		for each_img in all_imgs:
			if each_img.find(prediction)!=-1:
				if source_from==0 or source_from==1:
					result.append('img/'+each_img)
				else:
					result.append('picture/'+each_img)

		result=check_img_size(int(file_size),result)
		result=check_img_format(int(file_format),result)

		
		if len(result)==0:
			opps='Opps! No results found!'
		else:
			opps=''
			result=sort_result(result,image.name)
		os.remove(os.path.join(curr_path,image.name))
		return render(request,"search/result.html",locals())

def predict_category(file_name):
	img_name=file_name
	curr_path=os.path.abspath('.')
	
	num_to_category=['airplane',
					 'ant',
					 'butterfly',
					 'chair',
					 'crab',
					 'cup',
					 'garfield',
					 'lamp',
					 'pizza',
					 'rooster',
					 'wild',
					 'yin']

	img=Image.open(os.path.join(curr_path,img_name))
	new_img=img.resize((256,256),Image.BILINEAR)
	arr=np.asarray(new_img,dtype="float32")

	arr.resize((1,256,256,3))
	arr=arr/255.0
	with graph.as_default():
		result=model.predict(arr)

	return num_to_category[int(result.argmax(axis=1))]