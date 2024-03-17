from django.db import models
from datetime import date

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password

from django.utils import timezone
from django.utils.translation import gettext_lazy as _\

from django.core.mail import send_mail
from django.conf import settings

from .lib import get_search_results
from .helper import predict_priority_scores, extract_keywords, prioritize_results_order, generate_order

sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username        = models.CharField(
                        _("Username"),
                        max_length=150,
                        unique=True,
                        help_text=_(
                            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
                        ),
                        validators=[username_validator],
                        error_messages={
                            "unique": _("A user with that username already exists."),
                        },
                    )
    password        = models.CharField(_("password"), max_length=128)
    first_name      = models.CharField(_("first name"), max_length=150, blank=True)
    last_name       = models.CharField(_("last name"), max_length=150, blank=True)
    email           = models.EmailField(_("email address"), blank=True)
    gender          = models.CharField(
                        max_length=50, 
                        choices=sex_choice, 
                        default='Male'
                    )
    date_joined     = models.DateTimeField(_("date joined"), default=timezone.now)
    is_staff        = models.BooleanField(
                        _("staff status"),
                        default = False,
                    )
    is_active       = models.BooleanField(
                        _("active"),
                        default = True,
                    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"

    def get_all_groups(self):
        return self.groups

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

# class User(AbstractUser):
#     # CustomUser model will be act as General class of parent
#     searches_count          = models.IntegerField(default=0)
#     interested_sites        = models.JSONField(default=list)
#     not_interested_sites    = models.JSONField(default=list)

#     def update_search_profile(self, context):
        
#         # get me list of profiles which have query_keys in their query_keys, highest matching_count first
#         profiles = self.get_user_interest_profiles(context['query'])

#         if profiles.exists():
#             profile = profiles.first()
#         else:
#             profile = UserInterestProfile(user=self)
#             self.searches_count += 1
#             self.save()

#         profile.query = context['query']
#         profile.query_keys = list(set(profile.query_keys + context['query_keys']))
#         profile.interested_keywords = list(set(profile.interested_keywords + context['interested_keywords']))
#         profile.not_interested_keywords = list(set(profile.not_interested_keywords + context['not_interested_keywords']))
#         profile.site = context['site']
#         profile.save()

#     def get_user_interest_profiles(self: AbstractUser, query: str):
#         query_keys = [
#             token.lemma_ for token in nlp(query) if token.is_alpha and not token.is_stop
#         ]
#         return self.searches.annotate(
#                 matching_count = models.Sum(
#                     models.Case(
#                         *[modes.When(query_keys__icontains=key, then=1) for key in query_keys],
#                         default=0,
#                         output_field=models.IntegerField()
#                     )
#                 )
#             ).filter(matching_count__gt=0).order_by('-matching_count')

# class UserInterestProfile(models.Model):
#     user                        = models.OneToOneField(User, on_delete=models.CASCADE, related_name="searches")
#     query                       = models.CharField(max_length=100, blank=True)
#     query_keys                  = models.JSONField(default=list)
#     timestamp                   = models.DateTimeField(auto_now_add=True)
#     interested_keywords         = models.JSONField(default=list)
#     not_interested_keywords     = models.JSONField(default=list)
#     site                        = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.query}"
    

class Site(models.Model):
    domain          = models.CharField(max_length = 255)
    route           = models.CharField(max_length = 100)
    title           = models.CharField(max_length = 100)
    keywords        = models.JSONField(default=list)
    description     = models.TextField(blank=True)
    duration        = models.IntegerField(default = 20)

def generate_default_fields():
    return dict({"domains": {}, "action_intialization": 0})

class User(AbstractUser):
    info            = models.JSONField(default = generate_default_fields)

    def get_user_liked_keywords(self):
        search_histories = self.search_history.filter()[:settings.THRESHOLD_BACKTRACK_HISTORY]
        return search_histories.values_list('query_keys', flat=True)
    
    def get_user_specific_search_results(self, context):
        """
        Retrieve search results based on user-specific context and preferences.

        Args:
            self    (User): the instance of the class
            context (dict): user-specific context for the search
            
        Returns:
            SearchResults
                items (list[SearchResult]): prioritized user search results
        """
        # process the liked keywords
        liked_keywords = self.get_user_liked_keywords()

        search  = get_search_results(context)
        items   = search['items']

        meta_infos = [
            f"{item['title']} {item['snippet']}"
            for item in items
        ]
        priority_scores = predict_priority_scores(meta_infos, liked_keywords)
        scores          = generate_order({
            'predictive_score': priority_scores,
            # 'relevance_socre' : [],
        }, len(items))
        search['items'] = prioritize_results_order(items, scores)

        # for item in items:
        #     print('{} {}: {}'.format(item['title'], item['snippet'], item['priority_score']))

        return search
    
    def update_search_profile(self, context):
        domain = context.get('domain')

        # record the site details, if not already recorded
        existing_site   = Site.objects.filter(domain = domain).filter(route = context.get('route')).first
        if existing_site is None:
            site = Site.objects.create(
                domain = domain,
                route  = context.get('route'),
                title  = context.get('title'),
                keywords =  extract_keywords(context.get('meta', ""))
            )
            site.save()
        else:
            site = existing_site
        
        # increment the visits counter
        visits = self.info['domains'].get(domain, 0) + 1
        self.info['domains'][domain] = visits

        # create search history record
        search_history = self.search_history.filter(
            site_id = site.id
        ).first
        
        # if their is no previous visits, then create a new one
        if search_history is None:
            search_history = self.search_history.create(
                query       = context['query'],
                site_id     = site.id,
                query_keys  = context['query_keys'],
                is_relevant = context['like_status']
            )

        search_history.save()

    def get_user_interest_profiles(self: AbstractUser, query: str):
        query_keys = extract_keywords(query)
        return self.search_history.annotate(
                matching_count = models.Sum(
                    models.Case(
                        *[models.When(query_keys__icontains=key, then=1) for key in query_keys],
                        default=0,
                        output_field=models.IntegerField()
                    )
                )
            ).filter(matching_count__gt=0).order_by('-matching_count')

class SearchHistory(models.Model):
    query           = models.CharField(max_length = 100)
    timestamp       = models.DateTimeField(auto_now = True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "search_history")
    site            = models.ForeignKey(Site, on_delete=models.CASCADE)
    score           = models.IntegerField(default = 0)
    query_keys      = models.JSONField(default=list)
    time_spend      = models.PositiveIntegerField(default = 10)
    is_relevant     = models.BooleanField(default = True)


    
