#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 21:42:40 2018

@author: pirate
"""

from pydub import AudioSegment
sound = AudioSegment.from_mp3("black.mp3")
sound.export("black.wav", format="wav")