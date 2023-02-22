from PIL import Image
from ffmpy import FFmpeg
import cv2
import youtube_dl
import os


def get_meta(opts):
    # Getting meta data of the video
    url = input("Url: ")

    with youtube_dl.YoutubeDL(opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        return meta


def get_best_video_url(metadata):
    # Selecting the best video
    formats_length = len(meta["formats"])
    best_resolution_id = formats_length - 2
    print(meta["formats"][best_resolution_id])
    return meta["formats"][best_resolution_id]["url"]


def set_ffmpeg(video):
    # Defining inputs and outputs
    inputs = ffmpeg_inputs(video)
    outputs = ffmpeg_outputs()

    f = FFmpeg(
        inputs={inputs[0] : inputs[1]},
        outputs={outputs[0] : outputs[1]}
    )
    return f


def ffmpeg_inputs(video):
    # Set up ffmpeg inputs by getting the video start
    start = input("When does the sheet music start? ")
    first = video
    second = "-ss "+start
    inputs = [first, second]
    return inputs


def ffmpeg_outputs():
    # Set up ffmpeg outputs by getting how often does the sheet music change
    change = input("How often do the sheets change(in seconds)? ")
    first = "imgs\img%02d.jpeg"
    second = "-vf fps=1/"+change
    outputs = [first, second]
    return outputs


def put_it_together():
    img_count = len(os.listdir(r"C:\Users\Walter\PycharmProjects\sheets_getter\imgs"))
    for img in range(1, img_count, 2):
        number = f"{img:02}"
        imgs = img + 1
        number_more = f"{imgs:02}"

        img = cv2.imread(f"C:/Users/Walter/PycharmProjects/sheets_getter/imgs/img"+number+".jpeg")
        img1 = cv2.imread(f"C:/Users/Walter/PycharmProjects/sheets_getter/imgs/img"+number_more+".jpeg")
        vertical = cv2.vconcat([img, img1])

        cv2.imwrite("sheets"+number+".jpg", vertical)

        os.remove(rf'C:\Users\Walter\PycharmProjects\sheets_getter\imgs\img'+number+'.jpeg')
        os.remove(rf'C:\Users\Walter\PycharmProjects\sheets_getter\imgs\img'+number_more+'.jpeg')


if __name__ == '__main__':
    print("Sheet music getter")

    # Getting the youtube video url
    opts = {
        "format": "best[ext=mp4]",
        "outtmpl": "video.%(ext)s"
    }
    meta = get_meta(opts)

    # Selecting the best video quality
    best_resolution = get_best_video_url(meta)

    # Running ffmpeg and getting imgs of the sheet music
    ff = set_ffmpeg(best_resolution)
    ff.run()

    # The rest
    put_it_together()
