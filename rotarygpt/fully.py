import requests
import subprocess
import threading


class FullyTTSRequest:
    default_voice = "nova"
    voice = default_voice

    def __init__(self, chunk_callback, shutdown_event):
        self.chunk_callback = chunk_callback
        self.shutdown_event = shutdown_event

        self.socket = None
        self.texttospeech_path = "https://fully-wek1.onrender.com/text-to-speech"

    def send_request(self, text):
        params = {
            "voiceId": FullyTTSRequest.voice,
            "modelId": "eleven_monolingual_v1",
            "text": text,
            "optimizationLevel": 4,
        }

        self.response = requests.get(self.texttospeech_path, params=params, stream=True)

        if self.response.status_code != 200:
            print(f"Failed to retrieve data. Status code: {self.response.status_code}")

    def get_response(self):
        ffmpeg_process = subprocess.Popen(
            ['ffmpeg', '-i', 'pipe:0', '-f', 's16le', '-acodec', 'pcm_s16le', '-ar', '8000', '-ac', '1', '-'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        def feed_pcm_to_queue():
            while not self.shutdown_event.is_set():
                pcm_chunk = ffmpeg_process.stdout.read(4096)
                if not pcm_chunk:
                    break
                self.chunk_callback(pcm_chunk)

        thread = threading.Thread(target=feed_pcm_to_queue)
        thread.start()

        try:
            for chunk in self.response.iter_content(chunk_size=4096):
                ffmpeg_process.stdin.write(chunk)
                ffmpeg_process.stdin.flush()
        finally:
            ffmpeg_process.stdin.close()

        thread.join()
        ffmpeg_process.wait()
