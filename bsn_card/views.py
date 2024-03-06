# from django.shortcuts import render
import os.path
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
import cv2
import pytesseract
import re
from django.contrib import messages
import xlsxwriter
from pathlib import Path
from datetime import datetime
from django.core.files.storage import FileSystemStorage


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'bsn_card/index.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'bus_card/post_detail.html', {'post': post})


@login_required
def home(request):
    forms = masterForm()
    if request.method == 'POST':

        form = masterForm(request.POST, request.FILES)
        # form = MasterForm1(request.POST, request.FILES)
        print("""129""")

        if form.is_valid():
            form.save()
            img= request.FILES['img'].name
            BASE_DIR = Path(__file__).resolve().parent.parent
            path_new = os.path.join(BASE_DIR, 'media')
            file_name = os.path.join('media', img)
            # import pdb;pdb.set_trace()
            # with open(file_name, 'wb') as f:
            #     for chunk in request.FILES['img'].chunks():
            #         f.write(chunk)

            # image_path = os.path.join(settings.MEDIA_ROOT, img)
            # storage = FileSystemStorage()
            # # img.save(path_new)
            # import pdb;
            # pdb.set_trace()
            first_record = master.objects.order_by('-created_at').first()
            #
            # print('jai maa...', first_record.img.name)
            # piccc = first_record.img.name
            # img = cv2.imread(os.path.join(MEDIA_ROOT,'media')
            #
            # BASE_DIR = Path(__file__).resolve().parent.parent
            # path_new = os.path.join(BASE_DIR, 'media')

            # path = r"D:\POC\ocr_project\ocr_app\media"
            # file_name = first_record.img.name
            # import pdb; pdb.set_trace()
            # img = cv2.imread(os.path.join(path_new, file_name))
            img = cv2.imread(os.path.join(path_new, img))
            # img = cv2.imread(first_record.img.url)

            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Configure OCR settings
            config = '-l jpn --oem 1 --psm 3'
            # Perform OCR using pytesseract
            text = pytesseract.image_to_string(gray_img, config=config)
            # Print the extracted text
            # print(text)
            email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
            # phone_numbers = re.findall(r"(?i)(?:TEL:|tel :|\+1|FAX :|FAX:)\s*([0-9-]+)", text)
            phone_numbers = re.findall(r'(\d{2}[-.\s]?\d{4}[-.\s]?\d{4})', text, re.IGNORECASE)
            fax_number = re.findall(r"FAX\s?:\s?([\d\s()-]+)", text, re.IGNORECASE)
            urls = re.findall(r"https?://[^\s]+", text, re.IGNORECASE)

            text_without_phone = re.sub(r'\+\d{1,3}\s?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', '', text)
            text_without_email = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '', text_without_phone)

            # Split text into lines
            lines = text.splitlines()

            # Initialize the final dictionary
            final_dic = {
                "name": "",
                "depart": "",
                "desi": "",
                "phone_no": "",
                "fax_no": "",
                "email_id": "",
                "url": "",
                "information": "",
                "cname": ""
            }

            # Extract information from the first three lines
            for i in range(min(3, len(lines))):
                line = re.split(r'(?<=[.!?])\s+', lines[i])
                if line:
                    if i == 0:
                        final_dic["name"] = str(line[0])
                    elif i == 1:
                        final_dic["desi"] = str(line[0])
                    elif i == 2:
                        final_dic["depart"] = str(line[0])

            # Extract phone numbers
            if fax_number:
                final_dic["fax_no"] = (', '.join(fax_number))

            if phone_numbers:
                final_dic["phone_no"] = (', '.join(phone_numbers))

            # Extract email addresses
            if email_addresses:
                final_dic["email_id"] = email_addresses[0]

            if urls:
                final_dic["url"] = urls[0]

            # Clean up extra whitespace
            cleaned_text = re.sub(r'\s+', ' ', text_without_email).strip()

            # Word to remove
            word_to_remove = final_dic["name"]
            word_2_remove = final_dic["depart"]
            word_3_remove = final_dic["desi"]

            # Remove the word from the sentence
            new_sentence = cleaned_text.replace(word_to_remove, "")
            new_sentence = new_sentence.replace(word_2_remove, "")
            new_sentence = new_sentence.replace(word_3_remove, "")

            # Store cleaned text in final dictionary
            final_dic['information'] = text
            import json
            json_data = json.dumps(final_dic)

            # data_2 = {'img': first_record,'form': form, 'data':final_dic}
            # final_dic['img'] = img
            # final_dic['form'] = form
            final_dic["img"] = first_record
            final_dic["cname"] = ''

            context = {
                "data": final_dic
            }

            print('206......', 'this is line 206', final_dic)
            # import pdb; pdb.set_trace()
            return render(request, 'bsn_card/index.html', context)  # ,'form': form

        print("211........", 'this is line number 211')
    return render(request, 'bsn_card/index.html', {'form': forms})


@login_required
def saving_card(request):
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        # if request.POST.get('img') :

        img = request.POST['img']
        com_name = request.POST['cname']
        name = request.POST['name']
        desi = request.POST['desi']
        dept = request.POST['dept']
        email_id = request.POST['email_id']
        url = request.POST['url']
        phone_no = request.POST['phone_no']
        # fax_no  = request.POST['fax_no']
        desc = request.POST['detail']
        user_id = request.user.id
        category = request.POST['category']
        comment = request.POST['comment']
        # import pdb;pdb.set_trace()
        # user =

        # import pdb; pdb.set_trace()  img_bsn=img,
        data = details(img_bsn=img, com_name=com_name, name=name, desi=desi, dept=dept, url=url, email_id=email_id,
                       phone_no=phone_no, desc=desc, user_id=user_id, category=category, comment=comment)

        if details.objects.filter(email_id=email_id).exists():
            message = "Data is aldy exits."
            context = {"message": message}
            print('lne no: 165, Data is aldy exits')
            messages.error(request, 'The data are already exists.')
            # return render(request,'/bsn_card/index.html')
            return redirect('/bsn_card')

        else:
            data.save()
            data_list = details.objects.all()
            message = "Data is successfully saved in database."
            context = {"message": message}
            messages.success(request, 'The data are successfully submitted.')

        return redirect('/bsn_card')
        # return render(request,'bsn_card/index.html')


    else:
        forms = masterForm()
        print('line no 182...jai shrre ganesh')
        return redirect('/bsn_card')


# @login_required
def bsn_card_table(request):

    if request.method == 'GET':
        forms = masterForm()
        # import pdb; pdb.set_trace()

        if request.user.is_superuser:
            data_list = details.objects.select_related('user').values('com_name', 'name', 'desi', 'dept', 'phone_no',
                                                                      'email_id', 'fax_no', 'url', 'created_at__date',
                                                                      'user_id',
                                                                      'user__first_name', 'img_bsn',
                                                                      'category','comment').order_by('-created_at__date')
        else:
            data_list = details.objects.select_related('user').values('com_name', 'name', 'desi', 'dept', 'phone_no',
                                                                      'email_id', 'fax_no', 'url', 'created_at__date',
                                                                      'user_id',
                                                                      'user__first_name', 'img_bsn', 'category','comment').filter(
                user_id=request.user.id).order_by('-created_at__date')

        print('page..........211', data_list)

        return render(request, 'bsn_card/full-screen-table.html', {'data_list': data_list,'form': forms})

    else:

        result=  home(request)
        return result



def generate_csv_report_1(request):
    # Get the data for the report
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        data = details.objects.select_related('user').values('name', 'desi', 'dept', 'phone_no', 'email_id', 'fax_no',
                                                             'url', 'created_at__date', 'user__username').filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)

        # Define table data and style
        table_data = [['name', 'desi', 'dept', 'phone_no', 'email_id', 'fax_no',
                       'url', 'created_at__date', 'user__username']]
        for item in data:
            table_data.append([item['name'], item['desi'], item['dept'], item['phone_no'],
                               item['email_id'], item['fax_no'], item['url'],
                               item['created_at__date'], item['user__username']])

        # Create the response object with appropriate content type and headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

        # Create an XLSX workbook and worksheet
        workbook = xlsxwriter.Workbook(response, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Set table formatting
        table_format = workbook.add_format({'border': 1, 'bold': True})

        # Set filter formatting
        filter_format = workbook.add_format({'bold': True, 'font_color': 'blue'})

        # Write the data to the XLSX worksheet
        for i, row in enumerate(table_data):
            for j, cell in enumerate(row):
                if i == 0:
                    # Write header cells with filter formatting
                    worksheet.write(i, j, cell, filter_format)
                else:
                    worksheet.write(i, j, cell)

        # Apply autofilter to the header row
        worksheet.autofilter(0, 0, 0, len(data[0]) - 1)

        # Set the column width for better readability
        worksheet.set_column(0, len(data[0]) - 1, 15)

        # Close the workbook
        workbook.close()
        return response


import pandas as pd
from django.http import HttpResponse
from datetime import datetime


def generate_csv_report(request):
    # Get the data for the report
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']

        data = details.objects.select_related('user').values('name', 'desi', 'dept', 'phone_no', 'email_id', 'fax_no',
                                                             'url', 'created_at__date', 'user__username').filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)

        # Create a pandas DataFrame
        df = pd.DataFrame.from_records(data)

        # Rename columns
        column_names = {
            'name': 'Name',
            'desi': 'Designation',
            'dept': 'Department',
            'phone_no': 'Phone Number',
            'email_id': 'Email ID',
            'fax_no': 'Fax Number',
            'url': 'URL',
            'created_at__date': 'Date',
            'user__username': 'Username'
        }
        df.rename(columns=column_names, inplace=True)

        response = HttpResponse(content_type='text/excel')
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"BusinessCard_{current_date}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        df.to_excel(response, index=False)
        return response
