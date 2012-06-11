#!/usr/bin/env python

# Copyright (c) 2008 Carnegie Mellon University.
#
# You may modify and redistribute this file under the same terms as
# the CMU Sphinx system.  See
# http://cmusphinx.sourceforge.net/html/LICENSE for more information.

import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

from MythTV import Frontend

class DemoApp(object):
    """GStreamer/PocketSphinx Demo Application"""
    def __init__(self):
        """Initialize a DemoApp object"""
        self.init_gst()
        self.init_tivo()

    def init_gst(self):
        """Initialize the speech components"""

        self.pipeline = gst.Pipeline('player')

        source = gst.element_factory_make('pulsesrc')

        convert = gst.element_factory_make('audioconvert')

        resample = gst.element_factory_make('audioresample')

        vader = gst.element_factory_make('vader')
        vader.set_property('name', 'vad')
        vader.set_property('auto-threshold', 'true')

        sphinx = gst.element_factory_make('pocketsphinx')
        sphinx.set_property('name', 'asr')

        sink = gst.element_factory_make('fakesink')

        self.pipeline.add(source, convert, resample, vader, sphinx, sink)
        gst.element_link_many(source, convert, resample, vader, sphinx, sink)

        asr = self.pipeline.get_by_name('asr')
        asr.connect('partial_result', self.asr_partial_result)
        asr.connect('result', self.asr_result)
        asr.set_property('configured', True)

        asr.set_property('lm', 'language_model.lm')
        asr.set_property('dict', 'dictionary.dic')

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::application', self.application_message)

        self.pipeline.set_state(gst.STATE_PLAYING)

    def init_tivo(self):
        """Initialize the MythTV Frontend connection"""
        self.frontend = Frontend('localhost', '6546')

    def asr_partial_result(self, asr, text, uttid):
        """Forward partial result signals on the bus to the main thread."""
        struct = gst.Structure('partial_result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def asr_result(self, asr, text, uttid):
        """Forward result signals on the bus to the main thread."""
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def application_message(self, bus, msg):
        """Receive application messages from the bus."""
        msgtype = msg.structure.get_name()
        if msgtype == 'result':
            res = msg.structure['hyp']
            if res: print res
            self.dispatch_command(res)

    def dispatch_command(self, command):
        play_commands = {
            "TIVO PLAY": "speed normal",
            "TIVO PAUSE": "speed pause",
            "TIVO SKIP": "seek forward",
            "TIVO SKIP FORWARD": "seek forward",
            "TIVO SKIP BACK": "seek backward",
        }

        key_commands = {
            "TIVO STOP": "escape",
            "TIVO ESCAPE": "escape",
            "TIVO PAGE UP": "pageup",
            "TIVO PAGE DOWN": "pagedown",
            "TIVO UP": "up",
            "TIVO DOWN": "down",
            "TIVO ALTO": "up",
            "TIVO BAHO": "down",
            "TIVO LEFT": "left",
            "TIVO RIGHT": "right",
            "TIVO ENTER": "enter",
            "TIVO SELECT": "enter",
            "TIVO OK": "enter",
        }

        jump_commands = {
            "TIVO STOP": "playbackbox",
        }

        if command in play_commands.keys():
            print "** received %s, sending 'play %s'" % (command, play_commands[command])
            self.frontend.sendPlay(play_commands[command])
        elif command in key_commands.keys():
            print "** received %s, sending 'key %s'" % (command, key_commands[command])
            try:
                self.frontend.sendKey(key_commands[command])
            except AttributeError:
                self.frontend.key[key_commands[command]]
        elif command in jump_commands.keys():
            print "** received %s, sending 'jump %s'" % (command, jump_commands[command])
            try:
                self.frontend.sendJump(jump_commands[command])
            except AttributeError:
                self.frontend.jump[jump_commands[command]]

        elif command == "TIVO PLAY DAILY SHOW":
            print "PLAYing latest daily show"
            daily_shows = [x for x in self.frontend.sendQuery('recordings').split('\r\n') if x.find('Daily Show') >= 0]
            latest_ds = sorted(daily_shows)[-1].split()
            self.frontend.sendPlay('program %s %s' % (latest_ds[0], latest_ds[1]))
        elif command == "TIVO PLAY COLBERT":
            print "PLAYing latest colbert"
            daily_shows = [x for x in self.frontend.sendQuery('recordings').split('\r\n') if x.find('Colbert Report') >= 0]
            latest_ds = sorted(daily_shows)[-1].split()
            self.frontend.sendPlay('program %s %s' % (latest_ds[0], latest_ds[1]))


app = DemoApp()
loop = gobject.MainLoop()
gobject.threads_init()
loop.run()
