import xmpp, json, os, sys, time
import paho.mqtt.client as mqtt

def on_connect(self, mosq, obj, rc):
	mqttc.subscribe(config['mqtt']['topic'], 0)

def send(topic='', message=''):
	if (len(topic) > 0) & (len(message) > 0):
		if not(topic in topics):
			topics.append(topic)
		msg = xmpp.protocol.Message(body=json.dumps([topic, message]))
	else:
		msg = xmpp.protocol.Message(body=json.dumps([]))
	msg.setTo(config['xmpp']['muc']['room'] + '@' + config['xmpp']['muc']['server'])
	msg.setType('groupchat')
	try:
		cl.send(msg)
		cl.Process(5)
	except:
		pass

def on_message(mosq, obj, msg):
	data = json.loads(msg.payload.decode('utf8'))
	topic = str(msg.topic)
	send(topic, data)

def on_xmpp(conn, msg):
	body = str(msg.getBody())
	muc_id = config['xmpp']['muc']['room'] + '@' + config['xmpp']['muc']['server'] + '/' + config['xmpp']['muc']['handle']
	msg_from = str(msg.getFrom())
	if muc_id != msg_from:

		try:
			data = json.loads(body)
		except:
			data = []
		if(isinstance(data, (list))):
			if len(data) == 2:
				topic = data[0]
				data = data[1]
				mqttc.publish(topic, json.dumps(data))

topics = []

base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = os.path.join(base_path, 'config.json')
with open(config_file, 'r') as fp:
	config = json.loads('\n'.join(fp.readlines()))

jid_id = config['xmpp']['username'] + '@' + config['xmpp']['host']
muc_id = config['xmpp']['muc']['room'] + '@' + config['xmpp']['muc']['server'] + '/' + config['xmpp']['muc']['handle']
if 'resource' in config['xmpp']:
	if len(config['xmpp']['resource']) > 0:
		jid_id = jid_id + '/' + config['xmpp']['resource']

while True:

	jid=xmpp.protocol.JID(jid_id)
	cl=xmpp.Client(jid.getDomain(),debug=['always'])
	cl.connect()
	cl.auth(jid.getNode(), config['xmpp']['password'], resource=jid.getResource())
	presence = xmpp.protocol.Presence(to=muc_id)
	presence.setTag('x', namespace=xmpp.protocol.NS_MUC).setTagData('password', config['xmpp']['muc']['password'])
	cl.send(presence)
	cl.Process(5)

	cl.RegisterHandler('message', on_xmpp)
	cl.Process(5)

	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	mqttc.on_message = on_message
	mqttc.connect(config['mqtt']['host'], config['mqtt']['port'], config['mqtt']['timeout'])
	mqttc.loop_start()

	while True:

		try:
			cl.Process(config['xmpp']['timeout'])
		except:
			break

		if not(cl.isConnected()):
			break

	try:
		mqttc.loop_stop()
	except:
		pass
	try:
		mqttc.disconnect()
	except:
		pass
	try:
		cl.disconnect()
	except:
		pass

	print("ERROR: program      close Program terminated. Waiting to reconnect / Press Ctrl-C to cancel")
	time.sleep(5) # Wait before attempting reconnect
