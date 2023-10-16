from django.contrib import admin

# Register your models here.

from .models import User, Train, RoomStatus, Room, MatchType, Match, ReviewType, Review, Message, TransactionKarma

admin.site.register(User)
admin.site.register(Train)
admin.site.register(RoomStatus)
admin.site.register(Room)
admin.site.register(MatchType)
admin.site.register(Match)
admin.site.register(ReviewType)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(TransactionKarma)


