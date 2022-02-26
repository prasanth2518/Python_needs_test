import moviepy.editor as mp
import pafy
import re
import requests
import traceback
import urllib.request
import youtube_dl
from pytube import YouTube


class YouTube_Downloader:
    def __init__(self, url: list, path: str = None):
        self.path = path
        self.url = url

    def downnload_video(self):
        try:
            for url in self.url:
                video = YouTube(url)
                stream = video.streams.get_highest_resolution()
                # stream = video.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first()
                print("download_started", stream.default_filename)
                stream.download(output_path=self.path)
                print("video_download", stream.default_filename)
        except BaseException as err:
            print(err)
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url)
            print("done_with_youtube-dl")
        except BrokenPipeError as e:
            tb = traceback.format_exc()
            print(str(e) + " tb  " + str(tb))

    def download_audio(self):

        try:
            for link in self.url:
                video = pafy.new(link)
                audio_streams = video.audiostreams
                # list of audiostreams
                for stream_qquality in audio_streams:
                    print("bitrate:%s,ext: %s,size:%0.2fMb" % (
                        stream_qquality.bitrate, stream_qquality.extension,
                        stream_qquality.get_filesize() / 1024 / 1024))
                # download audio
                audio_streams[2].download(filepath=self.path, )
                print("audio_download_complete")
        except Exception as e:
            print(e)


class Instagram_Downloader:

    def __init__(self, url_list: list, video_paths: list = None, path: str = None):
        self.urls = url_list
        self.path = path
        self.video_paths = video_paths

    def get_response(self, url):
        r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        while r.status_code != 200:
            r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        return r.text

    def prepare_urls(self, matches):
        return list({match.replace("\\u0026", "&") for match in matches})

    def video_downloader(self):
        try:

            for url in self.urls:
                saved_file_name = url.split("/")[-2]
                response = self.get_response(url)
                vid_matches = re.findall('"video_url":"([^"]+)"', response)
                vid_urls = self.prepare_urls(vid_matches)
                if vid_urls:
                    print("detected videos:\n{0}".format("\n".join(vid_urls)))
                    for ind, vid_url in enumerate(vid_urls):
                        file_name = saved_file_name + '.mp4'
                        if self.path:
                            file_name = self.path + file_name
                        urllib.request.urlretrieve(vid_url, file_name)
                        print(saved_file_name, ".mp4 downloaded")

                else:
                    print("could not recognize media in the provided url")
        except Exception as e:
            print(str(e))

    def image_downloader(self):
        try:
            for url in self.urls:
                saved_file_name = url.split("/")[-2]
                response = self.get_response(url)
                picture_matches = re.findall('"display_url":"([^"]+)"', response)
                picture_urls = self.prepare_urls(picture_matches)
                if picture_urls:
                    print("detected_pictures:\n{0}".format("\n".join(picture_urls)))
                    for ind, picurl in enumerate(picture_urls):
                        file_name = saved_file_name + '.jpg'
                        if self.path:
                            file_name = self.path + file_name
                        urllib.request.urlretrieve(picurl, file_name)
                        print(saved_file_name, ".jpg downloaded")
                else:
                    print("could not recognize media in the provided url")

        except Exception as e:
            print(str(e))

    def mp3_converter(self):
        try:
            if self.video_paths:
                for video_path in self.video_paths:
                    saved_filename = video_path.split("/")[-1].split(".")[0]
                    my_clip = mp.VideoFileClip(video_path)
                    file_name = saved_filename + ".mp3"
                    if self.path:
                        file_name = self.path + file_name
                    my_clip.audio.write_audiofile(file_name)
                    print(saved_filename, ".mp3 downloaded")
            else:
                print("No video_paths received")
        except Exception as e:
            print(e)

# y_url = ['https://www.youtube.com/watch?v=62hPkQrhW-M']
# i_url = ['https://www.instagram.com/p/CPnG-Yxj4Zv/']
# path = '/home/prashanth/Downloads/movies/videos/'
# id = Instagram_Downloader(i_url, path= path)
# id.video_downloader()
# yt = YouTube_Downloader(y_url,path=path)
# yt.downnload_video()
