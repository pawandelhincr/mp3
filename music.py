import tkinter as tk
from tkinter import filedialog
import pygame
import os

class MacMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("VS Code MP3 Player")
        self.root.geometry("400x250")
        
        # UI को थोड़ा सुंदर बनाने के लिए
        self.root.configure(bg='#2c3e50')
        
        pygame.mixer.init()

        # गाने का नाम दिखाने के लिए लेबल
        self.status = tk.Label(root, text="कोई गाना चुनें", bg="#08192a", fg='white', font=("Arial", 12))
        self.status.pack(pady=20)

        # बटन्स का फ्रेम
        button_frame = tk.Frame(root, bg='#2c3e50')
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="गाना लोड करें", command=self.load_song, width=12).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Play/Pause", command=self.toggle_music, width=12).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Stop", command=self.stop_music, width=12).grid(row=0, column=2, padx=5)

        # वॉल्यूम स्लाइडर (Volume Slider)
        tk.Label(root, text="वॉल्यूम कम/ज्यादा करें", bg='#2c3e50', fg='white').pack(pady=5)
        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume, bg='#2c3e50', fg='white')
        self.volume_scale.set(70) # डिफॉल्ट वॉल्यूम 70%
        self.volume_scale.pack()

        self.paused = False

    def load_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if file_path:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.status.config(text=f"बज रहा है: {os.path.basename(file_path)}")

    def toggle_music(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.status.config(text="गाना बंद है")

    def set_volume(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)

if __name__ == "__main__":
    root = tk.Tk()
    app = MacMusicPlayer(root)
    root.mainloop()
    from flask import Flask, render_template, jsonify, request
import pygame
import os

app = Flask(__name__)

# Initialize Pygame Mixer
pygame.mixer.init()

# Path where your MP3 files are stored
MUSIC_DIR = "music_files" 
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

@app.route('/')
def index():
    songs = [f for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
    return render_template('index.html', songs=songs)

@app.route('/play/<song_name>')
def play_song(song_name):
    try:
        song_path = os.path.join(MUSIC_DIR, song_name)
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        return jsonify({"status": "Playing", "song": song_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pause')
def pause_song():
    pygame.mixer.music.pause()
    return jsonify({"status": "Paused"})

@app.route('/resume')
def resume_song():
    pygame.mixer.music.unpause()
    return jsonify({"status": "Resumed"})

@app.route('/stop')
def stop_song():
    pygame.mixer.music.stop()
    return jsonify({"status": "Stopped"})

if __name__ == '__main__':
    # Hosted on 0.0.0.0 so Docker can map it correctly
    app.run(host='0.0.0.0', port=5000, debug=True)