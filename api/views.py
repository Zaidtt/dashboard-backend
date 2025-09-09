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
    import json
    try:
        latest_dataset = Dataset.objects.latest("id")
        df = pd.DataFrame(latest_dataset.data)
        data = json.loads(df.to_json(orient="records"))
        nulls = {k: int(v) for k, v in df.isnull().sum().to_dict().items()}
        duplicates = int(df.duplicated().sum())
        response = {
            "data": data,
            "nulls": nulls,
            "duplicates": duplicates
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
        import json
        data = json.loads(df.to_json(orient="records"))
        Dataset.objects.create(name=file.name, data=data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "No file uploaded"}, status=400)