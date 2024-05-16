import os
from moviepy.editor import ImageClip, AudioFileClip

def make_video(audio_path, image_path, output_path):
    # Load the image clip
    image_clip = ImageClip(image_path)

    # Load the audio clip
    audio_clip = AudioFileClip(audio_path)

    # Set the duration of the video to match the duration of the audio
    image_clip = image_clip.set_duration(audio_clip.duration)

    # Combine the image and audio clips
    video_clip = image_clip.set_audio(audio_clip)

    # Export the combined video
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=5, threads=32, preset='ultrafast')


def add_audio_to_thumbnail(audio_files, input_dir):
    print('\n______________________ Making Video ______________________\n')
    thumbnails_dir = os.path.join(input_dir, 'thumbnails')
    output_dir = os.path.join(input_dir, 'videos')
    os.makedirs(output_dir, exist_ok=True)
    for audio_file in audio_files:
        thumbnail = os.path.join(thumbnails_dir, os.path.basename(audio_file).replace('.m4a', '.png'))
        output_file = os.path.join(output_dir, os.path.basename(audio_file).replace('.m4a', '.mp4'))
        make_video(audio_file, thumbnail, output_file)
