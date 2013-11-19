from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from models import Team, Institution, Country


class TeamResource(ModelResource):
    team_placement = fields.ToManyField('system.api.TeamPlacementResource', 'team_placement', null=True, blank=True)
    institution = fields.ForeignKey('contestants.api.InstitutionResource', 'institution')

    class Meta:
        queryset = Team.objects.all()
        resource_name = 'team'
        authorization = Authorization()


class InstitutionResource(ModelResource):
    country = fields.ForeignKey('contestants.api.CountryResource', 'country')

    class Meta:
        queryset = Institution.objects.all()
        resource_name = 'institution'
        authorization = Authorization()


class CountryResource(ModelResource):

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        authorization = Authorization()

