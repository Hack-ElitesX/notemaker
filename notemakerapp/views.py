from lib2to3.pgen2 import token
from typing import final
from urllib import response
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage

from uuid import uuid4
import moviepy.editor
import textwrap
from fpdf import FPDF
from deepgram import Deepgram
import asyncio, json
import re
from django.core.files.storage import default_storage
import os

# Create your views here.
def home(request):
    param = {'Name': "TestNotes"}
    return render(request, 'home.html', param)
        
def handleSignup(request):
    if request.method == 'POST':
        # get the post parameters
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        
        # Checks for errorneous inputs
        #
        if len(username) > 15:
            messages.error(request,"Username must be under 15 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request,"Username only contains alpha-numeric characters")
            return redirect('home')
        
        if password1 != password2 :
            messages.error(request,"Passwords do not match")
            return redirect('home')
            
            
        # Create the user
        my_user = User.objects.create_user(username=username,email=email,password=password1)
        my_user.first_name = name
        my_user.save()
        messages.success(request,"Your Account has been created Successfully !")

        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
    
def handleLogin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        passwd = request.POST['pass']
        
        user = authenticate(username=uname,password=passwd)
        
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In !")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials, Please Try again !")
            return redirect('home')
        
    else:
        return HttpResponse('404 - Not Found')

def handleLogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request,"Successfully Logged Out !")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def convert(request):
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        token_var = uuid4()
        saveFileName = str(token_var) + '_' + str(uploaded_file.name)
        fs.save(saveFileName, uploaded_file)
        
        text = audio_to_text(saveFileName)
        if(text == None):
            return HttpResponse('''
            <h1> Invalid File Format </h1>
            <p> <b> Supported File Formats </b> </p>
            <h3> Video </h3>
            <ul>
                <li> MP4 </li>
                <li> MKV </li>
            </ul>
            <br>
            <h3> Audio </h3>
            <ul>
                <li> MP3 </li>
                <li> WAV </li>
            </ul>
            <a href="/conversion"> Go Back </a>
            ''')
        return edit(request, text)
    else:
        return render(request,'conversion.html')


def editor(request,**params):
    print("Length of parameters : "+ str(len(params)))
    if len(params) == 0:
        return render(request,'edit.html')
    else:
        return render(request,'edit.html',params)

def collections(request):
    return render(request,'collections.html')

# Extract Audio From Video
# Note: Also give extension for the output file like output.wav or output.mp3 then the file will be converted in that format
def extract_audio_from_video(path, output):
    video = moviepy.editor.VideoFileClip(path)
    audio = video.audio
    audio.write_audiofile(output)


# Convert Text to PDF
def text_to_pdf(text, filename, format='A4', margin_bottom=10, font_family='Arial', fontsize_pt=12, orientation='P', unit='mm'):
    '''
text_to_pdf arguments:
    text: The text that is to be converted to PDF (Required)
    filename: Filename to save pdf as (Required)
    format: The format in which to save file -> Default: A4
        Supported Format: A3, A4, A4-wide, A5, B4, B4-wide, B5, letter, letter-wide, legal, legal-wide
    margin_bottom: The space to leave between the last line of text and the border of the page -> Default: 10
    font_family: Font Family to use -> Default: Arial
    fontsize_pt: Font Size to Use -> Default: 12
    orientation: Orientation of the pdf -> Default: P (Portrait)
    unit: Unit to measure fontsize in -> Default: mm
    '''
    width = {
        'A3': 297,
        'A4': 210,
        'A4-wide': 297,
        'A5': 148,
        'B4': 257,
        'B4-wide': 364,
        'B5': '182',
        'letter': 215.9,
        'letter-wide': 279.4,
        'legal': '215.9',
        'legal-wide': 355.6
    }
    width_mm = width[format]
    pt_to_mm = 0.45
    fontsize_mm = fontsize_pt * pt_to_mm
    character_width_mm = 7 * pt_to_mm
    width_text = width_mm / character_width_mm

    pdf = FPDF(orientation=orientation, unit=unit, format=format)
    pdf.set_auto_page_break(True, margin=margin_bottom)
    pdf.add_page()
    pdf.set_font(family=font_family, size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

DEEPGRAM_API_KEY = 'ce3960b83c89b1411d4fde4b9fd22905d1ee1900'
async def main(path):
    try:     
        # Initializes the Deepgram SDK
        deepgram = Deepgram(DEEPGRAM_API_KEY)

        f = default_storage.open(os.path.join('', path), 'rb')
        data = f.read()
        f.close()

        video_formats = ['mp4', 'mkv']
        audio_formats = ['mp3', 'wav']
        fileType = path.split('.')[1]
        mimetype = ""
        if(fileType in video_formats):
            mimetype += "video/" + fileType
        elif(fileType in audio_formats):
            mimetype += "audio/" + fileType
        else:
            return None;

        source = {'buffer': data, 'mimetype': 'audio/wav'}
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
    except Exception as e:
        return HttpResponse(e)

    res = json.dumps(response["results"]["channels"][0], indent=1)
    pattern = r"\"transcript\": \".+\""
    final_text = re.findall(pattern, res)
    final_text = " ".join(final_text)
    final_text += "<>"
    final_text = final_text.replace("\"transcript\": \"", '').replace("\"<>", '')
    return final_text

def audio_to_text(path):
    return asyncio.run(main(path))

def edit(request,text):
    param = {"text" :text}
    return render(request,'edit.html',param)