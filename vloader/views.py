from django.shortcuts import render
from django.http import HttpResponse
import pafy
import requests

def index(request):
    return render(request, 'index.html')

def analyze(request):
  try:
    # fetching the text
    ftext = request.POST.get('text')
 

    # Check checkbox value
    yload = request.POST.get('yload', 'off')
    wload = request.POST.get('wload', 'off')
    #Check which checkbox is on
    if yload == "on":
        url = ftext
        video = pafy.new(url)
        bestResolutionVideo = video.getbest()
        bestResolutionVideo.download()
        
        return HttpResponse("done")

        
    elif(wload=="on"):
      url = ftext
      myvideo = url.split("/")[-1] 
    
      raw = requests.get(url, stream=True)
      with open(myvideo, 'wb') as fd:
        for chunk in raw.iter_content(chunk_size=1024):
          fd.write(chunk)
      return HttpResponse("done")
       # analyzed = ""
      #  for char in djtext:
        #    analyzed = analyzed + char.upper()

      #  params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}
        # Analyze the text
      #  return render(request, 'analyze.html', params)
        
    else:
        return HttpResponse("Error")

  
  except Exception as e:
    print(e)