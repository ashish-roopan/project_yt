import librosa
import librosa.display
import soundfile as sf
import pedalboard
from pedalboard import Compressor, Gain, Reverb
import torchaudio


def add_reverb(audiofile, interval):
    # y, sr = librosa.load(audiofile, sr=44100)
    # y, sr = sf.read(audiofile)
    y, sr = torchaudio.load(audiofile)
    y = y[0].numpy()

    #. Extract the music 
    music = y[interval[0]*sr:interval[1]*sr]
    
    #. Apply the reverb effect
    music = board.process(music, sr)
    
    #. replace the original audio with the processed music
    y[interval[0]*sr:interval[1]*sr] = music

    return y, sr

board = pedalboard.Pedalboard([
    Compressor(ratio=10, threshold_db=-20),
    # Gain(gain_db=-1),
    # Phaser(),
    Reverb(room_size=0.95, damping=0.77, wet_level=0.42, dry_level=1, width=0),
])

