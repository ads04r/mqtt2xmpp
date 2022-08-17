mqtt2xmpp
=========

MQTT is great. So is XMPP. Sometimes, as in my case, you have
two networks, each with their own MQTT server and each behind
some kind of firewall or NAT, which can't see each other. But
you have a chat room on an XMPP server that is accessible by
both networks. So you simply have a background script running
on your MQTT server just repeating anything on a particular
topic (or topics) into the XMPP chat room, and the same script
at the other end listening to the chat room and repeating any
messages to its local MQTT server on the appropriate topic.
That's what this script does.

Installing
----------
Simply clone this repo to a directory on a machine that can
see both an MQTT broker and an XMPP server. Optionally
create a python virtual environment, and install the
requirements from the requirements.txt file using pip.

Configuration
-------------
The file config.json.dist needs to be renamed config.json,
and filled in with all the appropriate connection information.
This should be straightforward and if it isn't, then you
probably don't really need this script.

Testing
-------
You can just run the script for a bit in the foreground to
make sure everything works. You should see the script join
the chat room in the XMPP server, and once messages start
appearing on the MQTT topic, these should get repeated in
the chat. The messages are sent to the chat as JSON lists of
length 2: [topic, payload]. You can 'fake' one of these by
typing something into the chat such as ["testing", "testing"]
and check to ensure it gets repeated to the MQTT broker.
