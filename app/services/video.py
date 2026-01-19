import os
import uuid
import httpx
from pathlib import Path
from app.config import TEMP_DIR

# --- 1. PILLOW COMPATIBILITY FIX ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS

# Now safe to import moviepy
from moviepy.editor import AudioFileClip, ImageClip

# --- 2. DOWNLOAD UTILITIES ---

def download_thumbnail(thumbnail_url: str) -> str:
    thumb_path = TEMP_DIR / f"thumb_{str(uuid.uuid4())[:8]}.jpg"
    with httpx.Client(follow_redirects=True) as client:
        resp = client.get(thumbnail_url)
        resp.raise_for_status()
        with open(thumb_path, "wb") as f:
            f.write(resp.content)
    return str(thumb_path)

# --- 3. CORE VIDEO GENERATION ---

def create_video(audio_path: str, thumbnail_path: str) -> str:
    video_id = str(uuid.uuid4())[:8]
    output_path = TEMP_DIR / f"video_{video_id}.mp4"

    audio = AudioFileClip(audio_path)
    img_clip = ImageClip(thumbnail_path, duration=audio.duration)
    
    # Standardize to 1080p and ensure even dimensions for libx264
    img_clip = img_clip.resize(height=1080)
    w, h = img_clip.size
    if w % 2 != 0: w += 1
    if h % 2 != 0: h += 1
    img_clip = img_clip.resize(newsize=(w, h))

    final_clip = img_clip.set_audio(audio)
    final_clip.write_videofile(
        str(output_path),
        fps=1,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        threads=4,
        logger=None
    )

    audio.close()
    final_clip.close()
    return str(output_path)

# --- 4. EXPORTED PIPELINES (Used by telegram.py) ---

def process_uploaded_audio(audio_path: str, thumbnail_path: str) -> str:
    """Pipeline for files sent directly in chat"""
    print(f"🎬 Processing uploaded audio: {audio_path}")
    
    video_path = create_video(audio_path, thumbnail_path)
    
    print(f"✅ Video processing completed: {video_path}")
    return video_path

def cleanup_temp_files(*file_paths: str):
    for path in file_paths:
        if path and os.path.exists(path):
            try: os.remove(path)
            except: pass