from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Note
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


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


@login_required()
def delete(request, note_id):

    if request.method == "DELETE":
        note = get_object_or_404(Note, pk=note_id)

        if request.user == note.user:
            note.delete()

    notes = Note.objects.filter(user=request.user).order_by('-date_published')
    context = {"notes": notes, "error": ""}
    return render(request, "brokensite/index.html", context)