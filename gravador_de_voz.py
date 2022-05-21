# codigo adaptado a partir de outro encontrado em https://gist.github.com/mabdrabo/8678538
import pyaudio
import wave
import os

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 6

def gravar_microfone(temp_dir=".", segundos=RECORD_SECONDS):
    audio = pyaudio.PyAudio()

    # start recording
    print("fale alguma coisa...")
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    for _ in range(0, int(RATE / CHUNK * segundos)):
        data = stream.read(CHUNK)
        if data:
            frames.append(data)

    # stop secording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save temporary audio file
    arquivo_temporario = temp_dir + "/speech.wav"
    if os.path.isfile(arquivo_temporario):
        os.remove(arquivo_temporario)

    print(f"arquivo de audio sendo gerado: {arquivo_temporario}")
    with wave.open(arquivo_temporario, "wb") as wave_file: 
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

    return os.path.isfile(arquivo_temporario), arquivo_temporario