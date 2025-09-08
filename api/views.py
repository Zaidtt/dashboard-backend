from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import pandas as pd
import json

# Create your views here.

def index(request):
    return render(request, "index.html")


class DataAPI(APIView):
    def get(self, request):
        # Consulta SQL obligatoria: extrae datos de la BD
        with connection.cursor() as cursor:
            cursor.execute("SELECT data FROM api_dataset WHERE name = 'current_dataset'")
            row = cursor.fetchone()
        if row:
            data = json.loads(row[0])
            df = pd.DataFrame(data)
            # Calcula métricas para gráficos (nulos, duplicados, etc.)
            nulls = df.isnull().sum().to_dict()
            duplicates = df.duplicated().sum()
            stats = df.describe().to_dict()
            return Response({
                'nulls': nulls,
                'duplicates': duplicates,
                'stats': stats,
                'data': data  # Datos crudos para gráficos detallados
            })
        return Response({'error': 'No data'})

class UploadAPI(APIView):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        data_json = df.to_json(orient='records')
        # Guarda en BD vía SQL
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM api_dataset WHERE name = 'current_dataset'")
            cursor.execute("INSERT INTO api_dataset (name, data) VALUES ('current_dataset', %s)", [data_json])
        return Response({'success': True})