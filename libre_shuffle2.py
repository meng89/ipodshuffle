#!/bin/env python3

import sys
import getopt

"""
libre_shuffle shuffle=/media/shuffle4_dir src=/media/data/sounds_dir lang=zh_CN
    the shuffle4_dir is the ipod shuffle 4 mount point
    the sounds_dir is the dir contains the following dirs:
        n_pls
            Nothing Like The Love I Have For You
                1000 Songs
                Toilet
                Home Alone
                Nothing Like The Love I Have For You
                The Heart Is What We Need The Most
                Tomorrow Tomorrow Not Today
                Sleep With You
                Hard Work And Fate
                I Just Don't Care Anymore
                Let's Go Crazy
                Grow A Heart
                Happy
                Dot
                2000 Instrumentals

        a_pls
            2  Mary Queen Of Scots
                1 Fotheringhay.mp3
                2 France.mp3
                3 Darnley and Riccio.mp3
                4 The death of David Riccio.mp3
                5 My son is born.mp3
                6 Kirk O'Field.mp3
                7 Bothwell.mp3
                8 England.mp3
                9 A Death.mp3

"""


def usage():
    print('Usage: %s [OPTION]... -s sounds_dir -d ipod_shuffle4_dir' % sys.argv[0])
    print('  or : %s [OPTION]... --npls npl_dir1 npl_dir2 ... --apls apls_dir1 apls_dir2 ...'
          ' -d ipod_shuffle4_dir' % sys.argv[0])

    print('Options:')
    print(' -s')

    print(' --pls')
    print(' --imp  in master playlist')
    print(' --rpp  remember playing pos')

def main():
    options = {}
    getopt.getopt(sys.argv[1:], 's:d:', ['help'])

    if

main()