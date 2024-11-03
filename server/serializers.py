from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Avg

from .models import Book, Category, Comment, Contract, Author


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class BookSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        category = validated_data.pop('category')
        author_name = validated_data.pop('author')
        if author_name:
            author = Author.objects.get_or_create(name=author_name)[0] 
            book = Book.objects.create(author=author, **validated_data)
        else:
            book = Book.objects.create(**validated_data)

        
        for cat in category:
            book.category.add(cat)

        return book 
    
    def get_rating(self, book):
        ratings = book.ratings.all()
        count = ratings.count()
        if count:
            rating = ratings.aggregate(Avg('rating'))
            
            return {'rating': rating['rating__avg'], 'count': count}

        return {'rating': 0, 'count': 0}


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()
    
    class Meta:
        model = Contract
        fields = '__all__'
        


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    comment_owner = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    repliable = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('user', 'id', 'date', 'body', 'reply_count', 'comment_owner', 'repliable')

    def get_reply_count(self, comment):
        return comment.replies.count()

    def get_comment_owner(self, comment):
        return comment.user.id == self.context.get('request').user.id

    def get_repliable(self, comment):

        return comment.book != None
    