from django.db import models

# Create your models here.


class Questionnaire(models.Model):
    questionnaire_name = models.CharField(max_length=50)
    pub_date = models.DateTimeField()


class Page(models.Model):
    PAGE_TYPES = (
        ("Question", "Question"),
        ("Video", "Video"),
        ("Starting", "Starting"),
        ("Login", "Login"),
        ("Lottery", "Lottery")
    )

    page_number = models.IntegerField(default=0)
    page_type = models.CharField(max_length=50, choices=PAGE_TYPES)
    ua_page_title = models.CharField(max_length=50)
    ru_page_title = models.CharField(max_length=50)
    ua_page_heading = models.CharField(max_length=200, blank=True)
    ru_page_heading = models.CharField(max_length=200, blank=True)
    ua_page_text = models.CharField(max_length=2000, blank=True)
    ru_page_text = models.CharField(max_length=2000, blank=True)
    questionnaire = models.ForeignKey(Questionnaire)
    pub_date = models.DateTimeField()

    def __str__(self):
        return "Page №" + str(self.page_number) + " Title: " + self.page_title


class Question(models.Model):
    QUESTION_TYPES = (
        ("SimpleOpenQuestion", "SimpleOpenQuestion"),
        ("SimpleQuestionWithOneAnswer", "SimpleQuestionWithOneAnswer"),
        ("SimpleQuestionWithSeveralAnswers", "SimpleQuestionWithSeveralAnswers"),
        ("TableQuestion", "TableQuestion"),
        ("QuestionWithOptionsAndUserAnswer", "QuestionWithOptionsAndUserAnswer")
    )

    question_number = models.IntegerField(default=0)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    ua_question_heading = models.CharField(max_length=200)
    ru_question_heading = models.CharField(max_length=200)
    ua_question_text = models.CharField(max_length=500, blank=True)
    ru_question_text = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey(Page)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question_type + " " + self.question_heading


class Option(models.Model):
    question = models.ForeignKey(Question)
    option_text = models.CharField(max_length=50)

    def __str__(self):
        return self.option_text


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
    option = models.CharField(max_length=200)


class Video(models.Model):
    page = models.ForeignKey(Page)
    video_url = models.CharField(max_length=200)


