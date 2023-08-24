from django.db import models


# Create your models here.
class Word(models.Model):
    prototype = models.TextField(max_length=64, unique=True, verbose_name='原型', db_index=True)
    translated = models.TextField(max_length=16, unique=False, verbose_name='中文翻译', blank=True)
    explanation = models.TextField(max_length=1024, unique=False, verbose_name='释义', blank=True)
    part_of_speech = models.CharField(max_length=16, unique=False, verbose_name='词性', blank=True)

    def __str__(self):
        return "单词原型:{}".format(self.prototype)


class Author(models.Model):
    name = models.TextField(max_length='16', unique=True, verbose_name='作者名称', db_index=True)
    sEXT = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='sEXT', unique=False)
    sNEU = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='sNEU', unique=False)
    sAGR = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='sAGR', unique=False)
    sCON = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='sCON', unique=False)
    sOPN = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='sOPN', unique=False)
    cEXT = models.BooleanField(verbose_name='cEXT', unique=False)
    cNEU = models.BooleanField(verbose_name='cNEU', unique=False)
    cAGR = models.BooleanField(verbose_name='cAGR', unique=False)
    cCON = models.BooleanField(verbose_name='cCON', unique=False)
    cOPN = models.BooleanField(verbose_name='cOPN', unique=False)

    def __str__(self):
        return "作者名称:{}".format(self.name)
