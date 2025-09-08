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
    datasets = Dataset.objects.all().order_by('-id')
    if datasets.exists():
        dataset = datasets.first()
        return JsonResponse({
            "data": dataset.data,
            "duplicates": pd.DataFrame(dataset.data).duplicated().sum(),
            "nulls": pd.DataFrame(dataset.data).isnull().sum().to_dict()
        })
    return JsonResponse({"error": "No data"})

# API para subir CSV
def upload_api(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        df = pd.read_csv(file)
        Dataset.objects.create(name=file.name, data=df.to_dict(orient="records"))
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "No file uploaded"}, status=400)