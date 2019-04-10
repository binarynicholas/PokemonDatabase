from django.db import models

# Create your models here.

TYPES = (('0', 'Normal'), 
    ('1', 'Fire'), 
    ('2', 'Fighting'), 
    ('3', 'Water'), 
    ('4', 'Grass'), 
    ('5', 'Flying'), 
    ('6', 'Poison'), 
    ('7', 'Electric'), 
    ('8', 'Ground'), 
    ('9', 'Psychic'), 
    ('10', 'Rock'), 
    ('11', 'Ice'), 
    ('12', 'Bug'), 
    ('13', 'Dragon'), 
    ('14', 'Ghost'), 
    ('15', 'Dark'), 
    ('16', 'Steel'), 
    ('17', 'Fairy'), 
    ('18', 'Cyber'),
)
EGG_GROUPS = (('0', 'Monster'),
    ('1', 'Human-Like'),
    ('2', 'Bug'),
    ('3', 'Water 1'),
    ('4', 'Water 2'),
    ('5', 'Water 3'),
    ('6', 'Mineral'),
    ('7', 'Flying'),
    ('8', 'Amorphous'),
    ('9', 'Field'),
    ('10', 'Fairy'),
    ('11', 'Ditto'),
    ('12', 'Grass'),
    ('13', 'Dragon'),
    ('14', 'Undiscovered'),
    ('15', 'Gender unknown'),
)

class Species(models.Model):
    
    species_name = models.CharField(max_length=30)
    date_added = models.DateTimeField('Date Added')
    type_primary = models.CharField(
        max_length=10,
        choices=TYPES,
        default='Normal')
    type_secondary = models.CharField(
        max_length=10,
        choices=TYPES,
        blank=True,
        null=True,
        default=None)
    max_height = models.FloatField(
        max_length=10,
        default='0'
    )
    min_height = models.FloatField(
        max_length=10,
        default='0'
    )
    max_weight = models.FloatField(
        max_length=10,
        default='0'
    )
    min_weight = models.FloatField(
        max_length=10,
        default='0'
    )
    egg_group_1 = models.CharField(
        max_length=10,
        choices=EGG_GROUPS,
        default='Undiscovered'
    )
    egg_group_2 = models.CharField(
        max_length=10,
        choices=EGG_GROUPS,
        blank=True,
        null=True,
        default=None
    )
    ability_1 = models.ForeignKey(
        'Ability', 
        models.SET_NULL,
        related_name='ability_1',
        blank=True,
        null=True,
    )
    ability_2 = models.ForeignKey(
        'Ability', 
        models.SET_NULL,
        related_name='ability_2', 
        blank=True,
        null=True,
    )
    hidden_ability = models.ForeignKey(
        'Ability',  
        models.SET_NULL,
        related_name='hidden_ability',
        blank=True,
        null=True,
    )


    def __str__(self):
        return self.species_name

    def type(self):
        bothTypes = self.get_type_primary_display()
        if (self.type_secondary is not None):
            bothTypes += "/" + self.get_type_secondary_display()
        return bothTypes

    def typeID(long_name):
        right_id = [k for k, v in TYPES if v == long_name]
        return right_id[0]
    
    class Meta:
        verbose_name_plural = 'Species'

class Ability(models.Model):
    ability_name = models.CharField('Ability Name', max_length=30)
    ability_desc = models.CharField('Description', max_length=300)

    def __str__(self):
        return self.ability_name

        
    class Meta:
        verbose_name_plural = 'Abilities'