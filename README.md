# izle
**mpv GUI for watching live streams and YouTube's channels**

---

![ScreenShot](https://github.com/sgngr/izle/blob/main/izle-Screenshot.png) 

izle is for watching live streams and YouTube's channels. It works on Linux and Windows operating system.
izle supports three types of video channel:

- Basic channel: Any video URL supported by mpv.

- HTTP live stream channel: m3u8 playlists are retrieved from channel's website.

- YouTube's channel: Watchlinks are retrieved from channel's website.


## Requirements

- mpv Library

    Linux OS: Install corresponding software package using package manager of the distribution. 
    
    Windows OS: Get a copy of the library libmpv-2.dll from mpv development packages (mpv-dev-...) which can be downloaded from
    
    `https://github.com/shinchiro/mpv-winbuild-cmake/releases`

    or
    
    `https://github.com/zhongfly/mpv-winbuild/releases`
    

- Python >= 3.9
   
    It is recommended that using a virtual environment and installing the required modules with the command
   
    `pip install -r requirements.txt`

    
- Google Chrome Browser

    It is required by python module `selenium`.
    
    
## Issues

- If window system use Wayland decompositor, video output may not be embedded. In this case, set the use legacy video output driver option in application settings.

- Fullscreen mode may not work properly on GNOME desktop environments.

- m3u8 playlists of live stream channels can not be captured for some sites.
