from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'UserName': obj[0],
            'Password': obj[1],
        }

class GameFullSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'Name': obj[0],
            'ReleaseYear': obj[1],
            'Developer': obj[2],
            'Publisher': obj[3],
            'MaxPlayers': obj[4],
            'ESRB': obj[5],
            'OverView': obj[6],
            'Genres': obj[7],
            'Platforms': obj[8],
        }


class GameSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'Name': obj[0],
            'ReleaseYear': obj[1],
            'Developer': obj[2],
            'Publisher': obj[3],
            'MaxPlayers': obj[4],
            'ESRB': obj[5],
            'OverView': obj[6],
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
            'Id': obj[0],
            'TimestampCreated': obj[1],
            'Content': obj[2],
            'Title': obj[3],
            'GameName': obj[4],
            'UserName': obj[5],
        }



class ReviewSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'RecommendationId': obj[0],
            'UserName': obj[1],
            'Review': obj[2],
            'Timestampcreated': obj[3],
            'GameName': obj[4],
        }

class UserGamesSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'GameName': obj[0],
            'UserName': obj[1],
        }

class LikeSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'PostId': obj[0],
            'UserName': obj[1],
        }

class CommentSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'CommentId': obj[0],
            'Content': obj[1],
            'PostId': obj[2],
            'UserName': obj[3],
        }
