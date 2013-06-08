{% autoescape off %}{% for object in object_list %}INSERT INTO `team_affiliation` (`affilid`, `name`, `country`) VALUES (
    '{{object.code}}', 
    '{{object.name|addslashes}}', 
    '{{object.code}}'
) ON DUPLICATE KEY UPDATE 
    `name`='{{object.name|addslashes}}', 
    `country`='{{object.code}}';

{% endfor %}{% endautoescape %}