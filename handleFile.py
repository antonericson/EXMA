from constants import *
import os
import pyexiv2
from exif import Image
import exiftool
from hashlib import sha256
from datetime import datetime

def getFilePaths(conversation_path, file_data, file_type):
    original_file_name = file_data['uri'].split('/')[-1]
    original_file_path =f'{conversation_path}/{file_type}/{original_file_name}'
    created_date = datetime.fromtimestamp(file_data['creation_timestamp'])
    salt_string = sha256(original_file_name.encode('utf-8')).hexdigest()[0::5]
    file_format = file_data['uri'].split('/')[-1].split(".")[-1]
    new_file_name = f'{created_date.strftime("%Y-%m-%dT%H%M%S")}-{salt_string}.{file_format}'
    
    output_folder_path = f'./{OUTPUT_FOLDER_NAME}/{datetime.now().strftime("%Y-%m-%dT%H%M")}'
    new_file_path = f'{output_folder_path}/{new_file_name}'
    
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    return {
        'original': original_file_path,
        'new': new_file_path
    }

def handleJpgFile(conversation_path, file_data):
    paths = getFilePaths(conversation_path, file_data, PHOTOS_TAG)
    # Modify metadata
    original = None
    with open(paths['original'], 'rb') as original_file:
        original = Image(original_file)
        date_formatted = datetime.fromtimestamp(file_data['creation_timestamp']).strftime("%Y:%m:%d %H:%M:%S")
        original.datetime_original = date_formatted

    # Save new file
    with open(paths['new'], 'wb') as new_file:
        new_file.write(original.get_file())
        
def handlePngFile(conversation_path, file_data):
    paths = getFilePaths(conversation_path, file_data, PHOTOS_TAG)
    with open(paths['original'], 'rb') as original_file, open(paths['new'], 'wb') as new_file:
        new_file.write(original_file.read())
    
    with pyexiv2.Image(paths['new']) as img:
        date_formatted = datetime.fromtimestamp(file_data['creation_timestamp']).strftime("%Y:%m:%d %H:%M:%S")
        xmpData = {
            'Xmp.xmp.CreateDate': date_formatted,
            'Xmp.xmp.ModifyDate': date_formatted,
            'Xmp.xmp.DateTimeOriginal': date_formatted
        }
        exifData = {'Exif.Image.DateTime': date_formatted}
        img.modify_exif(exifData)
        img.modify_xmp(xmpData)

def handleMp4File(conversation_path, file_data):
    paths = getFilePaths(conversation_path, file_data, VIDEOS_TAG)
    date_formatted = datetime.fromtimestamp(file_data['creation_timestamp']).strftime("%Y:%m:%d %H:%M:%S")
    
    with open(paths['original'], 'rb') as original_file, open(paths['new'], 'wb') as new_file:
        new_file.write(original_file.read())
    
    with exiftool.ExifToolHelper() as eth:
        eth.set_tags(paths['new'], tags={"QuickTime:CreateDate": date_formatted}, params={'-overwrite_original'})