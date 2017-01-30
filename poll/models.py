from django.db import models

# Create your models here.


class Questionnaire(models.Model):
    name = models.CharField(max_length=50)


class Page(models.Model):
    PAGE_TYPES = (
        ("Question", "Question"),
        ("Video", "Video"),
        ("Starting", "Starting"),
        ("Login", "Login"),
        ("Lottery", "Lottery")
    )

    number = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=PAGE_TYPES)
    ua_title = models.CharField(max_length=50)
    ru_title = models.CharField(max_length=50)
    ua_heading = models.CharField(max_length=200, blank=True)
    ru_heading = models.CharField(max_length=200, blank=True)
    ua_text = models.CharField(max_length=2000, blank=True)
    ru_text = models.CharField(max_length=2000, blank=True)
    questionnaire = models.ForeignKey(Questionnaire)

    def __str__(self):
        return "Page №" + str(self.number) + " Title: " + self.ua_title


class Question(models.Model):
    QUESTION_TYPES = (
        ("SimpleOpenQuestion", "SimpleOpenQuestion"),
        ("SimpleQuestionWithOneAnswer", "SimpleQuestionWithOneAnswer"),
        ("SimpleQuestionWithSeveralAnswers", "SimpleQuestionWithSeveralAnswers"),
        ("TableQuestion", "TableQuestion"),
        ("QuestionWithOptionsAndUserAnswer", "QuestionWithOptionsAndUserAnswer")
    )

    type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    ua_heading = models.CharField(max_length=200)
    ru_heading = models.CharField(max_length=200)
    ua_text = models.CharField(max_length=500, blank=True)
    ru_text = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey(Page)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.type + " " + self.ua_heading


class Option(models.Model):
    question = models.ForeignKey(Question)
    ua_text = models.CharField(max_length=50)
    ru_text = models.CharField(max_length=50)

    def __str__(self):
        return self.ua_text


class Respondent(models.Model):
    LANGUAGES = (
        ("UA", "Ukrainian"),
        ("RU", "Russian"),
    )
    identity = models.CharField(max_length=50, primary_key=True)
    language = models.CharField(max_length=20, choices=LANGUAGES, default="UA")
    page = models.IntegerField(default=0)


class Condition(models.Model):
    page = models.ForeignKey(Page)
    option = models.ForeignKey(Option)


class Answer(models.Model):
    respondent = models.ForeignKey(Respondent)
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=200)


class Video(models.Model):
    page = models.ForeignKey(Page)
    url = models.CharField(max_length=200)


