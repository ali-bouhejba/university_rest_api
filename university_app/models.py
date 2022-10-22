import time
from datetime import date
from email.policy import default
from pyexpat import model
from django.db import models
from  datetime import timezone
import enum


StudyLevel = [('FirstClass', 'first_class'), ('SecondClass', 'second_class')]

class Adress(models.Model):
    number = models.IntegerFieldField(max_length=30,default=1,null=False,blank=False)
    streetName = models.CharField(max_length=50,null=False,blank=False,verbose_name="street Name")
    city = models.CharField(max_length=30)
    postalCode = models.CharField(max_length=30)

    class Meta:
        db_table = "adress"

    def __str__(self):
        return self.name



class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=100, choices=StudyLevel)
    speciality = models.CharField(max_length=30)


    def __str__(self):
        return '%s, %s, %s' % (self.name, self.level, self.speciality)

    class Meta:
        db_table = "group"


studentState=[('Present','student is present'),('Absent','student is absent'),('excluded','student is excluded'),('delayed','student is delayed')]
class Student(models.Person):


    stdGroup = models.ForeignKey(Group, on_delete=models.CASCADE)
    adress=models.OneToOneField(Adress,on_delete=models.CASCADE())
    group=models.ForeignKey(Group,null=True,on_delete=models.CASCADE())
    state = models.CharField(max_length=100, choices=studentState.choices, default=studentState[0][0])

    class Meta:
        db_table = "student"
        ordering = ['name', 'familyName']

    def __str__(self):
        return f'name={self.name},familyName={self.familyName},email={self.email},birthday={self.birthDate}'


class Module(models.Model):
    name = models.CharField(max_length=100,
                            null=True,
                            blank=False)
    coefficient = models.FloatField
    nbClass = models.IntegerField
    ## create the association class betwen modele and group
    ##class study will not be created because we dont have extra columns
    study=models.ManyToManyField(Group,on_delete=models.CASCADE(),blank=True,null=True)



    class Meta:
        db_table = "module"
        ordering = ['name']

    def __str__(self):
        return '%s,%s,%s' % (self.name, self.coefficient, self.nbClass)






class Teacher(models.Person):
    ##through_fields= les 2 cles etrangers(teacher_Modeule)
    teacher_module=models.ManyToManyField(Module,through='TeacherModules',through_fields=("teacher","module"))
    grade=models.CharField(max_length=200)
    weeklyHours=models.FloatFieldField()


class TeacherModules(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE())
    module=models.ForeignKey(Module,on_delete=models.CASCADE())
    year=models.IntegerField(default=timezone.now().year)
    nb_heures=models.PositiveIntegerField(default=1)



class Person(models.Model):
    name = models.CharField(max_length=100,
                            null=True,
                            blank=False)
    familyName = models.CharField(max_length=100,
                                  null=True,
                                  blank=False)
    email = models.EmailField(max_length=50, unique=True)
    birthDate = models.DateField(default=date(2003, 1, 1))
    photo = models.ImageField(upload_to="photos/students")
    #enumeration state
















