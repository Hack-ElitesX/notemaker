from genericpath import exists
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
from django.core.files.storage import FileSystemStorage
from .models import Collection
import platform
from uuid import uuid4
from deepgram import Deepgram
import asyncio, json
import re
from django.core.files.storage import default_storage
import os
import pdfkit   # Converts HTML to PDF
from htmldocx import HtmlToDocx # Converts HTML to DOCX
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from . import yt_download

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
            messages.warning(request,"Username must be under 15 characters")
            return redirect('home')
        
        if not username.isalnum():
            messages.warning(request,"Username only contains alpha-numeric characters")
            return redirect('home')
        
        if password1 != password2 :
            messages.warning(request,"Passwords do not match")
            return redirect('home')
            
            
        # Create the user
        try:
            my_user = User.objects.create_user(username=username,email=email,password=password1)
            my_user.first_name = name
            my_user.save()
            messages.success(request,"Your Account has been created Successfully !")
        except:
            messages.error(request,f"Username {username} already Exists !")
        
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
    if(platform.system() == "Windows"):
        wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
        pdf = pdfkit.from_string(text, output, options=options, configuration=wkhtml_path)
    else:
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
    # os.remove(saveFileName)

def editor(request,**params):
    if(not os.path.exists('media/')):
        os.mkdir(os.path.join('', 'media'))
    if(not os.path.exists('media/pdf')):
        os.mkdir(os.path.join('', 'media') + '/pdf')
    if(not os.path.exists('media/word')):
        os.mkdir(os.path.join('', 'media') + '/word')
    if(request.method == "POST"):
        html = request.POST['text'];
        type = request.POST['fileType'];
        pageSize = request.POST['pageSize'];
        output = os.path.join('', 'media', type, request.POST['file_name']) + ('.' + ('pdf' if type=='pdf' else 'docx'));
        # New Code for testing
        try:
            username = request.POST['username']
            title = request.POST['title']
            desc = request.POST['desc']
            text = request.POST['plain_text']
            note = Collection(username=username,title=title,desc=desc, text=text)
            note.save()
        except Exception as e:
            print("Error Found: ", e)

    # return render(request,'collections.html')
        downloadNote(request, html, type, pageSize, output)
        # os.remove(output)
    if len(params) == 0:
        return render(request,'edit.html')
    else:
        return render(request,'edit.html',params)
    
DEEPGRAM_API_KEY = 'ce3960b83c89b1411d4fde4b9fd22905d1ee1900'
async def main(type, path, url, language):
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    if(type == 'file'):
        try:     
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
        except Exception as e:
            return HttpResponse(e)
    elif(type == 'url'):
        source = {'url': url}
    response = await deepgram.transcription.prerecorded(source, {'punctuate': True, 'language':language})

    res = json.dumps(response["results"]["channels"][0], indent=1)
    pattern = r"\"transcript\": \".+\""
    final_text = re.findall(pattern, res)
    final_text = " ".join(final_text)
    final_text += "<>"
    final_text = final_text.replace("\"transcript\": \"", '').replace("\"<>", '')
    return final_text

def audio_to_text(type, path=None, url=None, language="en"):
    return asyncio.run(main(type, path, url, language))

def to_hinglish(text):
    return(transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI))

def download_yt_video(url, filename, savePath):
    yt = yt_download.YouTube()
    yt.download(url, filename, savePath)

def convert(request):
    print("Conversion")
    if request.method == "POST":
        text = None
        fileFormat = request.POST['format']
        language = request.POST['lang']
        if(fileFormat == 'file'):
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            token_var = uuid4()
            saveFileName = str(token_var) + '_' + str(uploaded_file.name)
            fs.save(saveFileName, uploaded_file)
            text = audio_to_text('file', saveFileName, language=language)
            if(language == "hi-Latn"):
                text = to_hinglish(text)
            if(language == "en"):
                imp_words = {'important', 'note', 'fundamental', 'chief point', 'necessary', 'etcetera', 'essential', 'diagram'}
                more_words = {'major', 'crucial', 'vital', 'significant', 'leading edge', 'example', 'called', 'those are'}
                text = text.split('.')
                print(text)
                sen_offset = 0
                for sentence in text:
                    print(sentence)
                    for words in imp_words:
                        if(words.lower() in sentence.lower()):
                            print("Word:", words, "\tSentence:", sentence)
                            # text[sen_offset] = "<span style='background-color: rgb(240, 102, 102);'>" + text[sen_offset] + "</span>"
                            print("Before:" + text[sen_offset])
                            text[sen_offset] = " | " + text[sen_offset] + " _ "
                            print("After:" + text[sen_offset])
                            print("Word Found:", words)
                            print("\n\n")
                    for words in more_words:
                        if(words.lower() in sentence.lower()):
                            # text[sen_offset] = "<span style='background-color: #66b966;'>" + text[sen_offset] + "</span>"
                            print("Before:" + text[sen_offset])
                            text[sen_offset] = " || " + text[sen_offset] + " __ "
                            print("After:" + text[sen_offset])
                            print("Word Found:", words)
                    sen_offset += 1
                text = ' '.join(text)
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
        elif(fileFormat == 'url'):
            url = request.POST['url']
            if("youtu" in url):
                filename = url.split('/')[-1]
                download_yt_video(url, filename, os.path.join('', 'media'))
                print(os.path.join('', 'media') + '/' + filename + '.mp4')
                text = audio_to_text('file', filename + '.mp4', language=language)
                if(language == "hi-Latn"):
                    text = to_hinglish(text)
            else: 
                text = audio_to_text('url', url=url, language=language)
        try:
            return render(request, 'edit.html', {'text': text, 'total': sen_offset})
        except:
            return render(request, 'edit.html', {'text': text})
    else:
        return render(request,'conversion.html')

def collections(request):
    if(request.user == "AnonymousUser"):
        return HttpResponse('''
        <h2> User Unauntheticated </h2>
        <p> Kindly <a href="home.html"> Login </a> / <a href=""> Register </a> to access collections page </p>
        ''')
    collection = Collection.objects.filter(username=request.user)
    context = {'notes': collection}
    return render(request,'collections.html', context) 
