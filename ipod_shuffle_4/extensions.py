#!/bin/env python3

fullpath = 'fullpath'


original_name = 'original_name'
checksum = 'checksum'
size = 'size'
mtime = 'mtime'
filename = 'filename'
dbid = 'dbid'
string = 'string'
lang = 'lang'
voice_string = 'voice_string'
text = 'text'

user_track_record = [
    {checksum: 'd41d8cd98f00b204e9800998ecf8427e',
     fullpath: '/media/data/music/张学友 - 吻别.mp3',
     size: 129871,
     mtime: 896182345876}
]

user_track_record2 = [
    {'/media/data/music/张学友 - 吻别.mp3':
         {checksum: 'd41d8cd98f00b204e9800998ecf8427e', size: 129871, mtime: 896182345876}
    }
]



track_add_info = {
    'alskflsaflsakfjslflj':
    {
        'checksum': 'd41d8cd98f00b204e9800998ecf8427e',
        'voice_string': '张学友 吻别',
        'voice_lang': 'zh_CN',
        'name': '张学友 - 吻别.mp3',
    }
}

playlist_add_info = {
    'alskflsaflsakfjslflj':
    {
        'name': '国语',
        'voice_string': '国语',
        'voice_lang': 'zh_CN'
    }
}
