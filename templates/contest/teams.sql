{% autoescape off %}{% for object in object_list %}INSERT INTO `team` (`login`, `name`, `categoryid`, `affilid`, `authtoken`, `members`, `room`) VALUES  (
        '{{object.username}}',
        '{{object.team.name|addslashes}}',
        1,
        '{{object.team.institution.institution_id}}',
        '{{object.computer.ip}}',
        '{% for member in object.team.teamperson_set.all %}{{member.person|addslashes}} ({{member.get_role_display|addslashes}})\n{%endfor%}',
        '{{object.computer.nwerc_number}}'
    ) ON DUPLICATE KEY UPDATE 
        `name`='{{object.team.name|addslashes}}', 
        `affilid`='{{object.team.institution.institution_id}}', 
        `authtoken`='{{object.computer.ip}}',
        `members`='{% for member in object.team.teamperson_set.all %}{{member.person|addslashes}} ({{member.get_role_display|addslashes}})\n{%endfor%}',
        `room`='{{object.computer.nwerc_number}}';

{% endfor %}
{%endautoescape%}