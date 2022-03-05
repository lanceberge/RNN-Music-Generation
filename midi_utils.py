#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import re
from IPython.display import Audio
from pretty_midi import PrettyMIDI


def download_midis(download_dir, genre='classic'):
    """
    Download midi files from midiword.com
    Code from: https://stackoverflow.com/questions/52124737/why-cant-i-download-a-midi-file-with-python-requests
    """
    main_page = requests.get('http://www.midiworld.com/'+genre+'.htm')
    parsed_page = BeautifulSoup(main_page.content, 'html.parser')

    links = parsed_page.find_all('a', href=re.compile('mid$'))
    
    
    def getFileName(link):
        link = link['href']
        filename = link.split('/')[::-1][0]
        return filename

    
    def downloadFile(link, filename):
        mid_file = requests.get(link['href'], stream=True)
        with open(download_dir+filename, 'wb') as saveMidFile:
            saveMidFile.write(mid_file.content)
          
        
    for link in links:
        filename = getFileName(link)
        downloadFile(link, filename)
        
        
def play_midi(midi_path):
    midi_data = PrettyMIDI(midi_file=midi_path)

    return Audio(midi_data.synthesize(fs=22050), rate=22050)