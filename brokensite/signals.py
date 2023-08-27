from django.contrib.auth.models import User
from brokensite.models import SecurityQuestion


def create_required_objects(sender, **kwargs):
    if not User.objects.filter(username="hannu").exists():
        user = User.objects.create_user("hannu", None, "hannu")
        q = SecurityQuestion.objects.create(question="What color is a red car?", answer="red", user_id=user.id)
        q.save()

    if not User.objects.filter(username="nea").exists():
        user = User.objects.create_user("nea", None, "nea")
        q = SecurityQuestion.objects.create(question="What is the meaning of life?", answer="4", user_id=user.id)
        q.save()
