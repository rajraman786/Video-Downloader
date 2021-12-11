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
    ftext = str(ftext)

    # boolean to tell whether the video is of youtube or not
    isYtUrl = ftext.startswith("https://www.youtube.com/watch?v=")

    initWorkDir = os.getcwd()
    currDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(currDir)
    if os.path.exists('downloadedFiles'):
      shutil.rmtree('downloadedFiles')
    os.mkdir('downloadedFiles')
    os.chdir('downloadedFiles')
    
    #Check which checkbox is on
    if isYtUrl:
        url = ftext
        video = pafy.new(url)
        bestResolutionVideo = video.getbest()
        bestResolutionVideo.download()
        response = download(bestResolutionVideo.filename)
        os.chdir(initWorkDir)
        return response

    else:
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
  
  except Exception as e:
    print(e)
    return HttpResponse("Error")