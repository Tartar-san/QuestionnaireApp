from django.shortcuts import render, get_object_or_404
from django.views.defaults import page_not_found, permission_denied, server_error
from django.http import HttpResponseRedirect
from .models import *
from .templates import *
import random
# Create your views here.


def skip_not_needed_pages(respondent):
    page = Page.objects.get(page_number=respondent.page)
    conditions = Condition.objects.filter(page=page)

    # check if all of conditions are met. if not - skip page
    for condition in conditions:
        # if respondent chose some language then his answers in this language
        if (respondent.language == "RU"):
            option_text = condition.option.ru_text
        elif (respondent.language == "UA"):
            option_text = condition.option.ua_text

        answers = Answer.objects.filter(respondent=respondent,
                                        question=condition.option.question,
                                        option=option_text)
        if len(answers) == 0:
            respondent.page += 1
            respondent.save()
            return True
    # if all conditions are met it is not needed to skip page
    return False


def get_context(respondent):
    # get information from database
    db_page = Page.objects.get(page_number=respondent.page)
    db_videos = Video.objects.filter(page=db_page)
    db_questions = Question.objects.filter(page=db_page)
    # prepare information for template
    template_page = TemplatePage(db_page, respondent)
    template_video = TemplatePage(random.choice(db_videos))
    template_questions = []
    # here we prepare questions and options for it
    for db_question in db_questions:
        db_options = Option.objects.filter(question=db_question)
        template_options = [TemplateOption(db_option, respondent.language) for db_option in db_options]
        template_questions.append(TemplateQuestion(db_question, template_options, respondent.language))

    context = {
        "page": template_page,
        "questions": template_questions,
        "video": template_video,
    }

    return context, template_page.type


def get_page(request):

    try:
        # try to get this respondent information
        respondent = Respondent.objects.get(identity=request.COOKIES["sessionid"])
    except:
        # create session in db
        respondent = Respondent(identity=request.COOKIES["sessionid"], page=1)
        respondent.save()

    # skip pages until the one respondent should see
    while skip_not_needed_pages(respondent):
        pass

    context, page_type = get_context(respondent)

    if (page_type == "Starting"):
        return render(request, "Starting.html", context=context)
    elif (page_type == "Login"):
        return render(request, "Login.html", context=context)
    elif (page_type == "Question"):
        return render(request, "Question.html", context=context)
    elif (page_type == "Video"):
        return render(request, "Video.html", context=context)
    elif (page_type == "Lottery"):
        return render(request, "Lottery.html", context=context)
    else:
        return page_not_found(request)


def post_answer(request):
    respondent = get_object_or_404(Respondent, identity=request.COOKIES["sessionid"])
    try:
        page = Page.objects.get(page_number=respondent.page)
        questions = Question.objects.filter(page=page)
        # one page could contain several questions
        for question in questions:
            # some questions could have several answers
            user_answer = request.POST.getlist(str(question.id))
            for option in user_answer:
                # allow user to choose preferred language
                if (question.type=="LanguageChoosing"):
                    respondent.language = {"Русский": "RU", "Українська": "UA"}[option]

                # save answer in database
                db_answer = Answer(respondent=respondent, question=question, option=option)
                db_answer.save()

        respondent.page += 1
        respondent.save()
        return HttpResponseRedirect('/poll/')
    except:
        return server_error(request)


