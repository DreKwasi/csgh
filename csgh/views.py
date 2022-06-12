from django.shortcuts import render, redirect, HttpResponse
from .models import *
import pandas as pd
from datetime import datetime as dt
from .salesquote_maker import make_sales_quote
from django.views.generic import ListView
from django.db.models import Q
import io
import zipfile
import os
from django.conf import settings

model_dict = {
    'Supply Data':SupplyData,
    'Retail Price':RetailPrice,
    'Wholesale Price':WHPrice,
    'VFL':FacilityList,
}



def create_objs(request, model, df):
    if model == "Supply Data":
        supply = df
        date_of_supply = supply.iloc[0,-1]
        valid_to_date = f"{int(date_of_supply[0:2]) + 2}{date_of_supply[2:]}"


        supply.drop(columns=supply.columns.tolist()[-1], inplace=True)

        supply.fillna(method='ffill', inplace=True)

        supply = supply[supply['Ship-to Location'] != 'Not assigned']

        dn_id = {}
        check = []
        for i in supply['Delivery ID']:
            if i not in check:
                fa = supply['Ship-to Location'][supply['Delivery ID'] == i]
            dn_id[i] = fa.tolist()[0]
            check.append(i)

        # supply.drop(columns='Ship-to Location', inplace=True)
        supply = supply.copy()
        supply.rename(columns={'Delivery ID':'DN ID', 
        'Product': 'Drug ID', 'Unnamed: 3':'Drug Name',
        'Delivered Quantity':'Quantity'}, inplace=True)


        supply.loc[:,'Quantity'] = [int(x[:-5]) for x in supply['Quantity']]
        # import pdb
        # pdb.set_trace()
        objs = [
            SupplyData(
                deliveryId = row[1]['DN ID'],
                shipToName = row[1]['Ship-to Location'],
                shipFromName = row[1]['Ship-from Location'],
                product_id = row[1]['Drug ID'],
                product = row[1]['Drug Name'],
                qty = row[1]['Quantity'],
                valid_to_date = dt.strptime(valid_to_date, "%d.%m.%Y"),
                created_date = dt.strptime(date_of_supply, "%d.%m.%Y")

            ) for row in supply.iterrows()
        ]
        return {'objs':objs,'Supply Data':SupplyData}
    
    elif model == 'Retail Price':
        objs = [
            RetailPrice(
                product_id = row[1]['PRODUCT ID'],
                product = row[1]['DRUG NAME'],
                price = row[1]['PACK PRICE']

            ) for row in df.iterrows()
        ]
        return {'objs':objs,'Retail Price':RetailPrice}
    
    elif model == 'Wholesale Price':
        objs = [
            RetailPrice(
                product_id = row[1]['PRODUCT ID'],
                product = row[1]['DRUG NAME'],
                price = row[1]['PACK PRICE']

            ) for row in df.iterrows()
        ]
        return {'objs':objs,'Wholesale Price':WHPrice}
    
    elif model == "VFL":
        objs = [
            FacilityList(
                facility_name = row[1]['NAME'],
                bu = row[1]['BU']

            ) for row in df.iterrows()
        ]
        return {'objs':objs,'VFL':FacilityList}


def home(request):
    return render(request, 'csgh/home.html')


def delnote(request):
    return render(request,'csgh/delnote.html')


def salesquote(request):
    items = request.POST.items()
    # import pdb
    # pdb.set_trace()
    if len(request.POST.keys()) == 1:
        supply = pd.DataFrame.from_records(SupplyData.objects.all().values())
        retail_price = pd.DataFrame.from_records(RetailPrice.objects.all().values())
        wh_price = pd.DataFrame.from_records(WHPrice.objects.all().values())
        facility = pd.DataFrame.from_records(FacilityList.objects.all().values())
    
        make_sales_quote(supply=supply, retail_price=retail_price, vmi_price=wh_price, vfl=facility)
    
    else:
        ids = []
        for key, value in request.POST.items():
            if value == "on":
                ids.append(key)
        
        zip_subdir = "Sales Quotes"
        zip_filename = zip_subdir + ".zip"
        byte_stream = io.BytesIO()

        zf = zipfile.ZipFile(byte_stream, "w")


        for i in ids:
            obj = SalesQuoteLogs.objects.get(deliveryId__iexact=i)
            filename = os.path.join(settings.MEDIA_ROOT, obj.salesquote.name)
            fdir, fname = os.path.split(filename)
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(filename, zip_path, compresslevel=9)    

            # close the zip folder and return
        zf.close()
        response = HttpResponse(byte_stream.getvalue(), content_type = "application/x-zip-compressed")
        response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return response  


    return redirect('salesquote')

class SalesQuoteListView(ListView):
    template_name = "csgh/salesquote.html"
    context_object_name = "quotes"
    
    def get_queryset(self):
        q = self.request.GET.get("q") if self.request.GET.get("q") != None else ''
        date = self.request.GET.get("date") if self.request.GET.get("date") != None else ''
        q_filter = SalesQuoteLogs.objects.filter(Q(shipToName__icontains=q)|
                                            Q(shipFromName__icontains=q)|
                                            Q(deliveryId__icontains=q))
        if date != '':
            q_filter = DocumentLogs.objects.filter(Q(shipToName__icontains=q)|
                                            Q(shipFromName__icontains=q)|
                                            Q(deliveryId__icontains=q)).filter(created_date=date)
        quotes = q_filter
        return quotes

    
    def post(self, request, *args, **kwargs):
        return salesquote(request)


def uploadfile(request, pk):
    context = {'pk':pk}
    if request.method == 'POST':
        file = request.FILES['upload_file']
        if pk == "supply_data":
            df = pd.read_csv(file, encoding='utf-8', dtype={'Delivery ID': str})
        else:
            df = pd.read_csv(file)
        
        dicts = create_objs(model=pk, df=df, request=request)
        if not model_dict[pk].objects:
            model_dict[pk].objects.all().delete()
            
        model_dict[pk].objects.bulk_create(dicts['objs'])
        return redirect('salesquote')


    return render(request, 'csgh/upload.html', context)
