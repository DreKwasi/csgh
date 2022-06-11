from django.shortcuts import render
from .models import *
import pandas as pd


def create_objs(request, pk, df):
    if pk == "supply_data":

        # objs = [
        #     SupplyData(
        #         deliveryID = request.user,
        #         product_id = row[1]['product_id'],
        #         product = row[1]['product'],
        #         qty = row[1]['qty']
        #     ) for row in df.iterrows()
        # ]
        return {'objs':objs,'stock':Stock}
    
    return None

def home(request):
    return render(request, 'csgh/home.html')


def delnote(request):
    return render(request,'csgh/delnote.html')


def salesquote(request):
    return render(request,'csgh/salesquote.html')

def uploadfile(request, pk):
    context = {'pk':pk}
    if request.METHOD == 'post':
        file = request.FILES['file']
        if pk == "supply_data":
            df = pd.read_csv(file, encoding='utf-8', dtype={'Delivery ID': str})
        else:
            df = pd.read_csv(file)

    return render(request, 'csgh/upload.html', context)
