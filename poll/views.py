from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *
from .templates import *
import random
# Create your views here.



def skip_not_needed_pages(respondent):
    page = Page.objects.get(page_number=respondent.page)
    conditions = Condition.objects.filter(page=page)

    for condition in conditions:
        answers = Answer.objects.filter(respondent=respondent, question=condition.option.question, option=condition.option.option_text)
        if len(answers) == 0:
            respondent.page += 1
            respondent.save()
            return True

    return False


def get_page(request):

    try:
        respondent = Respondent.objects.get(identity=request.COOKIES["sessionid"])

    except:
        # create session in db
        respondent = Respondent(identity=request.COOKIES["sessionid"], page=1)
        respondent.save()

    while skip_not_needed_pages(respondent):
        pass

    db_page = Page.objects.get(page_number=respondent.page)
    db_videos = Video.objects.filter(page=db_page)
    db_questions = Question.objects.filter(page=db_page)






def post_answer(request):
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
                if (option=="Русский"):
                    respondent.language = "RU"
                    respondent.save()
                db_answer = Answer(respondent=respondent, question=question, option=option)
                db_answer.save()
    finally:
        respondent.page += 1
        respondent.save()
        return HttpResponseRedirect('/poll/')


