from datetime import datetime as dt
import os
from io import BytesIO
from itertools import zip_longest

import pandas as pd

from .create_table_fpdf2 import PDF
from supply_chain.settings import MEDIA_ROOT
from django.core.files.base import ContentFile
from .models import SalesQuoteLogs

def make_sales_quote(supply, retail_price, vmi_price, vfl):

    qrx = vfl['facility_name'][vfl['bu'] == 'QRX']

    date_of_supply = supply.loc[0,'created_date'].strftime("%d.%B.%Y") 
    valid_to_date = supply.loc[0, 'valid_to_date'].strftime("%d.%B.%Y") 


    dn_id = {}
    unique_dns = supply.drop_duplicates(subset="deliveryId")
    for i in unique_dns['deliveryId']:
        fa = supply['shipToName'][supply['deliveryId'] == i]
        dn_id[i] = fa.tolist()[0]


    supply.drop(columns=['shipToName', 'id', 'valid_to_date', 'created_date'])



    price_list = []
    try:
        for i in zip(supply['deliveryId'], supply['product_id'], supply['qty']):
            if qrx[qrx == dn_id[i[0]]].any():
                p = float(retail_price['price'][retail_price['product_id']==i[1]].values[0])
            else:
                p = float(vmi_price['price'][vmi_price['product_id']==i[1]].values[0])
            price_list.append((p, round(i[2]*p, 2)))
    except IndexError:
        raise IndexError(f"There is no Price for {i[1]}, for Facility: {dn_id[i[0]]}")
        

    supply['Price'] = [x[0] for x in price_list]
    supply['Total Amount'] = [x[1] for x in price_list]


    all_dns = [x for x in dn_id.keys()]
    dicts = {}
    for i in all_dns:
        dicts[i] = supply[supply['deliveryId'] == i]

    # def grouper(iterable, n, fillvalue=None):
    #     "Collect data into fixed-length chunks or blocks"
    #     args = [iter(iterable)] * n
    #     return zip_longest(*args, fillvalue=fillvalue)

    # os.chdir("C:\\Users\\mpharma\\Downloads")

    def split_dataframe(df,chunksize=14):
        chunks = []

        num_chunks = len(df) //chunksize +1
        for i in range(num_chunks):
            chunks.append(df[i*chunksize:(i+1)*chunksize])
        return chunks

    header = os.path.join(MEDIA_ROOT, 'SALES QUOTE HEADER.PNG')
    footer = os.path.join(MEDIA_ROOT, 'FOOTER.PNG')
    font = os.path.join(MEDIA_ROOT, 'calibri.ttf')
    #Loop through datasets

    for  dn in dn_id.keys():
        facility = dn_id[dn]
        print(f'Sales Quote for {facility} \n with DN ID {dn} is being generated')

        total_amount = round(sum(supply['Total Amount'][supply['deliveryId']==f'{dn}']),2)
        add = 1
        groups = split_dataframe(dicts[dn])
        # items = [x for x in grouper([x for x in range(1,len(dicts[dn])+1)], 12) if x != None]
        count = 1
        for df in groups:
            if df.empty != True:
                new_dict = {}
                
                for index, row in df.iterrows():
                    row.drop('deliveryId', inplace=True)
                    row['Item'] = count
                    row = row[['Item','product_id', 'product', 'qty', 'Price', 'Total Amount']]
                    row.index
                    count += 1
                    for key,value in zip(row.index.tolist(), row.tolist()):
                        if key not in new_dict.keys():
                            new_dict[key] = [f'{value}']
                        else:
                            new_dict[key].append(f'{value}')
            if add == 1:
                class MyPDF(PDF):
                    def header(self):
                        self.image(header,
                        x=0, y=5,  type='PNG', w=210, h=1288/40)
                        pdf.add_font('Calibri','', font, uni=True)
                        pdf.set_font('Calibri', size=13)
                        pdf.cell(w=0, h=70, txt=f"{facility}")
                        pdf.set_y(50)
                        pdf.cell(120)
                        pdf.multi_cell(w=0, h=7, markdown=True,
                        txt=f"Delivery Note ID: {dn}\nValid To: {valid_to_date}\nRequest Date: {date_of_supply}", 
                        border=0,ln=0, max_line_height=10)
                    
                    def footer(self):
                        self.set_y(-15)
                        self.image(footer,
                        x=0, y=265, type='PNG', w=150, h=30)
                        self.set_font('Helvetica', 'B', 12)
                        self.set_x(180)
                        self.cell(w=25, h=10, txt= 'Page ' + str(self.page_no()) + 
                        '/{nb}', border=1, ln=0, align='C')
                        
                pdf = MyPDF('P', 'mm', 'A4')
                pdf.add_page()
                pdf.alias_nb_pages()
                pdf.set_font('Calibri', size=13)

            pdf.create_table(table_data = new_dict,
                title='Dear Sir or Madam, \nThank you for your interest. We offer the following items:', 
                cell_width=[15,26,70,22,22,22], data_size=11, align_data='L',
                emphasize_data=[1], emphasize_style='BIU',emphasize_color=(255,0,0))

            if len(groups) > 1 and add < len(groups):
                pdf.add_page()
        
            elif len(groups) >1 and  add == len(groups):
                pdf.cell(90)
                pdf.cell(w=50,h=10 ,txt=f"Total Amount:     GHS {total_amount}",
                            ln=2)

            if len(groups) ==1:
                pdf.cell(90)
                pdf.cell(w=50, h=10, txt=f"Total Amount:     GHS {total_amount}",
                            ln=2)
            

            pdf_h = 297
            pdf_w = 210
            add += 1
        bytes = pdf.output()

        if not SalesQuoteLogs.objects.filter(deliveryId__iexact=dn).exists():
            object = SalesQuoteLogs.objects.create(
                    deliveryId=dn,
                    created_date = dt.strptime(date_of_supply, "%d.%B.%Y"),
                    shipFromName = 'Accra',
                    shipToName = facility,
                    )

            object.salesquote.save(f'{facility} SQ {dn}.pdf', ContentFile(BytesIO(bytes).read()))
