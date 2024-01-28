from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import moviepy.video.fx.all as vfx
import os
import mux_python
from mux_python.rest import ApiException
import requests 
import uuid 
from moviepy.editor import *
from moviepy.video.compositing.concatenate import concatenate_videoclips
from time import sleep
import re 
import json 
import gizeh
import tempfile
import os 
import json
import sys

# os.chdir('/tmp')

def main(video_source, website_screenshot_url, linkedin_screenshot_url, script1_url, upload_url):
    def generate_video():
        print('starting to process the video with moviepy')
        # load video 1
        vid1 = VideoFileClip(VID1)
        print('check 1')
        vid1 = vid1.resize(0.6) # 70% of its size
        print('check 2')

        def create_circle(size, name):
            WIDTH, HEIGHT = size
            surface = gizeh.Surface(WIDTH, HEIGHT)

            circle = gizeh.circle(r=min(WIDTH, HEIGHT)//2, fill=(2,2,2), xy=(WIDTH//2, HEIGHT//2))

            circle.draw(surface)

            # save to png
            surface.write_to_png(name)

        ''' CREATE MASK AND ADD IT TO VIDEO '''
        # generate mask png with correct size
        create_circle(vid1.size, MASK_1_PNG)

        ''' FOR FIRST VIDEO '''
        # load mask image
        MASK_1 = ImageClip(MASK_1_PNG, transparent=True, ismask=True)
        MASK_1 = MASK_1.set_duration(vid1.duration) # set duration
        MASK_1 = MASK_1.set_fps(15) # set fps

        # convert mask img to video clip
        MASK_1 = CompositeVideoClip([MASK_1], bg_color=(0), size=vid1.size, ismask=True)
        # set mask to video
        vid1.mask = MASK_1 
        vid1 = concatenate_videoclips([vid1], method='compose') # combine with video

        ''' ADD IMAGE TO THE VIDEO '''
        image_clip1 = ImageClip(PIC1, duration=vid1.duration)
        result1 = CompositeVideoClip([image_clip1, vid1.set_position(("right", "bottom"))], use_bgclip=True)

        # add black area to left and right side
        def resize_vids_if_not_same_size():
            # add black area to left and right side
            m = abs(image_clip1.w - vid1.w) 

            if m % 2 == 1: 
                l, r = (m // 2, m // 2 + 1)
            else: 
                l, r = (m // 2, m // 2)

            result1 = result1.margin(left=l, right=r)

        print(result1.size)

        # final video
        final = result1

        final.write_videofile(FINAL_VID)

    def upload_video_to_mux(video_path, upload_url):
        try:
            data = open(FINAL_VID, 'rb')
            print('the upload url is' + str(upload_url))
            req = requests.put(url=upload_url, data=data)
            print(req)
            print('Uploaded the video to the MUX API!')

        except ApiException as e:
            print("Exception when calling AssetsApi->list_assets: %s\n" % e)

    def download_pic(url, file_name):
        print('downloading picture ' + url)
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, "w+b") as file:
                response = requests.get(url)
                file.write(response.content)
        else: 
            raise Exception('Failed downloading the video')

    def download_loom(videoLink, vid_name):
        print("vid link" +videoLink)
        print(vid_name)
        linkList = re.split("/", videoLink)

        videoId = linkList[-1]

        transcodedURL = "https://www.loom.com/api/campaigns/sessions/" + \
        videoId + "/transcoded-url"

        postRequest = requests.post(transcodedURL)

        deserialize = json.loads(postRequest.text)

        videoURL = "https://media.istockphoto.com/id/1430945266/video/nature-sunrise-mountain-trees-and-aerial-view-of-the-forrest-and-beautiful-scenic-in-the.mp4?s=mp4-640x640-is&k=20&c=gosr3IBQvn0OV-RLrkaWEzLBeCulQ4QZILC4M5B9DcY=" #deserialize['url']

        print("Downloading...")

        downloadVideo = requests.get(videoURL)

        with open(vid_name, 'wb') as f: 
                for chunk in downloadVideo.iter_content(chunk_size=255):
                    if chunk:
                        f.write(chunk)

        print('successfully downloaded loom video')

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            VID1 = "try.mp4" #os.path.join(tmpdir, 'vid1.mp4')
            PIC1 = "image.png" #os.path.join(tmpdir, 'image.png')
            MASK_1_PNG = "image.png" #os.path.join(tmpdir, 'mask1.png')
            FINAL_VID = os.path.join(tmpdir, 'final.mp4')

            video_source = 'try.mp4'
            if video_source == 'website_video':
                website_screenshot_url = website_screenshot_url  # replace with actual value
                download_pic(website_screenshot_url, PIC1)
            else:
                linkedin_screenshot_url = 'https://media.istockphoto.com/id/1468192804/photo/concept-of-generating-photo-realistic-image-by-ai-software.jpg?s=1024x1024&w=is&k=20&c=God714gBMXXOvPsYnWUWFo6h_SHJTk_Tpa4RT5oDD2Q='  # replace with actual value
                download_pic(linkedin_screenshot_url, PIC1)

            script1_url = 'https://app.vidscale.io/api/errored_video/'  # replace with actual value
            download_loom(script1_url, VID1)

            generate_video()
            upload_url = 'https://app.vidscale.io/api/errored_video/'  # replace with actual value
            upload_video_to_mux(FINAL_VID, upload_url)
    except Exception as e:
        print("errored video and the reason of exceptions is:")
        print(str(e))
        upload_id = 'id'  # replace with actual value
        requests.post("https://app.vidscale.io/api/errored_video/" + str(upload_id))

    return {
        'statusCode': 200,
    }


if __name__ == "__main__":
    VIDEO_SOURCE = 'https://media.istockphoto.com/id/1430945266/video/nature-sunrise-mountain-trees-and-aerial-view-of-the-forrest-and-beautiful-scenic-in-the.mp4?s=mp4-640x640-is&k=20&c=gosr3IBQvn0OV-RLrkaWEzLBeCulQ4QZILC4M5B9DcY='
    WEBSITE_SCREENSHOT_URL = 'https://media.istockphoto.com/id/1468192804/photo/concept-of-generating-photo-realistic-image-by-ai-software.jpg?s=1024x1024&w=is&k=20&c=God714gBMXXOvPsYnWUWFo6h_SHJTk_Tpa4RT5oDD2Q='
    LINKEDIN_SCREENSHOT_URL = 'https://media.istockphoto.com/id/1468192804/photo/concept-of-generating-photo-realistic-image-by-ai-software.jpg?s=1024x1024&w=is&k=20&c=God714gBMXXOvPsYnWUWFo6h_SHJTk_Tpa4RT5oDD2Q='
    SCRIPT1_URL = 'https://media.istockphoto.com/id/1430945266/video/nature-sunrise-mountain-trees-and-aerial-view-of-the-forrest-and-beautiful-scenic-in-the.mp4?s=mp4-640x640-is&k=20&c=gosr3IBQvn0OV-RLrkaWEzLBeCulQ4QZILC4M5B9DcY='
    UPLOAD_URL = 'https://api.mux.com/video/v1/uploads'

    main(VIDEO_SOURCE, WEBSITE_SCREENSHOT_URL, LINKEDIN_SCREENSHOT_URL, SCRIPT1_URL, UPLOAD_URL)