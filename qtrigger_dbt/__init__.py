import logging
import azure.functions as func

from .dbt_runner import DBTRunner

def main(msg: func.QueueMessage):
    message_json = msg.get_json()
    runner = DBTRunner()
    runner.go(**message_json)