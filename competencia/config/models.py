from django.db import models


class Catalogo(models.Model):
    nombre = models.CharField(max_length=64)
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True


class Aparato(Catalogo):
    class Meta:
        managed = True
        db_table = 'aparato'


class Calificacion(models.Model):
    aparato = models.ForeignKey('Aparato', models.DO_NOTHING)
    calificacion = models.FloatField()
    competidor = models.ForeignKey('Competidor', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'calificacion'


class Competencia(models.Model):
    nombre = models.CharField(max_length=128)
    fecha = models.DateField()
    estatus = models.BooleanField()

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'competencia'


class Competidor(models.Model):
    nombre = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128)
    nivel = models.ForeignKey('Nivel', models.DO_NOTHING)
    gimnasio = models.ForeignKey('Gimnasio', models.DO_NOTHING)
    edad = models.IntegerField()
    competencia = models.ForeignKey('Competencia', models.DO_NOTHING)
    grupo = models.ForeignKey('Grupo', models.DO_NOTHING, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre + " " + self.apellidos

    class Meta:
        managed = True
        db_table = 'competidor'


class Genero(Catalogo):
    class Meta:
        managed = True
        db_table = 'genero'


class Gimnasio(Catalogo):
    class Meta:
        managed = True
        db_table = 'gimnasio'


class Grupo(models.Model):
    competencia = models.ForeignKey('Competencia', models.DO_NOTHING)
    aparato = models.ForeignKey('Aparato', models.DO_NOTHING, blank=True, null=True)


class Nivel(Catalogo):
    class Meta:
        managed = True
        db_table = 'nivel'
