from clickhouse_driver import Client

client = Client('localhost')
client.execute('CREATE DATABASE IF NOT EXISTS  book_database')


