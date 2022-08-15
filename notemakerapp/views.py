from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
from .models import Collections
from uuid import uuid4
from deepgram import Deepgram
import asyncio, json
import re
from django.core.files.storage import default_storage
import os
import pdfkit   # Converts HTML to PDF
from htmldocx import HtmlToDocx # Converts HTML to DOCX

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

def edit(request,text=""):
    param = {"text" :text}
    return render(request,'edit.html',param)

def html_to_pdf(text, output, title=None, pageSize="A4"):
    options = {
        'title': title,
        'page-size': pageSize,
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8"
    }
    pdf = pdfkit.from_string(text, output, options=options)
    return pdf  # Returns True if pdf created successfully

def html_to_docx(text, output):
    parser = HtmlToDocx()
    docx = parser.parse_html_string(text)
    docx.save(output)

global saveFileName
def downloadNote(request, html, type, pageSize, output):
    if(type == "pdf"):
        html_to_pdf(html, f'{output}', "Title", pageSize)
    else:
        html_to_docx(html, f'{output}')
    os.remove(saveFileName)

def editor(request,**params):
    if(request.method == "POST"):
        html = request.POST['text'];
        type = request.POST['fileType'];
        pageSize = request.POST['pageSize'];
        output = os.path.join('', 'media/') + type + '/' + request.POST['file_name'] + '.' + ("pdf" if type == "pdf" else "docx");
        # If user is authenticated, save note for collections in DB
        try:
            username = request.POST['username']
            title = request.POST['title']
            desc = request.POST['desc']
            note = Collections(username=username,title=title,desc=desc)
            note.save()
        except Exception as e:
            print("Error Found: ", e)

        downloadNote(request, html, type, pageSize, output)
        os.remove(output)
    if len(params) == 0:
        return render(request,'edit.html')
    else:
        return render(request,'edit.html',params)

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
        return render(request, 'edit.html', {'text': text})
    else:
        return render(request,'conversion.html')

def collections(request):
    return render(request,'collections.html')
