"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
Channels module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import os
from copy import deepcopy

# -----------------------

from lxml import etree as ET

from yt_watchlinks import WatchLink

from hls import get_m3u8_urls
from yt_watchlinks import get_yt_watchlinks, get_yt_playlist


class Channel():
    def __init__(self):
        self.channel_type = 0
        # 0: Basic
        # 1: Live stream
        # 2: Youtube watch
        # 3: Youtube playlist
        self.name = None
        self.video = None
        self.web = None
        #  0: first
        # -1: last
        self.first_last = -1
        self.max_watchlink = 10
        self.watchlinks = list()
        self.iWatchlink = 0

    def m3u8_url_update(self, load_timeout, capture_duration ):
        if self.web is not None:
            print("Updating channel video URL ...")
            print("Connecting to {}".format(self.web))
            result, url_list = get_m3u8_urls(self.web,
                                             load_timeout, capture_duration)
            if len(url_list) > 0:
                print("{} video URL found".format(len(url_list)))
                print(url_list)
                url = url_list[self.first_last]
                if self.first_last == 0:
                    print("First m3u8 video URL selected")
                else:
                    print("Last m3u8 video URL selected")
                print("New video URL:", url)
                self.video = url
            else:
                print("No video URL found!")

    def watch_links_update(self, timeout):
        if self.web is not None:
            print("Updating watchlinks ...\nConnecting to {}".format(self.web))
            timeout = 30
            print("Channel type:",self.channel_type)
            if self.channel_type == 3:
                result, watchlinks = get_yt_playlist(self.web, timeout,
                                                     self.max_watchlink)
            else:
                result, watchlinks = get_yt_watchlinks(self.web, timeout,
                                                       self.max_watchlink)
            print("Watchlinks updated.")
            for watchlink in watchlinks:
                print(f"  - {watchlink.title} ({watchlink.href})")
            self.watchlinks = deepcopy(watchlinks)
            self.iWatchlink = 0


class Channels():
    def __init__(self, file_name="channels.xml"):
        self.file_channel_list = file_name
        self.iChannel = 0
        self.nChannel = 0
        self.channels = []
        self.read()

    def read(self):
        isFile = os.path.isfile(self.file_channel_list)
        if isFile:
            tree = ET.parse(self.file_channel_list)
            root = tree.getroot()
            element = root.find('playing')
            if element is not None:
                self.iChannel = int(element.text)
            self.channels = []
            for channel in root.findall('channel'):
                self.channels.append(Channel())
                self.nChannel = len(self.channels)

                element = channel.find('name')
                if element is not None:
                    self.channels[self.nChannel-1].name = element.text

                element = channel.find('web')
                if element is not None:
                    self.channels[self.nChannel-1].web = element.text

                element = channel.find('video')
                if element is not None:
                    self.channels[self.nChannel-1].video = element.text

                element = channel.find('channel_type')
                if element is not None:
                    self.channels[self.nChannel -
                                  1].channel_type = int(element.text)

                element = channel.find('first_last')
                if element is not None:
                    self.channels[self.nChannel -
                                  1].first_last = int(element.text)

                element = channel.find('max_watchlink')
                if element is not None:
                    self.channels[self.nChannel -
                                  1].max_watchlink = int(element.text)

                element = channel.find('i_watchlink')
                if element is not None:
                    self.channels[self.nChannel -
                                  1].iWatchlink = int(element.text)

                for watchlink in channel.findall('watchlink'):
                    element = watchlink.find('title')
                    if element is not None:
                        title = element.text
                    else:
                        title = None
                    element = watchlink.find('href')
                    if element is not None:
                        href = element.text
                    else:
                        href = None

                    self.channels[self.nChannel - 1].watchlinks.append(
                        WatchLink(title=title, href=href))

        else:
            newChannel = Channel()
            newChannel.name = "Unknown Channel"
            self.channels = []
            self.channels.append(newChannel)
            self.nChannel = 1
            self.iChannel = 0

    def write(self, file_channel_list):
        root = ET.Element("channelList")
        playing = ET.SubElement(root, "playing")
        playing.text = "{}".format(self.iChannel)
        for i in range(self.nChannel):
            Channel = ET.SubElement(root, "channel")

            ET.SubElement(Channel, "channel_type").text = "{f}".format(
                f=self.channels[i].channel_type)

            ET.SubElement(Channel, "name").text = "{n}".format(
                n=self.channels[i].name)

            if self.channels[i].video is not None:
                ET.SubElement(Channel, "video").text = "{u}".format(
                    u=self.channels[i].video)

            if self.channels[i].web is not None:
                ET.SubElement(Channel, "web").text = "{w}".format(
                    w=self.channels[i].web)

            if self.channels[i].channel_type == 1:
                ET.SubElement(Channel, "first_last").text = "{fl}".format(
                    fl=self.channels[i].first_last)

            if self.channels[i].channel_type in (2, 3) :
                ET.SubElement(Channel, "max_watchlink").text = "{m}".format(
                    m=self.channels[i].max_watchlink)
                ET.SubElement(Channel, "i_watchlink").text = "{i}".format(
                    i=self.channels[i].iWatchlink)

            if self.channels[i].channel_type in (2, 3):
                for j in range(len(self.channels[i].watchlinks)):
                    Watchlink = ET.SubElement(Channel, "watchlink")
                    ET.SubElement(Watchlink, "title").text = "{t}".format(
                        t=self.channels[i].watchlinks[j].title)
                    ET.SubElement(Watchlink, "href").text = "{t}".format(
                        t=self.channels[i].watchlinks[j].href)

        tree = ET.ElementTree(root)
        tree.write(file_channel_list, encoding="utf-8",
                   xml_declaration=True, pretty_print=True)

    def add_channel(self, channel):
        newChannel = Channel()
        newChannel.channel_type = channel.channel_type
        newChannel.name = channel.name
        newChannel.video = channel.video
        newChannel.web = channel.web
        newChannel.first_last = channel.first_last
        newChannel.max_watchlink = channel.max_watchlink
        newChannel.watchlinks = channel.watchlinks
        newChannel.iWatchlink = channel.iWatchlink
        self.channels.append(newChannel)
        self.nChannel = self.nChannel+1
        self.iChannel = self.nChannel-1
        self.print()

    def remove_channel(self, index):
        if self.nChannel > 1:
            del self.channels[index]
            if index == self.nChannel-1:
                self.iChannel = self.iChannel-1
            self.nChannel = len(self.channels)
        self.print()

    def update_channel(self, index, channel):
        self.channels[index].channel_type = channel.channel_type
        self.channels[index].name = channel.name
        self.channels[index].video = channel.video
        self.channels[index].web = channel.web
        self.channels[index].first_last = channel.first_last
        self.channels[index].max_watchlink = channel.max_watchlink
        self.channels[index].watchlinks = channel.watchlinks
        self.channels[index].iWatchlink = channel.iWatchlink
        self.print()

    def print(self):
        print("Channels:")
        print(' # of Channel: {}'.format(self.nChannel))
        for i in range(self.nChannel):
            channel = self.channels[i]
            if channel.channel_type == 0:
                print(" {i:2d} > {n} : {u} ".format(
                    i=i, u=channel.video, n=channel.name))
            if channel.channel_type == 1:
                print(" {i:2d} > {n} : {u} : {w}".format(
                    i=i, n=channel.name,  u=channel.video, w=channel.web))
            if channel.channel_type in (2, 3):
                print(" {i:2d} > {n} : {w}".format(
                    i=i, n=channel.name, w=channel.web))
                print("      # of Watchlinks", len(channel.watchlinks))
                for j in range(len(channel.watchlinks)):
                    print("        {j:2d} > {t} | {h}".format(
                        j=j, t=channel.watchlinks[j].title,
                        h=channel.watchlinks[j].href))

        print(" Selected channel:", self.iChannel)


if __name__ == '__main__':
    # channels = Channels()
    channels = Channels('channels.xml')
    channels.print()
    channels.write('test.xml')  # to save as
