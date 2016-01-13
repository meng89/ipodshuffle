#!/usr/bin/env python3
import os
import sys

from ipod_shuffle_4 import Shuffle
from ipod_shuffle_4 import utils


def getShuffleAudioFiles(folder):
    audioFiles = []
    for file in os.listdir(folder):
        if os.path.isfile(file):
            if utils.is_able_file(file):
                audioFiles.append(os.path.realpath(file))
            else: break
        elif os.path.isdir(file):
            getShuffleAudioFiles(file)
    return audioFiles


def main():
    com = sys.argv[1]
    if com in ('-s', '--sync'):
        source_dir, my_shuffle = sys.argv[2], Shuffle(sys.argv[3])
        sync(source_dir, my_shuffle)


def sync(source_dir,my_shuffle):
    audioFilenames = getShuffleAudioFiles(source_dir)
    newTracks = []
    for audio in audioFilenames:
        track = my_shuffle.getExistTrackFromFilename(audio)
        if not track:
            track = my_shuffle.add_sound(audio)
        newTracks.append([audio,track])

    newPlaylists = []
    for file in os.listdir(source_dir):
        if os.path.isdir(file):
            audioFiles = getShuffleAudioFiles(file)
            if audioFiles:
                tracks = []
                for audio in audioFiles:
                    for newTrack in newTracks:
                        if newTrack[0] == audio:
                            tracks.append(newTrack[1])
                            break
                newPlaylists.append([os.path.split(file)[-1],tracks])

    tracks_need_to_del = []
    for track in my_shuffle.tracks:
        if track not in [newTrack[0] for newTrack in newTracks]:
            tracks_need_to_del.append(track)
    for track in tracks_need_to_del:
        my_shuffle.del_track(track)

    playlist_need_to_del = []
    for playlist in my_shuffle.playlists:
        if playlist.name not in [newPlaylist[0] for newPlaylist in newPlaylists]:
            playlist_need_to_del.append(playlist)
    for playlist in playlist_need_to_del:
        my_shuffle.del_playlist(playlist)

    for newPlaylist in newPlaylists:
        playlist = my_shuffle.getExistPlaylistFromName(newPlaylist[0])
        if not playlist:
            playlist = my_shuffle.add_playlist(newPlaylist[0])
        for track in newPlaylist[1]:
            if track not in playlist.tracks:
                playlist.tracks.append(track)
    my_shuffle.finish()

#if __name__ == '__main__':main()

shuffle = Shuffle('/media/data/mine/program/libre_shuffle/temp/ipod')
shuffle = Shuffle("/run/media/obs/OBS' IPOD/")
print(len(shuffle.get_all_tracks()),len(shuffle.get_all_playlists()))

