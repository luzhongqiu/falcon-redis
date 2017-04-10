# -*- encoding: utf-8 -*-
import redis
from .exception import NotRedisException


class MiddleWare(object):
    def __init__(self, conn):
        self.conn = conn

    def process_resource(self, req, resp, resource, params):
        path = req.path
        content = req.stream.read()
        key = '{}:{}'.format(path, content)
        if isinstance(self.conn, redis.StrictRedis):
            self.conn.get(key)
        else:
            raise NotRedisException()

    def process_response(self, req, resp, resource, req_succeeded):
        if req.context.get('cache'):
            path = req.path
            content = req.stream.read()
            key = '{}:{}'.format(path, content)
            value = resp.body
            ttl = req.context.get('cache_ttl', 600)
            if isinstance(self.conn, redis.StrictRedis):
                self.conn.set(key, value, ex=ttl)
            else:
                raise NotRedisException()


class Cache(object):
    def __init__(self, host, port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.conn = redis.StrictRedis(connection_pool=self.pool)

    def cache(self, ttl=600):
        def wrap1(func):
            def wrap2(cls, req, resp, *args, **kwargs):
                func(cls, req, resp, *args, **kwargs)
                req.context['cache'] = True
                req.context['cache_ttl'] = ttl

            return wrap2

        return wrap1

    @property
    def middleware(self):
        return MiddleWare()
