import os
import torch
import torchaudio
import sys
sys.path.append('.')
from resemble_enhance.resemble_enhance.enhancer.inference import denoise, enhance
from scipy.io.wavfile import write


def _fn(input, output, solver, nfe, tau, denoising):
    if input is None:
        return None, None

    print("path:", input)
    print("solver:", solver)
    print("nfe:", nfe)
    print("tau:", tau)
    print("denoising:", denoising)
    print("output:", output)
    print()
    
    solver = solver.lower()
    nfe = int(nfe)
    lambd = 0.9 if denoising else 0.1

    dwav, sr = torchaudio.load(input)
    dwav = dwav.mean(dim=0)

    # wav1, new_sr = denoise(dwav, sr, device)
    wav2, new_sr = enhance(dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau)
    
    wav2 = wav2.cpu().numpy()
    write(output, new_sr, wav2)

def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='data/audio/raw')
    parser.add_argument("--output", type=str, default='data/audio/denoised')
    parser.add_argument("--solver", type=str, default="midpoint")
    parser.add_argument("--nfe", type=int, default=64)
    parser.add_argument("--tau", type=float, default=0.5)
    parser.add_argument("--denoising", action="store_true")
    return parser.parse_args()



if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

args = parse_args()
raw_files = os.listdir(args.input)
for raw_file in raw_files:
    input_file = os.path.join(args.input, raw_file)
    output_file = os.path.join(args.output, os.path.basename(input_file))
    print(f"Processing {input_file}...")
    _fn(input_file, output_file, args.solver, args.nfe, args.tau, args.denoising)