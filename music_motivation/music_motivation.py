import tkinter as tk
from tkinter import ttk
import pygame
import os
import random

class MusicMotivationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        pygame.mixer.init()
        self.create_widgets()

    def create_widgets(self):
        # Music Player
        music_frame = ttk.LabelFrame(self, text="Ambient Music Player")
        music_frame.pack(fill="x", padx=10, pady=5)
        self.music_files = self.get_music_files()
        self.music_list = tk.Listbox(music_frame, height=3)
        for f in self.music_files:
            self.music_list.insert(tk.END, f)
        self.music_list.pack(side=tk.LEFT, padx=5)
        ttk.Button(music_frame, text="Play", command=self.play_music).pack(side=tk.LEFT, padx=5)
        ttk.Button(music_frame, text="Stop", command=self.stop_music).pack(side=tk.LEFT, padx=5)

        # Guided Meditation
        meditation_frame = ttk.LabelFrame(self, text="Guided Meditation")
        meditation_frame.pack(fill="x", padx=10, pady=5)
        self.meditation_files = self.get_meditation_files()
        self.meditation_list = tk.Listbox(meditation_frame, height=3)
        for f in self.meditation_files:
            self.meditation_list.insert(tk.END, f)
        self.meditation_list.pack(side=tk.LEFT, padx=5)
        ttk.Button(meditation_frame, text="Play", command=self.play_meditation).pack(side=tk.LEFT, padx=5)
        ttk.Button(meditation_frame, text="Stop", command=self.stop_music).pack(side=tk.LEFT, padx=5)

        # Motivational Quotes
        quote_frame = ttk.LabelFrame(self, text="Motivational Quotes")
        quote_frame.pack(fill="x", padx=10, pady=5)
        self.quote_label = ttk.Label(quote_frame, text=self.get_random_quote(), wraplength=400)
        self.quote_label.pack(pady=5)
        ttk.Button(quote_frame, text="New Quote", command=self.show_new_quote).pack(pady=5)

    def get_music_files(self):
        music_dir = os.path.join("assets", "music")
        if not os.path.exists(music_dir):
            os.makedirs(music_dir)
        return [f for f in os.listdir(music_dir) if f.endswith(".mp3")]

    def get_meditation_files(self):
        meditation_dir = os.path.join("assets", "meditation")
        if not os.path.exists(meditation_dir):
            os.makedirs(meditation_dir)
        return [f for f in os.listdir(meditation_dir) if f.endswith(".mp3")]

    def play_music(self):
        idx = self.music_list.curselection()
        if not idx:
            return
        file = self.music_files[idx[0]]
        path = os.path.join("assets", "music", file)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def play_meditation(self):
        idx = self.meditation_list.curselection()
        if not idx:
            return
        file = self.meditation_files[idx[0]]
        path = os.path.join("assets", "meditation", file)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def get_random_quote(self):
        quotes_path = os.path.join("assets", "quotes.txt")
        if not os.path.exists(quotes_path):
            with open(quotes_path, "w") as f:
                f.write("You are enough.\nKeep going.\nBreathe in, breathe out.\n")
        with open(quotes_path, "r") as f:
            quotes = [line.strip() for line in f if line.strip()]
        return random.choice(quotes) if quotes else "Stay motivated!"

    def show_new_quote(self):
        self.quote_label.config(text=self.get_random_quote())
