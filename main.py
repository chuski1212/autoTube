import datetime
import logging
import settings
from twitch_api import get_clips_by_lang
from video_edition import edit_video
from youtube_service import upload_video, upload_thumbnail
from cleaning import clean_files

# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# clips = ['0', '1']
# clips = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
# first_title = 'RandomTitle'


def setup():
    logging.basicConfig(filename=settings.LOGS_DIRECTORY + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log', level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started')


def generate_video():
    if settings.ENVIRONMENT == 'production':
        setup()
    logging.info('Starting to clean the files')
    clean_files()
    logging.info('Files cleaned')

    clips, first_clip_title, first_streamer = get_clips_by_lang('all')
    edit_video(clips)
    video_id = upload_video(first_clip_title)
    upload_thumbnail(video_id, first_streamer, first_clip_title)

try:
    generate_video()
except Exception as e:
    logging.error(str(e))
    print(str(e))    