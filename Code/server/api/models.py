from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        DATER = 'dater'
        CUPID = 'cupid'
        MANAGER = 'manager'

    role = models.CharField(choices=Role.choices, max_length=7)
    phone_number = models.CharField(max_length=10, unique=True)


class Dater(models.Model):
    class Communication(models.IntegerChoices):
        EMAIL = 0
        TEXT = 1
        # PUSH = 2   Not implemented
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.role = User.Role.DATER
        self.user.save()

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    budget = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    communication_preference = models.IntegerField(default=Communication.EMAIL, choices=Communication.choices)
    description = models.TextField()
    dating_strengths = models.TextField()
    dating_weaknesses = models.TextField()
    interests = models.TextField()
    past = models.TextField()
    nerd_type = models.TextField()
    relationship_goals = models.TextField()
    ai_degree = models.TextField(default="max")
    cupid_cash_balance = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    location = models.TextField()
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    is_suspended = models.BooleanField(default=False)
    # TODO: height_field and width_field were removed as they were not
    # implemented correctly. These should indicate what field to store
    # that data on, not a hard-coded integer
    profile_picture = models.ImageField(
        upload_to='api/images', max_length=100, null=True
    )


class Cupid(models.Model):
    class Status(models.IntegerChoices):
        OFFLINE = 0
        GIGGING = 1
        AVAILABLE = 2

    def save(self, *args, **kwargs):
        self.user = User.objects.get(username=self.user)
        super().save(*args, **kwargs)
        self.user.role = User.Role.CUPID
        self.user.save()

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    accepting_gigs = models.BooleanField(default=False)
    gigs_completed = models.IntegerField(default=0)
    gigs_failed = models.IntegerField(default=0)
    status = models.IntegerField(default=0,choices=Status.choices)
    cupid_cash_balance = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    location = models.TextField(default="")
    gig_range = models.IntegerField(default=20)
    rating_sum = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    is_suspended = models.BooleanField(default=False)


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    from_ai = models.BooleanField()


class Quest(models.Model):
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    items_requested = models.TextField()
    pickup_location = models.TextField()

# Need to refactor gig so that it's not just a hard coded list.
class Gig(models.Model):
    class Status(models.IntegerChoices):
        # Need to refactor so that these aren't hard coded
        UNCLAIMED = 0   
        CLAIMED = 1
        COMPLETE = 2
    
    # detailsJson = models.TextField()
    # location = models.TextField()
    # budget = models.DecimalField(max_digits=10, decimal_places=2)
    dater = models.ForeignKey(Dater, on_delete=models.CASCADE)
    cupid = models.ForeignKey(Cupid, on_delete=models.CASCADE, null=True) # Move to GigAssignment
    status = models.IntegerField(choices=Status.choices)
    date_time_of_request = models.DateTimeField(auto_now_add=True)
    date_time_of_claim = models.DateTimeField(null=True)
    date_time_of_completion = models.DateTimeField(null=True)
    quest = models.OneToOneField(Quest, on_delete=models.CASCADE)
    dropped_count = models.IntegerField()
    accepted_count = models.IntegerField()


class Date(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned'
        OCCURRING = 'occurring'
        PAST = 'past'
        CANCELED = 'canceled'

    dater = models.ForeignKey(Dater, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    location = models.TextField()
    description = models.TextField()
    status = models.TextField(choices=Status.choices)
    budget = models.DecimalField(max_digits=10, decimal_places=2)


class Feedback(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='owner')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    message = models.TextField()
    star_rating = models.IntegerField()
    date_time = models.DateTimeField()

# REMOVE FOR STRIPE INTEGRATION
class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_on_card = models.TextField()
    card_number = models.TextField()
    cvv = models.TextField()
    expiration = models.TextField()

# REMOVE FOR STRIPE INTEGRATION
class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routing_number = models.TextField()
    account_number = models.TextField()

# ----------------------------------------
# Future features below
# ----------------------------------------

# class PaymentMethodToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     provider = models.TextField()
#     provider_token = models.TextField()
#     brand = models.TextField()
#     last4 = models.TextField()
#     exp_month = models.IntegerField()
#     exp_year = models.IntegerField()

# class PaymentIntent(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     provider = models.TextField()
#     intent_id = models.TextField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.TextField()
#     status = models.TextField()
#     metadataJson

# class gigAssignment(models.Model):
#     gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
#     cupid = models.ForeignKey(Cupid, on_delete=models.CASCADE)
#     date_time_of_claim = models.DateTimeField(auto_now_add=True)
#     date_time_of_completion = models.DateTimeField(null=True)
#     date_time_of_drop = models.DateTimeField(null=True)
#     cancel_reason = models.TextField(null=True)
#     detailsJson = models.TextField()    # Inherited from gig