#!/usr/bin/env python
# coding: utf-8

# # Kafka Producer

# In[6]:


import json
from datetime import datetime
from time import sleep

from kafka import KafkaProducer

# In[ ]:


# By default it take JSON serializer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10, 1))

# In[ ]:


# Topic name is youtube
producer.send('youtube', b'Hello, Kafka right now')
# Now go to consumer terminal and check this message


# In[ ]:


now = datetime.now()
now

# In[ ]:


current_time = now.strftime("%d/%m/%Y %H:%M:%S")
current_time

# In[ ]:


for i in range(10):
    message = "Message {}".format(str(datetime.now().time()))
    producer.send('youtube', json.dumps(message).encode('utf-8'))
    sleep(2)
    print("Message sent ", i)

# # Kafka consumer

# In[4]:


from kafka import KafkaConsumer

# In[5]:


consumer = KafkaConsumer('youtube',
                         bootstrap_servers=['localhost:9092'],
                         api_version=(0, 10)
                         # ,consumer_timeout_ms=1000
                         )

# In[ ]:


for message in consumer:
    # print(message)
    print(message.value)
