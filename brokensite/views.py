from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Note, RecoveryCode
from django.utils import timezone
from django.core.mail import send_mail
import json
from django.contrib.auth.models import User

import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@login_required
def index(request):
    error = ""

    if request.method == "POST":
        note_text = request.POST.get('note_text', None)
        if note_text is None or len(note_text.strip()) == 0:
            error = "Failed to add new note."
        else:
            note = Note(note_text=note_text, date_published=timezone.now(), user=request.user)
            note.save()

    notes = Note.objects.filter(user=request.user).order_by('-date_published')
    context = {"notes": notes, "error": error}
    return render(request, "brokensite/index.html", context)


# Flaw: csrf exempted
@login_required()
def delete(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        note_id = post_data.get('note_id')

        if note_id is not None:
            # A03:2021 – Injection
            note = get_object_or_404(Note, pk=note_id)
            note.delete()

    notes = Note.objects.filter(user=request.user).order_by('-date_published')
    context = {"notes": notes, "error": ""}
    return render(request, "brokensite/index.html", context)


# A01:2021 – Broken Access Control icon
@login_required()
def search(request):
    keyword = request.GET.get('keyword', None)
    userid = request.user.id

    if keyword is not None:
        notes = Note.objects.filter(note_text__contains=keyword, user_id=userid)
        context = {"notes": notes}
    else:
        context = {"notes": None}

    return render(request, "brokensite/search.html", context)


# A04:2021 – Insecure Design
def recover(request):
    if request.method == "GET":
        return render(request, "brokensite/recover.html")
    else:
        randomstring = get_random_string(20)
        user = User.objects.filter(email=request.POST.get('email', None)).first()
        RecoveryCode.objects.filter(user_id=user.id).delete()
        code = RecoveryCode(user_id=user.id, code=randomstring)
        code.save()

        """""
        send_mail(
            "Password recovery code",
            code.code,
            "admin@amazingnotes.com",
            [user.email],
            fail_silently=False,
        )
        """

        return render(request, "brokensite/recover.html", {"message": "Email sent!"})


def changepassword(request):
    try:
        if request.method == "GET":
            return render(request, "brokensite/changepassword.html")
        else:
            code = request.POST.get("code", None)
            newpassword = request.POST.get("newpassword")
            newpasswordagain = request.POST.get("newpasswordagain")
            user = User.objects.filter(email=request.POST.get('email', None)).first()

            recoverycode = RecoveryCode.objects.filter(user_id=user.id).first()

            if recoverycode.code != code or newpassword != newpasswordagain:
                return render(request, "brokensite/changepassword.html", {"message": "Password change failed."})

            recoverycode.delete()
            user.set_password(newpasswordagain)
            user.save()

            return render(request, "brokensite/changepassword.html", {"message": "Password updated!"})

    except:
        return render(request, "brokensite/changepassword.html", {"message": "Password change failed."})
