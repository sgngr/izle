"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
Application settings module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import os
from lxml import etree


class Settings():
    def __init__(self):
        self.file_settings = "settings.xml"
        self.last_channel_list = "channels.xml"
        self.use_legacy_vo = False
        self.page_load_timeout = 2
        self.capture_duration = 10
        self.screen_padding = [10, 10, 10, 10]
        if os.path.exists(self.file_settings):
            self.read(self.file_settings)
        else:
            self.write(self.file_settings)

    def read(self, file):
        tree = etree.parse(file)
        root = tree.getroot()
        self.last_channel_list = root.find('last_channel_list').text
        vo = int(root.find('use_legacy_vo').text)
        if vo == 0:
            self.use_legacy_vo = False
        else:
            self.use_legacy_vo = True
        self.page_load_timeout = int(root.find('page_load_timeout').text)
        self.capture_duration = int(root.find('capture_duration').text)
        self.screen_padding[0] = int(root.find('screen_padding_left').text)
        self.screen_padding[1] = int(root.find('screen_padding_top').text)
        self.screen_padding[2] = int(root.find('screen_padding_right').text)
        self.screen_padding[3] = int(root.find('screen_padding_bottom').text)

    def write(self, file):
        root = etree.Element("settings")
        etree.SubElement(root, "last_channel_list").text = "{}".format(
            self.last_channel_list)
        print(">>>>>>>>>>>>>>>>>>", self.use_legacy_vo )
        if self.use_legacy_vo:
            etree.SubElement(root, "use_legacy_vo").text = "1"
        else:
            etree.SubElement(root, "use_legacy_vo").text = "0"
        etree.SubElement(root, "page_load_timeout").text = "{}".format(
            self.page_load_timeout)
        etree.SubElement(root, "capture_duration").text = "{}".format(
            self.capture_duration)
        etree.SubElement(root, "screen_padding_left").text = "{}".format(
            self.screen_padding[0])
        etree.SubElement(root, "screen_padding_top").text = "{}".format(
            self.screen_padding[1])
        etree.SubElement(root, "screen_padding_right").text = "{}".format(
            self.screen_padding[2])
        etree.SubElement(root, "screen_padding_bottom").text = "{}".format(
            self.screen_padding[3])
        tree = etree.ElementTree(root)
        tree.write(file, encoding="utf-8",
                   xml_declaration=True, pretty_print=True)

    def print(self):
        print("Application Settings:")
        print(" Last used channel list:", self.last_channel_list)
        print(" Use legacy video output driver:", self.use_legacy_vo)
        print(" Page load timeout:", self.page_load_timeout)
        print(" Network log capture duration:", self.capture_duration)

if __name__ == '__main__':
    settings = Settings()
    settings.print()
    if settings.use_legacy_vo:
        print("* Use legacy video output driver")
    else:
        print("* Don't use legacy video output driver")
    settings.write(settings.file_settings)
