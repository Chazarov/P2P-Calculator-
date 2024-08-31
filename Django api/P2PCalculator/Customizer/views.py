import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest

from .processing import refresh_koefs, get_current_coefs


def index(request):

    context = get_current_coefs()

    return render(request, 'Customizer/index.html', context)



def submit_parametrs(request:WSGIRequest):

    if request.method == 'POST':
        try:

            result = refresh_koefs(request)

            if(result == None): 
                print("Incorrect request body")
                return JsonResponse({'status': 'error', 'message': 'Incorrect request body'}, status=400)
            elif(result == "Invalid password"):
                print("Invalid password")
                return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=400)
            elif(result == "Value error"):
                print("Value error")
                return JsonResponse({'status': 'error', 'message': 'Value error'}, status=400)
            elif(result == "Success"):
                return JsonResponse({'status': 'Success', 'message': 'Success'}, status=200)
        
        except json.JSONDecodeError:
            print("Invalid JSON")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    print("Invalid request method")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)