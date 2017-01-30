from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question, Respondent, Answer, Option, Page, Video, Condition
import random
from django.urls import reverse
# Create your views here.

class TemplateQuestion:

    def __init__(self, question, options):
        self.id = question.id
        self.heading = question.question_heading
        self.type = question.question_type
        self.text = question.question_text
        self.options = options

def skip_not_needed_pages(respondent):
    pass


def get_page(request):


    try:
        respondent = Respondent.objects.get(identity=request.COOKIES["sessionid"])

    except:
        # create session in db
        respondent = Respondent(identity=request.COOKIES["sessionid"], page=1)
        respondent.save()

    skip_not_needed_questions(respondent)
    needed_page = Page.objects.get(page_number=respondent.page)

    if (needed_page.page_type == "Video"):
        videos = Video.objects.filter(page=needed_page)
        video = random.choice(videos).video_url
        return render(request, 'Video.html', context={
            "page" : needed_page,
            "video_url" : video,
        })
    elif (needed_page.page_type == "Starting"):
        return render(request, "Greetings.html", context={
            "page" : needed_page,
        })
    elif (needed_page.page_type == "Login"):
        return render(request, "Login.html", context={
            "page": needed_page,
        })
    elif (needed_page.page_type == "Question"):

        questions_set = Question.objects.filter(page=needed_page)

        questions_for_templates = []

        for question in questions_set:
            options_set = Option.objects.filter(question=question)
            questions_for_templates.append(TemplateQuestion(question, options_set))

        context = {
            "page" : needed_page,
            "questions" : questions_for_templates,
        }

        return render(request, 'Question.html', context=context)


def answer(request):
    respondent = get_object_or_404(Respondent, identity=request.COOKIES["sessionid"])
    try:
        page = Page.objects.get(page_number=respondent.page)
        print(page.page_title)
        questions = Question.objects.filter(page=page)
        print(questions)
        for question in questions:
            print(question.id)
            user_answer = request.POST.getlist(str(question.id))
            print(user_answer)
            for option in user_answer:
                db_answer = Answer(respondent=respondent, question=question, option=option)
                db_answer.save()
    finally:
        respondent.page += 1
        respondent.save()
        return HttpResponseRedirect('/poll/')


