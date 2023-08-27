from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Note
from django.utils import timezone
from django.db import connection
import json


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


@login_required
def delete(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        note_id = post_data.get('note_id')

        if note_id is not None:
            # A01:2021 – Broken Access Control
            # Access control enforces policy such that users cannot act outside of their intended permissions.
            # Logged in users can delete each others notes if they know the note id
            # A simple fix is to add the following line:
            # if request.user == note.user:

            # A03:2021 – Injection
            # This is unsafe and gives in the possibility for an injection attack
            # should be using the following instead:
            # note = get_object_or_404(Note, pk=note_id)
            # note.delete()
            with connection.cursor() as cursor:
                query = "DELETE FROM brokensite_note WHERE id=" + str(note_id) + ""
                cursor.executescript(query)

    notes = Note.objects.filter(user=request.user).order_by('-date_published')
    context = {"notes": notes, "error": ""}
    return render(request, "brokensite/index.html", context)


def search(request):
    keyword = request.GET.get('textToSearch', None)

    if keyword is not None:
        notes = Note.objects.filter(note_text__contains=keyword, user_id=request.user.id)
        context = {"notes": notes}
    else:
        context = {"notes": None}

    return render(request, "brokensite/search.html", context)
