import requests
from kafka import KafkaConsumer
import time
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')


class EventNode(object):

    def __init__(self, obj_data):
        self.prev = None
        self.next = None
        self.object_data = obj_data
        

class ListIterator():
    def __init__(self, l):
        self.list = l
        self.cur = l.head

    def __iter__(self):
        return self

    def next(self):
        if self.cur.next == l.tail:
            raise StopIteration()
        else:
            self.cur = self.cur.next
            return self.cur.object_data


class EventList():
    def __init__(self):
        self.head = EventNode(0, None)
        self.tail = EventNode(0, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.count = 0

    def __len__(self):
        return self.count

    def __iter__(self):
        return ListIterator(self)
    
    def insertBefore(self, node, obj_data):
        newEventNode = EventNode(obj_data)
        node.prev.next = newEventNode
        newEventNode.prev = node.prev
        newEventNode.next = node
        node.prev = newEventNode
        self.count += 1
        return newEventNode

    def insertAfter(self, node, obj_data):
        return self.insertBefore(node.next, obj_data)

    def append(self, obj_data):
        return self.insertBefore(self.tail, obj_data)

    def addFirst(self, obj_data):
        return self.insertAfter(self.head, obj_data)

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.count -= 1

    def remove_last(self):
        self.remove(self.tail.prev)
    
    def find(self, obj_id):
        cur = self.head.next
        while cur and cur.object_data.obj_id != obj_id:
            cur = cur.next
        return cur

def gen_obj_list(msg):
    obj_list = []
    cur_ts = time.time()
    for i in range(len(msg['objects'])):
        obj_dict = {}
        obj_dict['ts'] = cur_ts
        obj_dict['sensorId'] = msg['sensorId']
        obj_meta = msg['objects'][i].split('|')
        obj_dict['obj_id'] = obj_meta[0]
        obj_dict['bbox'] = [float(x) for x in obj_meta[1:5]]
        obj_dict['event'] = obj_meta[-1]
        obj_list.append(obj_dict)
    return obj_list

def sound_the_alarm():
    pass


interval = int(config['params']['interval'])
consumer = KafkaConsumer(bootstrap_servers= [str(config['kafka']['host'])], 
                        value_deserializer=lambda m: json.loads(m.decode('ascii')), auto_offset_reset='latest')
consumer.subscribe(topics = [str(config['kafka']['topic'])])

event_list = EventList()

for msg in consumer:
    current_time = time.time()
    last_ts = current_time - interval

    # add the newly received event objects to the event list.
    detected_objs = gen_obj_list(msg.value)
    for i in range(len(detected_objs)):
        event_obj = Event(detected_objs[i])
        exist_obj = event_list.find(detected_objs[i]['obj_id'])  # check if the same object existed already.
        if not exist_obj:
            event_list.addFirst(event_obj)  # if not, add it to the top of the event link list.
        else:
            # if the same event object existed for a period of time, we should sound the alarm.
            if event_obj.object_data['ts'] - exist_obj.object_data['ts'] > interval:
                sound_the_alarm()
                
    # remove the timeout event objects.
    while True:
        if event_list.tail.prev.object_data['ts'] < last_ts:
            event_list.remove_last()
        else:
            break
    

