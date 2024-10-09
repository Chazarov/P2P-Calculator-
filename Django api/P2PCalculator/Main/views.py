from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
import json

from STPars.processing import processing_data





def index(request):
    return render(request, 'Main/index.html')

def calculator(request):
    return render(request, 'Main/calcIndex.html')


@csrf_exempt
def submit_parametrs(request:WSGIRequest):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_data = processing_data(params = data)

            if(response_data == None): 
                print("Incorrect request body")
                return JsonResponse({'status': 'error', 'message': 'Incorrect request body'}, status=400)
            else:
                return JsonResponse(response_data)
        
        except json.JSONDecodeError:
            print("Invalid JSON")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    print("Invalid request method")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


