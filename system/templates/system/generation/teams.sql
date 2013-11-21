{% autoescape off %}{% for object in object_list %}INSERT INTO `team` (`login`, `name`, `categoryid`, `affilid`, `authtoken`, `members`, `room`, `hostname`) VALUES  (
        '{{object.username}}',
        '{{object.team.name|addslashes}}',
        {% if object.team.status == 'A' %}1{%else%}2{%endif%},
        '{{object.team.institution.institution_id}}',
        '{{object.computer.ip}}',
        '{% for member in object.team.teamperson_set.all %}{{member.person|addslashes}} ({{member.get_role_display|addslashes}})\n{%endfor%}',
        '{{object.computer.unique_number}}',
        '{{object.computer.hostname}}'
    ) ON DUPLICATE KEY UPDATE 
        `name`='{{object.team.name|addslashes}}', 
        `affilid`='{{object.team.institution.institution_id}}', 
        `categoryid`={% if object.team.status == 'A' %}1{%else%}2{%endif%},
        `authtoken`='{{object.computer.ip}}',
        `members`='{% for member in object.team.teamperson_set.all %}{{member.person|addslashes}} ({{member.get_role_display|addslashes}})\n{%endfor%}',
        `room`='{{object.computer.unique_number}}',
        `hostname`='{{object.computer.hostname}}';

{% endfor %}
{%endautoescape%}