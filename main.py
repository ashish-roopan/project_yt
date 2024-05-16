import argparse
from colorama import Style

from scripts.audio_processor import AudioProcessor
from scripts.video_maker import add_audio_to_thumbnail



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='data')
    parser.add_argument("--solver", type=str, default="midpoint")
    parser.add_argument("--nfe", type=int, default=64)
    parser.add_argument("--tau", type=float, default=0.5)
    parser.add_argument("--denoising", type=bool, default=True)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()
    print(Style.BRIGHT + '\n\n______________________ Arguments ______________________\n' + Style.RESET_ALL)
    print('  input_dir:', args.input)
    print('  solver:', args.solver)
    print('  nfe:', args.nfe)
    print('  tau:', args.tau)
    print('  denoising:', args.denoising)
    print('  device:', args.device)
    return args


args = parse_args()
processor = AudioProcessor(args)

#. Denoise all the audio files
# files = processor.denoise_all(processor.raw_files)

processor.denoised_files = ['data/audio/denoised/slokam7.wav', 'data/audio/denoised/slokam8.wav']
print(processor.denoised_files)
#. Add reverb to audio
files = processor.reverb_all(processor.denoised_files)

#. Add audio to the thumbnail
# add_audio_to_thumbnail(files, args.input)