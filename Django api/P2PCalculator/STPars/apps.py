import asyncio
import threading

from django.apps import AppConfig
from STPars.tasks import refresh_data




THREADINGS = []



def starting_a_stream():

    thread1 = threading.Thread(target = process1)
    thread1.start()
    
    THREADINGS = []
    THREADINGS.append(thread1)

    print("\n>>>Start threads<<<\n")



def process1():
    asyncio.run(refresh_data())





class StparsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'STPars'



    def ready(self):
        print("> > > > > > > > Start app < < < < < < < < <")

        if(len(THREADINGS) == 0):
            starting_a_stream()
        

    