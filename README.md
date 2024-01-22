# multimodal-inputs
Converting websites/youtube videos/audio snippets to text to eventually remove irrelevant content.

## How to run:

Make sure to download the speech to text model from [here](https://alphacephei.com/vosk/models) and rename the folder to `model/`. 

This also requires `ffmpeg` which can be downloaded from [here](https://ffmpeg.org/download.html).
```
pip install -r requirements.txt
python multimodality.py youtube/website youtube link/website url
```

