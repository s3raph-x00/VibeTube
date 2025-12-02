from pymongo import MongoClient
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from bson import ObjectId
from datetime import datetime

client = MongoClient(settings.MONGODB_SETTINGS['host'])
db = client[settings.MONGODB_SETTINGS['database']]

class UserModel:
    collection = db['users']
    
    @classmethod
    def create(cls, username, password, email=''):
        user_data = {
            'username': username,
            'password': make_password(password),
            'email': email,
            'created_at': datetime.utcnow()
        }
        result = cls.collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    
    @classmethod
    def find_by_username(cls, username):
        return cls.collection.find_one({'username': username})
    
    @classmethod
    def find_by_id(cls, user_id):
        return cls.collection.find_one({'_id': ObjectId(user_id)})
    
    @classmethod
    def check_password(cls, user, password):
        return check_password(password, user['password'])
    
    @classmethod
    def username_exists(cls, username):
        return cls.collection.find_one({'username': username}) is not None

class PlaylistModel:
    collection = db['playlists']
    
    @classmethod
    def create(cls, user_id, name, description=''):
        playlist_data = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'videos': [],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = cls.collection.insert_one(playlist_data)
        playlist_data['_id'] = result.inserted_id
        return playlist_data
    
    @classmethod
    def find_by_user(cls, user_id):
        return list(cls.collection.find({'user_id': user_id}))
    
    @classmethod
    def find_by_id(cls, playlist_id, user_id=None):
        query = {'_id': ObjectId(playlist_id)}
        if user_id:
            query['user_id'] = user_id
        return cls.collection.find_one(query)
    
    @classmethod
    def add_video(cls, playlist_id, user_id, video_data):
        cls.collection.update_one(
            {'_id': ObjectId(playlist_id), 'user_id': user_id},
            {
                '$addToSet': {'videos': video_data},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
    
    @classmethod
    def remove_video(cls, playlist_id, user_id, video_path):
        cls.collection.update_one(
            {'_id': ObjectId(playlist_id), 'user_id': user_id},
            {
                '$pull': {'videos': {'path': video_path}},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
    
    @classmethod
    def delete(cls, playlist_id, user_id):
        cls.collection.delete_one({'_id': ObjectId(playlist_id), 'user_id': user_id})
