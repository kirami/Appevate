#!/usr/bin/env python
# Jacob Salmela
# 2016-06-02
# Writes text to a PDF at coordinates.  Use for quickly filling out forms that you use regularly.
# This takes some manual setup, but saves a ton of time once done

# http://stackoverflow.com/a/17538003
# Make sure to install the two utilities below first
# sudo easy_install pyPdf
# sudo easy_install reportlab

######## IMPORTS #########
import sys
import os
import StringIO
import time
from pyPdf import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import json, logging


####### VARIABLES ########

# Information for the form
# Varibles and their names can be changed to anything depending on the form being filled out
# Date of service and date needed by can be a second argument since the rest of the information will stay pretty much the same
#entry_name = sys.argv[1]


def getData():
    data = {}

    with open('C:\Users\kiraj\Downloads\\bInfo_.json') as json_file:
        data = json.load(json_file)
    """
    data["business_name"] = "Test Business"
    data["dba"]="DBA"
    data["b_add"]= "B address"
    data["b_add3"]= "City State Zip"
    data["b_contact"]= "Contact name"
    data["b_phone"]= "Phone"
    data["b_email"]= "B Email"
    data["o_name"]= "John Doe"
    data["SSID"]= "123456789"
    data["o_add"]= "O Add"
    data["o_add3"]="O City state zip"
    data["o_phone"]= "1336667777"
    data["FID"]= "957595-2-2982"
    #data["dob"]= "2-2-20"

    data["routing"]= "48948985"
    data["account"]= "88505272"
    """

    return data

####### FUNCTIONS ########
def main(data):


    #get Info
    logging.basicConfig(level=logging.DEBUG)
    logging.info("What type? Cash Discount=1, Reg=2, Clover=3")  # same as print
   
    deal_type = raw_input()
    

    packet = StringIO.StringIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    # width / height
    can.drawString(40, 485, data["dba_name"])
    can.drawString(40, 460, data["street"] + " " + data["street2"])
    can.drawString(40, 435, data["city"] + ", " + data["state"] + " " + data["zip"])
    can.drawString(40, 410, data["owner_name"])
    can.drawString(220, 410, data["business_phone"])
 
    can.drawString(310, 485, data["business_name"])
    can.drawString(310, 385, data["owner_email"])
    can.drawString(155, 330, data["business_name"])
    can.drawString(430, 330, data["FID"])

    """
    if data["business_type"]=="Corporation":
        can.drawString(280, 295, "x")
    if data["business_type"]=="LLC":
        can.drawString(65, 105, "x")
    """

    can.drawString(40, 230, data["owner_name"])
    can.drawString(40, 205, data["owner_SSID"])
    can.drawString(40, 180, data["owner_street"] + " " + data["owner_street2"])
    can.drawString(40, 155, data["owner_city"] + ", " + data["owner_state"] + " " + data["owner_zip"])

    can.drawString(210, 205, data["owner_phone"])
    can.drawString(250, 155, data["dob"])


    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # Read the existing PDF (the first argument passed to this script)
    #existing_pdf = PdfFileReader(file(filename + file_extension, "rb"))
    if deal_type == "2":
        existing_pdf = PdfFileReader(file("C:\Users\kiraj\Downloads\PS-Scripts\org.pdf", "rb"))
    else:
        existing_pdf = PdfFileReader(file("C:\Users\kiraj\Downloads\PS-Scripts\orgCD.pdf", "rb"))
    

    output = PdfFileWriter()

    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    ####
    #  Page 2
    ####
    packet = StringIO.StringIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    # width / height
    if data.get("bank_routing",None):
        can.drawString(45, 207, data["bank_routing"])
        can.drawString(315, 207, data["bank_ac"])
    else:
        can.drawString(315, 207, "")

    
    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    new_pdf = PdfFileReader(packet)

    page = existing_pdf.getPage(1)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    ####
    #  Page 3
    ####

    packet = StringIO.StringIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    # width / height
    can.drawString(45, 440, data["owner_name"])
    can.drawString(175, 125, data["business_name"])
    can.drawString(40, 60, data["owner_name"])

    
    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)


    page = existing_pdf.getPage(2)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    ####
    #  Page 4
    ####

    packet = StringIO.StringIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    # width / height

    can.drawString(195, 307, data["business_name"])
    can.drawString(65, 105, data["owner_name"])

    
   

    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)


    page = existing_pdf.getPage(4)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)


    ####
    #  Page 5
    ####

    packet = StringIO.StringIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(30, 695, data["dba_name"])
    can.drawString(315, 695, data["owner_email"])
    can.drawString(30, 128, data["dba_name"])
    can.drawString(270, 128, data["business_phone"])
    can.drawString(30, 105, data["street"] + " " +data["street2"])
    can.drawString(30, 80, data["city"] )
    can.drawString(260, 80, data["state"]) 
    can.drawString(310, 80, data["zip"])


    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    page = existing_pdf.getPage(5)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    #Only do for Clover (3)
    if deal_type=="3":

        existing_pdf = PdfFileReader(file("C:\Users\kiraj\Downloads\PS-Scripts\CSF-CD.pdf", "rb"))
        ####
        #  CSF
        ####

        packet = StringIO.StringIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)
        can.drawString(50, 645, data["dba_name"])
        can.drawString(370, 645, data["owner_email"])

        if sys.argv[1]=="full":
            can.drawString(285, 495, "1")
        if sys.argv[1]=="mobile":
            can.drawString(285, 240, "1")
        if sys.argv[1]=="mini":
            can.drawString(285, 285, "1")

        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

        ####
        #  CSF 2 & fill 3, 4, 5, 6
        ####

        page = existing_pdf.getPage(1)
        output.addPage(page)

        packet = StringIO.StringIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)
        can.drawString(40, 388, data["dba_name"])
        can.drawString(370, 388, data["business_phone"])
        can.drawString(470, 388, data["owner_name"])
        can.drawString(40, 368, data["street"])
        can.drawString(365, 368, data["street2"])
        can.drawString(40, 345, data["city"])
        can.drawString(365, 345, data["state"])
        can.drawString(470, 345, data["zip"] )
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        page = existing_pdf.getPage(2)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

        i = [3,4,5]
        for num in i:
            page = existing_pdf.getPage(num)
            output.addPage(page)
    
        ###############
        #
        # Trans Armer Clover
        ###

        existing_pdf = PdfFileReader(file("C:\Users\kiraj\Downloads\PS-Scripts\CloverTransArmorForm2.pdf", "rb"))

        packet = StringIO.StringIO()
        # Create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)
        if data["street2"]:
            street = data["street"] + " " + data["street2"]
        else:
            street = data["street"]
        can.drawString(350, 675, street + ", " + data["city"] + ", " + data["state"] + "  " + data["zip"])
        can.drawString(380, 652, data["owner_email"])
        can.drawString(380, 640, data["dba_name"])
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

        #fill all but last
        i = [1,2,3,4,5,6,7,8,9]
        for num in i:
            #logging.info("page: %s" % num)
            page = existing_pdf.getPage(num)
            output.addPage(page)

        ##### TransArmer last page
        packet = StringIO.StringIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 10)
        #can.drawString(95, 485, data["owner_name"])
        can.drawString(95, 465, "Owner")
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        page = existing_pdf.getPage(10)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)


        
        

    ##############################

    # Finally, write "output" to a real file
    outputStream = file("C:\Users\kiraj\Downloads\EPI-MPA " +data["dba_name"]+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()


######### SCRIPT #########
if __name__ == "__main__":
    data = getData()
    main(data)
    try:
        sys.stdout.close()
    except:
        pass
    try:
        sys.stderr.close()
    except:
        pass