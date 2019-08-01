from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
REGIONS = (('0', 'Alolan'),
    ('1', 'Unovan'),
    ('2', 'Sinnoan'),
    ('3', 'Galarian'),
    ('4', 'Zea'),
    ('5', 'Qinese'),
)
MOVE_CATEGORIES = (('0', 'Status'),
    ('1', 'Physical'),
    ('2', 'Special'),
)
MOVE_SOURCES = (('0', 'Levelup'),
    ('1', 'TM'),
    ('2', 'Hatch'),
    ('3', 'Tutor'),
)
REGION_NAMES = (('0', 'Kanto'),
('1', 'Johto'),
('2', 'Hoenn'),
('3', 'Sinnoh'),
('4', 'Unova'),
('5', 'Kalos'),
('6', 'Alola'),
('7', 'Galar'),
('8', 'Qinoa'),
('9', 'Zan'),
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
    form = models.CharField(
        max_length=10,
        default='Base',
    )
    regional_variant = models.CharField(
        max_length=10,
        choices=REGIONS,
        blank=True,
        null=True,
        default=None
    )
    base_HP = models.IntegerField(default=0)
    base_Attack = models.IntegerField(default=0)
    base_Defense = models.IntegerField(default=0)
    base_SpAttack = models.IntegerField(default=0)
    base_SpDefense = models.IntegerField(default=0)
    base_Speed = models.IntegerField(default=0)


    def __str__(self):
        my_string = self.species_name
        if self.form != 'Base':
            my_string += "-" + self.form  
        if self.regional_variant is not None:
            my_string =  self.get_regional_variant_display().__str__() + " " + my_string           
        return my_string

    def type_string(self):
        bothTypes = self.get_type_primary_display()
        if (self.type_secondary is not None):
            bothTypes += "/" + self.get_type_secondary_display()
        return bothTypes

    def typeID(long_name):
        right_id = [k for k, v in TYPES if v == long_name]
        return right_id[0]

    def BST(self):
        return self.base_HP + self.base_Attack + self.base_Defense + self.base_SpAttack + self.base_SpDefense + self.base_Speed
    
    def name_first(self):
        my_string = self.species_name
        if self.form != 'Base':
            my_string += "-" + self.form  
        if self.regional_variant is not None:
            my_string =  my_string + " (" + self.get_regional_variant_display().__str__() + ")"           
        return my_string

    class Meta:
        verbose_name_plural = 'Species'
        unique_together = ('species_name', 'regional_variant', 'form',)

class Ability(models.Model):
    ability_name = models.CharField('Ability Name', max_length=30)
    ability_desc = models.CharField('Description', max_length=300)

    def __str__(self):
        return self.ability_name

        
    class Meta:
        verbose_name_plural = 'Abilities'

class Move(models.Model):
    move_name = models.CharField('Move Name', max_length=30)
    move_desc = models.CharField('Description', max_length=300)
    move_type = models.CharField(
        max_length=10,
        choices=TYPES,
        default='Normal')
    base_power = models.IntegerField('Base Power', blank=True, null=True)
    base_accuracy = models.IntegerField('Accuracy', blank=True, null=True)
    move_category = models.CharField(
        max_length=8,
        choices=MOVE_CATEGORIES,
        default='Physical'
    )
    TM_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.move_name
    
    def move_type_string(self):
        return self.get_move_type_display()
    
    def move_category_string(self):
        return self.get_move_category_display()

    def typeID(long_name):
        right_id = [k for k, v in TYPES if v == long_name]
        return right_id[0]

    def categoryID(long_name):
        right_id = [k for k, v in MOVE_CATEGORIES if v == long_name]
        return right_id[0]

class LearnableMove(models.Model):
    move = models.ForeignKey(
        'Move',
        models.SET_NULL,
        blank=True,
        null=True,
    )
    species = models.ForeignKey(
        'Species', 
        models.SET_NULL,
        blank=True,
        null=True,
    )
    source = models.CharField(
        max_length=7,
        choices=MOVE_SOURCES,
        default='TM'
    )

    
    def __str__(self):
        return self.species.species_name + ": " + self.move.move_name

    class Meta:
        unique_together = ('move', 'species', 'source')

class LevelMove(LearnableMove):
    level = models.PositiveIntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

class Location(models.Model):
    location_name = models.CharField(max_length=30)
    region=models.CharField(
        max_length=10,
        choices=REGION_NAMES,
        default='Kanto'
    )
    available_species = models.ManyToManyField(
        Species
    )

    def __str__(self):
        my_string = self.location_name
        if (self.region is not None):
            my_string += ", " + self.get_region_display()
        return my_string