from django.db import models

# Create your models here.


class Questionnaire(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Page(models.Model):
    PAGE_TYPES = (
        ("Question", "Question"),
        ("Video", "Video"),
        ("Starting", "Starting"),
        ("Login", "Login"),
        ("Lottery", "Lottery"),
        ("FinalPage", "FinalPage")
    )

    # important field. defines order of pages
    number = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=PAGE_TYPES)
    ua_title = models.CharField(max_length=50)
    ru_title = models.CharField(max_length=50)
    ua_heading = models.TextField(max_length=500, blank=True)
    ru_heading = models.TextField(max_length=500, blank=True)
    ua_text = models.TextField(max_length=2000, blank=True)
    ru_text = models.TextField(max_length=2000, blank=True)
    questionnaire = models.ForeignKey(Questionnaire)

    def __str__(self):
        return "Questionnaire: " + str(self.questionnaire) + "|||  Page number: " + str(self.number)


class Question(models.Model):
    QUESTION_TYPES = (
        ("SimpleOpenQuestion", "SimpleOpenQuestion"),
        ("SimpleQuestionWithOneAnswer", "SimpleQuestionWithOneAnswer"),
        ("SimpleQuestionWithSeveralAnswers", "SimpleQuestionWithSeveralAnswers"),
        ("TableQuestion", "TableQuestion"),
        ("QuestionWithOptionsAndUserAnswer", "QuestionWithOptionsAndUserAnswer"),
        ("LanguageChoosing", "LanguageChoosing"),
        ("DateTimeChoosing", "DateTimeChoosing"),
        ("QuestionWithSeveralOptionsAndUserAnswer", "QuestionWithSeveralOptionsAndUserAnswer"),
        ("TableHeadingQuestion", "TableHeadingQuestion")
    )

    number = models.CharField(max_length=10, default="0")
    type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    ua_heading = models.CharField(max_length=200)
    ru_heading = models.CharField(max_length=200)
    ua_text = models.CharField(max_length=500, blank=True)
    ru_text = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey(Page)
    pub_date = models.DateTimeField()
    column_number = models.IntegerField(null=True)

    def __str__(self):
        return str(self.page) + "||| Question number: " + str(self.number) + " " + str(self.id)


class Option(models.Model):
    question = models.ForeignKey(Question)
    ua_text = models.CharField(max_length=50)
    ru_text = models.CharField(max_length=50)

    def __str__(self):
        return str(self.question) + "||| Option: " + self.ua_text

class Video(models.Model):
    key_name = models.CharField(max_length=200)
    page = models.ForeignKey(Page)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.key_name


class Respondent(models.Model):
    LANGUAGES = (
        ("UA", "Ukrainian"),
        ("RU", "Russian"),
    )
    LOTTERY_PAGES = (
        ("G", "generating"),
        ("M", "manual"),
        ("B", "both"),
    )
    identity = models.CharField(max_length=50)
    language = models.CharField(max_length=20, choices=LANGUAGES, default="UA")
    page = models.IntegerField(default=0)
    spreadsheet_row = models.AutoField(primary_key=True)
    lottery_number = models.CharField(max_length=10, default="0")
    video = models.ForeignKey(Video, null=True)
    lottery_page = models.CharField(max_length=10, choices=LOTTERY_PAGES, default="B")
    lottery_generated = models.CharField(max_length=10, null=True)
    refreshed_lottery = models.BooleanField(default=False)


    def __str__(self):
        return "Identity: " + self.identity \
               + " Language: " + self.language


class Condition(models.Model):
    page = models.ForeignKey(Page)
    option = models.ForeignKey(Option)

    def __str__(self):
        return "Show: " + str(self.page) \
               + " If: " + str(self.option)


class Answer(models.Model):
    respondent = models.ForeignKey(Respondent)
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=200)

    def __str__(self):
        return "Respondent: " + self.respondent.identity \
               + " Answer: " + self.text


