import glob
import taglib
from subprocess import check_output, CalledProcessError

AUDIO_PATH = '/volume/files/'
OUTPUT_PATH = '/volume/output/'


def get_onsets(audio_file):
    for line in ''.join(check_output(['aubioonset', audio_file])).split('\n'):
        if len(line) > 0:
            yield line


def get_pitches(audio_file):
    for line in ''.join(check_output(['aubiopitch', audio_file])).split('\n'):
        if len(line) > 0:
            yield line.split(' ')


def get_files():
    return glob.glob(AUDIO_PATH + '**/*.flac') + \
        glob.glob(AUDIO_PATH + '**/*.mp3')


def write_onsets(id, filename):
    with open(OUTPUT_PATH + 'onsets.csv', 'a') as o:
        for onset in get_onsets(filename):
            o.write(','.join([str(id), onset]) + '\n')


def write_pitches(id, filename):
    with open(OUTPUT_PATH + 'pitch.csv', 'a') as o:
        for time, pitch in get_pitches(filename):
            o.write(','.join([str(id), time, pitch]) + '\n')

processing_errors = False
with open(OUTPUT_PATH + 'files.csv', 'w') as o:
    for i, audio_file in enumerate(get_files(), 1):
        print('Processing file ' + str(i) + ': ' + audio_file)
        filename = audio_file[len(AUDIO_PATH):]
        tags = taglib.File(audio_file).tags
        values = [
            '"' + tags[key][0].encode('utf-8') + '"' for key in [
                'ARTIST',
                'ALBUM',
                'TITLE'
            ]
        ]
        values = [str(i), '"' + filename + '"'] + values
        csv_line = ','.join(values)
        o.write(csv_line + '\n')
        try:
            write_onsets(i, AUDIO_PATH + filename)
            write_pitches(i, AUDIO_PATH + filename)
        except CalledProcessError as error:
            processing_errors = True
            print('Error processing file: ' + filename)
            with open(OUTPUT_PATH + 'errors.log', 'a') as e:
                e.write(filename + '\n')

if processing_errors:
    print('Errors occurred while processing some files. See output/errors.log')
