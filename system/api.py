from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL
from models import Computer, TeamPlacement


class ComputerResource(ModelResource):
    team_placement = fields.ToManyField('system.api.TeamPlacementResource', 'team_placement')

    class Meta:
        queryset = Computer.objects.all()
        resource_name = 'computer'
        authorization = Authorization()
        filtering = {
            "unique_number": ALL,
        }


class TeamPlacementResource(ModelResource):
    computer = fields.ForeignKey(ComputerResource, 'computer')
    team = fields.ForeignKey('contestants.api.TeamResource', 'team')

    class Meta:
        queryset = TeamPlacement.objects.all()
        resource_name = 'team-placement'
        authorization = Authorization()

