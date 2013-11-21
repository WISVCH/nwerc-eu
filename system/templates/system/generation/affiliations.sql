{% autoescape off %}{% for object in team_placements %}INSERT INTO `team_affiliation` (`affilid`, `name`, `country`) VALUES (
    '{{object.institution_id}}', 
    '{{object.name|addslashes}}', 
    '{{object.country.ICPC_name}}'
) ON DUPLICATE KEY UPDATE 
    `name`='{{object.name|addslashes}}', 
    `country`='{{object.country.ICPC_name}}';

{% endfor %}{% endautoescape %}