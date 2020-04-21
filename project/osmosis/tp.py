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

import json


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
    packet = StringIO.StringIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    # width / height
    if sys.argv[1] == "full":
        can.drawString(40, 580, "1 Clover Station, 1 P500 Printer, 1 Clover Cash Drawer, 1 Clover Barcode Scanner")
    
    if sys.argv[1] == "mini":
        can.drawString(40, 580, "1 Clover Station, 1 Clover Charger")
    
    if sys.argv[1] == "mobile":
        can.drawString(40, 580, "1 Clover Station, 1 Clover charger")
    

    can.drawString(109, 495, data["street"] + " " + data["street2"] )
    can.drawString(280, 495, data["city"] )
    can.drawString(430, 495, data["state"])
    can.drawString(510, 495, data["zip"])
   
    
    
    if sys.argv[1] == "full":
        can.drawString(445, 355, "$129.00")
    if sys.argv[1] == "mini":
        can.drawString(445, 355, "$119.00")
    if sys.argv[1] == "mobile":
        can.drawString(445, 355, "$99.00")


    can.drawString(85, 160, data["owner_name"])


    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # Read the existing PDF (the first argument passed to this script)
    #existing_pdf = PdfFileReader(file(filename + file_extension, "rb"))
    existing_pdf = PdfFileReader(file("C:\Users\kiraj\Downloads\PS-Scripts\Commercial D&A.pdf", "rb"))
    
    output = PdfFileWriter()

    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)


    ##############################

    # Finally, write "output" to a real file
    outputStream = file("C:\Users\kiraj\Downloads\D&A  " +data["business_name"]+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()


    ##########################Invoice

    packet = StringIO.StringIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    # width / height
    can.setFont("Helvetica", 8)
    import datetime

    x = datetime.date.today()
    can.drawString(425, 620, str(x))
    can.drawString(335, 565, data["business_name"] + " DBA: " + data["dba_name"])
    can.drawString(335, 550, data["street"] + " " + data["street2"] )
    can.drawString(335, 535, data["city"] +", " + data["state"] +" " + data["zip"] )
    can.drawString(335, 520, data["owner_name"])
   
    if sys.argv[1] == "full":
        can.drawString(135, 410, "Clover Station")
        can.drawString(135, 395, "P500 Printer")
        can.drawString(135, 380, "Clover Cash Drawer")
        can.drawString(135, 365, "Clover Barcode Scanner")
        can.drawString(105, 380, "1")
        can.drawString(105, 365, "1")
    if sys.argv[1] == "mini" or sys.argv[1] == "mobile":
        can.drawString(135, 410, "Clover Station")
        can.drawString(135, 395, "Clover charger")
    
    if sys.argv[1] == "full":
        can.drawString(235, 235, "$129.00")
    if sys.argv[1] == "mini":
        can.drawString(235, 235, "$119.00")
    if sys.argv[1] == "mobile":
        can.drawString(235, 235, "$99.00")


    can.drawString(390, 230, "$" +sys.argv[2])


    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # Read the existing PDF (the first argument passed to this script)
    #existing_pdf = PdfFileReader(file(filename + file_extension, "rb"))
    existing_pdf = PdfFileReader(file("C:\Users\kiraj\Downloads\PS-Scripts\invoice.pdf", "rb"))
    
    output = PdfFileWriter()

    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)


    ##############################

    # Finally, write "output" to a real file
    outputStream = file("C:\Users\kiraj\Downloads\Invoice  " +data["business_name"]+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()


######### SCRIPT #########
if __name__ == "__main__":
    data = getData()
    main(data)