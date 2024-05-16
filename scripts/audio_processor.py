import yaml
import os
import torchaudio
import sys
sys.path.append('.')
from resemble_enhance.resemble_enhance.enhancer.inference import enhance, denoise
from scipy.io.wavfile import write
from scripts.add_reverb import add_reverb
from colorama import Fore, Back, Style


class AudioProcessor:
    def __init__(self, args):
        self.device = args.device
        self.solver = args.solver
        self.nfe = args.nfe
        self.tau = args.tau
        self.denoising = args.denoising
    
        self.audio_dir = os.path.join(args.input, 'audio')
        self.raw_path = os.path.join(self.audio_dir, 'raw')
        self.denoised_path = os.path.join(self.audio_dir, 'denoised')
        self.reverbed_path = os.path.join(self.audio_dir, 'reverbed')
        self.interval_file = os.path.join(self.audio_dir, 'intervals.yaml')
        os.makedirs(self.denoised_path, exist_ok=True)
        os.makedirs(self.reverbed_path, exist_ok=True)

        self.raw_files = [os.path.join(self.raw_path, f) for f in os.listdir(self.raw_path)]
        self.denoised_files = [os.path.join(self.denoised_path, f) for f in os.listdir(self.raw_path)]
        self.reverbed_files = [os.path.join(self.reverbed_path, f) for f in os.listdir(self.raw_path)]
        self.intervals = self.get_intervals()

    def get_intervals(self):
        #. Create a dictionary of intervals if file does not exist
        if not os.path.exists(self.interval_file):
            intervals = {os.path.basename(f): None for f in self.raw_files}
            with open(self.interval_file, 'w') as f:
                yaml.dump(intervals, f)
        else:
            with open(self.interval_file, 'r') as f:
                intervals = yaml.load(f, Loader=yaml.FullLoader)
        
        for k, v in intervals.items():
            if v is None:
                intervals[k] = None
            else:
                start = int(v.split('-')[0].split(':')[0])*60 + int(v.split('-')[0].split(':')[1])
                end = int(v.split('-')[1].split(':')[0])*60 + int(v.split('-')[1].split(':')[1])
                intervals[k] = (start, end)
        return intervals

    def denoise_all(self, input_files):
        print(Style.BRIGHT + '\n______________________ Denoising ______________________\n' + Style.RESET_ALL)
        processed_files = []
        for input_file in input_files:
            print('  Processing:', Fore.LIGHTCYAN_EX + input_file + Style.RESET_ALL, end=' ')
            output_file = os.path.join(self.denoised_path, os.path.basename(input_file))
            processed_files.append(output_file)
            if os.path.exists(output_file):
                print(Style.BRIGHT + Fore.YELLOW +'  Already exists' + Style.RESET_ALL)
                continue
            print()
            self.__class__.denoise_audio(input_file, output_file, self.solver, self.nfe, self.tau, self.denoising, self.device)
        print()
        return processed_files

    @staticmethod
    def denoise_audio(input, output, solver, nfe, tau, denoising, device):
        if input is None:
            return None, None

        solver = solver.lower()
        nfe = int(nfe)
        lambd = 0.9 if denoising else 0.1

        dwav, sr = torchaudio.load(input)
        dwav = dwav.mean(dim=0)

        # wav1, new_sr = denoise(dwav, sr, device)
        wav2, new_sr = enhance(dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau)
        
        # wav1 = wav1.cpu().numpy()
        wav2 = wav2.cpu().numpy()
        
        # write(output, new_sr, wav1)
        write(output, new_sr, wav2)

    def reverb_all(self, input_files):
        print(Style.BRIGHT + '\n______________________ Reverb ______________________\n' + Style.RESET_ALL)
        processed_files = []
        for input_file in input_files:
            print('  Processing:', Fore.LIGHTCYAN_EX + input_file + Style.RESET_ALL, end=' ')
            output_file = os.path.join(self.reverbed_path, os.path.basename(input_file))
            processed_files.append(output_file)            
            # try statement to handle the case where the interval key is not present
            # if not keyerror, then the print any other error message
            try:
                interval = self.intervals[os.path.basename(input_file)]
            except KeyError:
                print(Style.BRIGHT + Fore.RED +'  Interval not provided : Skipping Reverb'+  Style.RESET_ALL)
                continue
            
            if os.path.exists(output_file):
                print(Style.BRIGHT + Fore.YELLOW +'  Already exists' + Style.RESET_ALL)
                continue
            elif interval is None:
                print(Style.BRIGHT + Fore.RED +'  Interval not provided : Skipping Reverb'+  Style.RESET_ALL)
                continue
            else: 
                print(f'| Interval: [ {interval[0]} - {interval[1]}]', end=' ')
            
            y, sr = add_reverb(input_file, interval)
            write(output_file, sr, y)
            print(Style.BRIGHT + Fore.GREEN +'  Done' + Style.RESET_ALL)
        print('\n')
        return processed_files
