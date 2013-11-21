{% autoescape off %}{% for object in livecontest %}INSERT INTO `team` (`login`, `name`, `categoryid`, `authtoken`, `members`, `room`) VALUES  (
        '{{object.login}}',
        '{{object.name|addslashes}}',
        1,
        '{{object.authtoken}}',
        '{{object.members|addslashes}}',
        ''
    ) ON DUPLICATE KEY UPDATE 
        `name`='{{object.name|addslashes}}',
        `authtoken`='{{object.authtoken}}',
        `members`='{{object.members|addslashes}}',
        `room`='';

{% endfor %}
{%endautoescape%}