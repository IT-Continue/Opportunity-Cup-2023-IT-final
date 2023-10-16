from django.contrib import admin

# Register your models here.

from .models import User, Train, RoomStatus, Room, MatchType, Match, ReviewType, Review, Message, TransactionKarma, UserLikes, UserFlags, UserData

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
admin.site.register(UserLikes)
admin.site.register(UserFlags)
admin.site.register(UserData)


