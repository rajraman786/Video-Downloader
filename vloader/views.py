from django.shortcuts import render
from django.http import HttpResponse
import pafy
import requests
import os
import shutil
import pathlib
from django.http import FileResponse

def download(file_path):
  file_server = pathlib.Path(file_path)
  file_to_download = open(str(file_server), 'rb')
  response = FileResponse(file_to_download, content_type='application/force-download')
  response['Content-Disposition'] = f'inline; filename="{file_path}"'
  return response

def index(request):
  return render(request, 'index.html')

def analyze(request):
  try:
    # fetching the text
    ftext = request.POST.get('text')
 

    # Check checkbox value
    yload = request.POST.get('yload', 'off')
    wload = request.POST.get('wload', 'off')

    initWorkDir = os.getcwd()
    currDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(currDir)
    if os.path.exists('downloadedFiles'):
      shutil.rmtree('downloadedFiles')
    os.mkdir('downloadedFiles')
    os.chdir('downloadedFiles')
    #Check which checkbox is on
    if yload == "on":
        url = ftext
        video = pafy.new(url)
        bestResolutionVideo = video.getbest()
        bestResolutionVideo.download()
        response = download(bestResolutionVideo.filename)
        os.chdir(initWorkDir)
        return response

    elif(wload=="on"):
      url = ftext
      myvideo = url.split("/")[-1] 
    
      raw = requests.get(url, stream=True)
      with open(myvideo, 'wb') as fd:
        for chunk in raw.iter_content(chunk_size=1024):
          fd.write(chunk)
      fd.close()
      response = download(myvideo)
      os.chdir(initWorkDir)
      return response
       # analyzed = ""
      #  for char in djtext:
        #    analyzed = analyzed + char.upper()

      #  params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}
        # Analyze the text
      #  return render(request, 'analyze.html', params)
        
    else:
        os.chdir(initWorkDir)
        return HttpResponse("Error")

  
  except Exception as e:
    print(e)