{% autoescape off %}{% for object in object_list %}INSERT INTO `team` (`login`, `name`, `categoryid`, `affilid`, `authtoken`, `members`, `room`) VALUES  (
        '{{object.login}}',
        '{{object.name|addslashes}}',
        1,
        '{{object.country.code}}',
        '{{object.authtoken}}',
        '{{object.members|addslashes}}',
        ''
    ) ON DUPLICATE KEY UPDATE 
        `name`='{{object.name|addslashes}}', 
        `affilid`='{{object.country.code}}', 
        `authtoken`='{{object.authtoken}}',
        `members`='{{object.members|addslashes}}',
        `room`='';

{% endfor %}
{%endautoescape%}