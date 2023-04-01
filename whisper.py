# Import the libraries 
import whisper
import torch 
import os

# Set the device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the model 
whisper_model = whisper.load_model("tiny", device=device) # large
# tiny	~1 GB	~32x
#base	74 M	base.en	base	~1 GB	~16x
#small	244 M	small.en	small	~2 GB	~6x
#medium	769 M	medium.en	medium	~5 GB	~2x
#large	1550 M	N/A	large
from pytube import YouTube


def video_to_audio(video_URL, destination, final_filename):

  # Get the video
  video = YouTube(video_URL)

  # Convert video to Audio
  audio = video.streams.filter(only_audio=True).first()

  # Save to destination
  output = audio.download(output_path = destination)

  _, ext = os.path.splitext(output)
  new_file = output + final_filename + '.mp3'

  # Change the name of the file
  os.rename(output, new_file)

# Video to audio
#video_URL = 'https://www.youtube.com/watch?v=KCTbAbNH2UQ'
# video prueba
print ("cero")
video_URL = 'https://www.youtube.com/watch?v=uv357YzY7-k'
destination = '.'
final_filename = "prueba"
#final_filename = "mananera_03_31"
#video_to_audio(video_URL, destination, final_filename)


print ("uno")
# Run the test
result_ADO = whisper_model.transcribe('prueba.mp3')
print ("dos")
print(result_ADO["text"])

# Run the test
spa_to_english = whisper_model.transcribe('prueba.mp3', task = 'translate', language = "Spanish")
# Show the result
print(spa_to_english["text"])
     
