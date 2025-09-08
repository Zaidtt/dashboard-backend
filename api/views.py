from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.views import View
from .models import Dataset, Upload
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from django.shortcuts import render
from django.views import View

# Vista principal para renderizar el dashboard
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")

# API para obtener los datos

def data_api(request):
    try:
        latest_dataset = Dataset.objects.latest("id")
        df = pd.DataFrame(latest_dataset.data)
        response = {
            "data": df.to_dict(orient="records"),
            "nulls": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum()
        }
        return JsonResponse(response)
    except Dataset.DoesNotExist:
        # Devuelve estructura vacía para que PyScript no rompa
        return JsonResponse({"data": [], "nulls": {}, "duplicates": 0})


# API para subir CSV
@csrf_exempt
def upload_api(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        df = pd.read_csv(file)
        Dataset.objects.create(name=file.name, data=df.to_dict(orient="records"))
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "No file uploaded"}, status=400)