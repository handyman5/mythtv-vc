# MythTV Voice Control

This script listens to a small set of voice commands in US English and translates them into instructions for a MythTV frontend. The intention is to emulate the voice control capabilities of an Xbox360 with a Kinect (e.g., you can say "Xbox pause" and it will cause the currently playing video to pause).

The script is fully functional; however, I don't have a good handle on providing echo cancellation, so a) the script will pick up audio from the playing television show and occasionally consider it to be a valid command, and b) it's almost impossible to issue voice commands while a show is playing or when there's other substantial background noise. Suggestions and pull requests would be most welcome. I'm testing the [webrtc echo cancelling](http://cgit.freedesktop.org/pulseaudio/webrtc-audio-processing/tree/README) functionality Pulseaudio 2.0 now, so I'll update here if I can figure something out.

**Note**: I've been using the voice trigger "TiVo"; this is my own nickname for my MythTV HTPC, and used without permission of the [TiVo](http://www.tivo.com/) corporation.

## Requirements
* Linux
* [Pocketsphinx](http://cmusphinx.sourceforge.net/wiki/download/) 0.5+
* Gstreamer 0.10+
* [MythTV](http://www.mythtv.org/) 0.24+

## Tested
* Ubuntu 11.10, 12.04
* MythTV 0.24, 0.25

## Links
* This code started as the demo code from [Using PocketSphinx with GStreamer and Python](http://cmusphinx.sourceforge.net/wiki/gstreamer).
* Makes use of the [MythTV Frontend control socket](http://www.mythtv.org/wiki/Frontend_control_socket) and [MythTV Python bindings](http://www.mythtv.org/wiki/Python_bindings#Frontend.28host.2C_port.29).
 * Also useful: [mythremctl.py](http://www.mythtv.org/wiki/Mythremctl.py).
* Language model and dictionary generated using the CMUSphinx online tool [lmtool](http://www.speech.cs.cmu.edu/tools/lmtool-new.html).
 * Using the file `sentence_corpus.txt` from this repo.
 * [Other sphinx language model resources](http://www.speech.cs.cmu.edu/sphinx/models/#lm).

## License
The original link for the LICENSE file of the demo code I used [is 404](http://cmusphinx.sourceforge.net/html/LICENSE), but the [Internet Archive has a copy](http://web.archive.org/web/20090626063031/http://cmusphinx.sourceforge.net/html/LICENSE). This project adheres to that license.
