#!/usr/bin/env python3
import json
from glob import glob
from handleFile import handleJpgFile, handlePngFile, handleMp4File 
from constants import *

def main():
    conversations = glob(f'{DATA_PATH}/*', recursive=True)

    for conversation_path in conversations:
        file_paths = glob(f'{conversation_path}/*', recursive=True)
        if f'{conversation_path}/{VIDEOS_TAG}' not in file_paths and f'{conversation_path}/{PHOTOS_TAG}' not in file_paths:
            continue
        
        json_paths = glob(f'{conversation_path}/*.json')
        for json_path in json_paths:
            with open(json_path) as file:
                jsonObject = json.load(file)
                for msg in jsonObject['messages']:
                    
                    if PHOTOS_TAG in msg:
                        for photo_data in msg[PHOTOS_TAG]:
                            if photo_data['uri'].split('/')[-1].split(".")[-1] == 'jpg':
                                handleJpgFile(conversation_path, photo_data)
                            else:
                                handlePngFile(conversation_path, photo_data)
                                
                    if VIDEOS_TAG in msg:
                        for video_data in msg[VIDEOS_TAG]:
                            handleMp4File(conversation_path, video_data)
                        
if __name__ == "__main__":
    main()                    
