# -*- coding: utf-8 -*-
# reader-writer problem, producer consumer
#   ���Ӥ� �@��producer�@��consumer�A�h��reader�h��writer
# todo: queue�[�W�j�p���� Ĵ�p�̦h�u���J40�ӪF��

import random
import time
from threading import Thread
from queue import Queue

print('main start')

q = Queue()

obj_done = object()

def readerF(q_in):
	while True:
		d = q_in.get()
		if d is obj_done:
			break
		print('reader', d + 1000)
		time.sleep(random.random())

def writerF(q_out):
	while True:
		for i in range(40):
			print('writer ', i)
			q_out.put(i)
			time.sleep(random.random())
		q_out.put(obj_done)
		break
		

treader = Thread(target=readerF, args=(q, ))
twriter = Thread(target=writerF, args=(q, ))
treader.start()
twriter.start()


print('main end')
