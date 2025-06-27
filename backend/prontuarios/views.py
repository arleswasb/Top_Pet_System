print("Importing prontuarios/views.py")
# prontuarios/views.py

from django.http import HttpResponse


def simple_view(request):
    return HttpResponse("Hello from prontuarios")

print("Finished importing prontuarios/views.py")