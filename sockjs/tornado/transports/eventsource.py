# -*- coding: utf-8 -*-
"""
    sockjs.tornado.transports.eventsource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    EventSource transport implementation.
"""

from tornado.web import asynchronous

from sockjs.tornado.transports import pollingbase


class EventSourceTransport(pollingbase.PollingTransportBase):
    @asynchronous
    def get(self, session_id):
        # Start response
        self.preflight()
        self.handle_session_cookie()
        self.disable_cache()

        self.set_header('Content-Type', 'text/event-stream; charset=UTF-8')
        self.write('\r\n')
        self.flush()

        if not self._attach_session(session_id):
            self.finish()
            return

        if not self.detached:
            self.session.flush()

    def send_pack(self, message):
        try:
            self.write('data: %s\r\n\r\n' % message)
            self.flush()
        except IOError:
            # If connection dropped, make sure we close offending session instead
            # of propagating error all way up.
            self._detach()
            self.session.delayed_close()

        # TODO: Close connection based on amount of data transferred
