from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .forms import UserForm
import moviepy.editor
import textwrap
from fpdf import FPDF


def home(request):
    param = {'Name': "TestNotes"}
    return render(request, 'home.html', param)


def login1(request):
    return render(request, 'login1.html')


def conversion(request):
    return render(request, 'conversion.html')


def register1(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # confpassword = request.POST['confPassword']
        # if password == confpassword:
        password = make_password(password)

        a = User(first_name=name, username=username,
                 email=email, password=password)

        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('login1')

    forms = UserForm()
    context = {
        'forms': forms
    }
    return render(request, 'register1.html', context)
    # return render(request, 'register1.html')

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

def edit(request):
    param = {
    "text" : ""
    }
    return render(request, 'edit.html', param)
