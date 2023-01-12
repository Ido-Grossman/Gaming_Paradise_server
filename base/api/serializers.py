from rest_framework import serializers
import datetime

class UserSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'UserName': obj[0],
            'Password': obj[1],
        }

class GameFullSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'id': obj[0],
            'Name': obj[1],
            'ReleaseYear': obj[2],
            'Developer': obj[3],
            'Publisher': obj[4],
            'MaxPlayers': obj[5],
            'ESRB': obj[6],
            'OverView': obj[7],
            'Genres': obj[8],
            'Platforms': obj[9],
        }


class GameSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'id': obj[0],
            'Name': obj[1],
            'ReleaseYear': obj[2],
            'Developer': obj[3],
            'Publisher': obj[4],
            'MaxPlayers': obj[5],
            'ESRB': obj[6],
            'OverView': obj[7],
        }

class GameNameSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'GameName': obj[0],
        }

class GenreSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'Genre': obj[0],
        }


class GenreGameSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'GameName': obj[0],
        }

class PlatformSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'Platform': obj[0],
        }


class PlatformGameSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'GameName': obj[0],
        }

class PostSerializer(serializers.Serializer):

    def to_representation(self, obj):
        return {
            'id': obj[0],
            'TimestampCreated': obj[1].strftime('%d/%m/%Y %H:%M:%S'),
            'Content': obj[2],
            'Title': obj[3],
            'GameName': obj[4],
            'UserName': obj[5],
        }



class ReviewSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'id': obj[0],
            'UserName': obj[1],
            'Content': obj[2],
            'TimestampCreated': obj[3].strftime('%d/%m/%Y %H:%M:%S'),
        }

class UserGamesSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'GameName': obj[0],
            'UserName': obj[1],
        }

class CommentSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'id': obj[0],
            'Content': obj[1],
            'TimestampCreated': obj[2].strftime('%d/%m/%Y %H:%M:%S'),
            'PostId': obj[3],
            'UserName': obj[4],
        }
