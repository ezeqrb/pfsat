from django.db import models
# Create your models here.

class Choices(models.Model):
    choice = models.CharField(max_length=5000)
    is_answer = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
    
    def __str__(self):
        return f"{self.choice}"

class Questions(models.Model):
    question = models.CharField(max_length= 10000)
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default= False)
    answer_key = models.CharField(max_length = 5000, blank = True)
    score = models.IntegerField(blank = True, default=0)
    feedback = models.CharField(max_length = 5000, null = True)
    choices = models.ManyToManyField(Choices, related_name = "choices")

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return f"{self.question}"

class Answer(models.Model):
    answer = models.CharField(max_length=5000)
    answer_to = models.ForeignKey(Questions, on_delete = models.CASCADE ,related_name = "answer_to")

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
    
    def __str__(self):
        return f"{self.answer}"

class Form(models.Model):
    ESTADOS = [
        ('','--- Seleccione ---'),
        ('b','borrador'),
        ('p','publicada')
    ]

    code = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, blank = True)
    background_color = models.CharField(max_length=20, default = "#f2f6fc")
    text_color = models.CharField(max_length=20, default="#272124")
    collect_email = models.BooleanField(default=False)
    authenticated_responder = models.BooleanField(default = True)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.CharField(max_length = 10000, default = "Sus respuestas han sido guardadas con éxito!")
    is_quiz = models.BooleanField(default=False)
    allow_view_score = models.BooleanField(default= True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    questions = models.ManyToManyField(Questions, related_name = "questions")
    status = models.CharField(max_length=1,choices=ESTADOS,default='b')

    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
    
    def __str__(self):
        return f"{self.title}"

class Responses(models.Model):
    response_code = models.CharField(max_length=20)
    response_to = models.ForeignKey(Form, on_delete = models.CASCADE, related_name = "response_to")
    responder_ip = models.CharField(max_length=30)
    responder_email = models.EmailField(blank = True)
    response = models.ManyToManyField(Answer, related_name = "response")

    class Meta:
        verbose_name = 'Responde Respuesta'
        verbose_name_plural = 'Responden Respuestas'

    def __str__(self):
        return f"{self.response_code}"
