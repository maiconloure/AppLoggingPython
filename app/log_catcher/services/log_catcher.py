from google.auth import jwt
from google.cloud import pubsub_v1
from google.cloud import bigquery
import settings
import base64
import json
import threading

class LogCatcherService:
    def __init__(self):
        self.project_id = settings.PROJECT_ID
        self.client = bigquery.Client()
        self.dataset_id = settings.DATASET_ID
        self.table_id = settings.TABLE_ID
        self.subscriber = pubsub_v1.SubscriberClient()
        self.timeout = settings.TIMEOUT
        self.active = False

    def spamming_streaming(self, subscribers):
        self.active = True
        for subscription in subscribers:
            # self.streaming_messages(subscription)
            stream_subscribe = threading.Thread(
                 target=self.streaming_messages, args=(subscription, ), daemon=True)
            stream_subscribe.start()

            print(stream_subscribe.terminate())

        return True

    
    def streaming_messages(self, subscription_id):
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription_id)
        streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=self.callback)
        print(f"Listening for messages on {subscription_path}...\n")
        
        with self.subscriber:
            try:
                streaming_pull_future.result(timeout=int(self.timeout))
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()
              
        # return
    

    def collect_messages(self, data):
        stream = base64.urlsafe_b64decode(data)
        raw = json.loads(stream)
        message = (*raw.values(),)
        return self.write_messages_to_bq(self.dataset_id, self.table_id, [message])

    def callback(self, message):
        print(f"\nReceived {message.data}")
        result = self.collect_messages(message.data)

        if (result['status'] == 'success'):
            message.ack()
        else:
            message.nack()
            


    def write_messages_to_bq(self, dataset_id, table_id, messages):
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table = self.client.get_table(table_ref)

        errors = self.client.insert_rows(table, messages)

        if not errors:
            print('Loaded {} row(s) into {}:{}'.format(len(messages), dataset_id, table_id,))
            return { 'message': 'Loaded {} row(s) into {}:{}'.format(len(messages), dataset_id, table_id,),
                     'status': 'success' }
        else:
            for error in errors:
                return { 'message': error.message, 'status': 'error' }
