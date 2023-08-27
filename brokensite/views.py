from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .models import Note, SecurityQuestion
from django.utils import timezone
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


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
# this enables an attack where attacker forces authenticated user to submit a request
# to this web application
@csrf_exempt
@login_required()
def delete(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        note_id = post_data.get('note_id')

        if note_id is not None:
            # A03:2021 – Injection
            # This is unsafe and gives in the possibility for an injection attack
            # should be using the following instead:
            # note = get_object_or_404(Note, pk=note_id)
            # note.delete()
            with connection.cursor() as cursor:
                query = "DELETE FROM brokensite_note WHERE user_id=" + str(request.user.id) + " AND id=" + str(note_id)
                cursor.executescript(query)

    notes = Note.objects.filter(user=request.user).order_by('-date_published')
    context = {"notes": notes, "error": ""}
    return render(request, "brokensite/index.html", context)


# A01:2021 – Broken Access Control icon
# @login_required missing, user id is retrieved from request
def search(request):
    keyword = request.GET.get('keyword', None)
    # should be request.user.id
    userid = request.GET.get('userid', None)

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
        try:
            username = request.POST.get('username')
            user = User.objects.filter(username=username).first()
            answer = request.POST.get('answer')
            newpassword = request.POST.get('password')

            question = SecurityQuestion.objects.filter(user_id=user.id).first()

            if question.answer != answer:
                raise Exception("Answers did not match")

            user.set_password(newpassword)
            question.answer = request.POST.get('newanswer')
            question.question = request.POST.get('newquestion')
            question.save()
            user.save()

            # Insecure design with the password being just text
            return render(request, "brokensite/recover.html", {"message": "Password recovered! New password is " + newpassword})
        except:
            return render(request, "brokensite/recover.html", {"message": "Password recovery failed."})

# A04:2021 – Insecure Design icon
def getquestion(request):
    try:
        username = request.GET.get('username', None)
        user = User.objects.filter(username=username).first()
        question = SecurityQuestion.objects.filter(user_id=user.id).first().question
        return JsonResponse({
            "question": question
        })
    except:
        return JsonResponse({})
