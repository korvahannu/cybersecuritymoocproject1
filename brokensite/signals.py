from django.contrib.auth.models import User


def create_required_objects(sender, **kwargs):
    if not User.objects.filter(username="hannu").exists():
        User.objects.create_user("hannu", None, "hannu")

    if not User.objects.filter(username="nea").exists():
        User.objects.create_user("nea", None, "nea")
