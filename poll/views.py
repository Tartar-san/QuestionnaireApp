from django.shortcuts import render, get_object_or_404
from django.views.defaults import page_not_found, permission_denied, server_error
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import *
from .templates import *
from .google_spreadsheet_extractor import SpreadSheetUpdater
from .forms import FormWithCaptcha
import random
import os
# Create your views here.
spreadsheet_updater = SpreadSheetUpdater(filename=os.path.join(settings.STATICFILES_DIRS[0], 'poll/client_secret.json'))

def skip_not_needed_pages(respondent):
    page = Page.objects.get(number=respondent.page)
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
                                        text=option_text)
        if len(answers) == 0:
            respondent.page += 1
            respondent.save()
            return True
    # if all conditions are met it is not needed to skip page
    return False


def get_context(respondent):
    # get information from database
    db_page = Page.objects.get(number=respondent.page)
    db_videos = Video.objects.filter(page=db_page)
    db_questions = Question.objects.filter(page=db_page)

    # prepare information for template
    template_page = TemplatePage(db_page, respondent.language)

    if (len(db_videos) > 0):
        template_video = TemplateVideo(random.choice(db_videos))
    else:
        template_video = None


    template_questions = []
    # here we prepare questions and options for it
    for db_question in db_questions:
        db_options = Option.objects.filter(question=db_question)
        template_options = [TemplateOption(db_option, respondent.language) for db_option in db_options]
        print(template_options)
        template_questions.append(TemplateQuestion(db_question, template_options, respondent.language))

    context = {
        "page": template_page,
    }

    if (db_page.type in ["Question", "Lottery"]):
        context["questions"] = template_questions
    if (db_page.type in ["Starting"]):
        context["captcha_form"] = FormWithCaptcha()
    if (db_page.type in ["Video"]):
        context["video"] = template_video

        video_answer = Answer(question=db_questions.get(number=171),
                              respondent=respondent,
                              text=template_video.url)
        video_answer.save()
        spreadsheet_updater.add_answer(template_video.key_name,
                                       db_questions.get(number=171).id,
                                       respondent.spreadsheet_row)

    return context, db_page.type


def get_page(request):

    if (request.session.session_key is None):
        request.session.save()

    try:
        # try to get this respondent information
        respondent = Respondent.objects.get(identity=request.session.session_key)
    except:
        # create session in db
        respondent = Respondent(identity=request.session.session_key, page=1)
        respondent.save()
        spreadsheet_updater.add_respondent(respondent.spreadsheet_row)


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
        return render(request, "Question.html", context=context)
    elif (page_type == "FinalPage"):
        return render(request, "FinalPage.html", context=context)
    else:
        return page_not_found(request)


def post_answer(request):
    respondent = get_object_or_404(Respondent, identity=request.session.session_key)
    #try:
    page = Page.objects.get(number=respondent.page)
    questions = Question.objects.filter(page=page)
    if (page.type == "Login"):
        text_like = request.COOKIES["Like"]
        question_like = questions.get(ua_heading="Лайкнув")
        answer_like = Answer(respondent=respondent,
                             question=question_like,
                             text=text_like)
        answer_like.save()
        spreadsheet_updater.add_answer(str(text_like), question_like.id, respondent.spreadsheet_row)


        #shared = request.POST["Shared"] == "true"
    else:
        if (page.type == "Starting"):
            form = FormWithCaptcha(request.POST)
            if not form.is_valid():
                return HttpResponseRedirect('/poll/')
    # one page could contain several questions
        for question in questions:
         # some questions could have several answers
            user_answer = request.POST.getlist(str(question.id))
            print(question.id)
            spreadsheet_updater.add_answer(str(user_answer), question.id, respondent.spreadsheet_row)
            for option in user_answer:
                # allow user to choose preferred language
                if (question.type=="LanguageChoosing"):
                    respondent.language = {"Русский": "RU", "Українська": "UA"}[option]

                # save answer in database
                db_answer = Answer(respondent=respondent, question=question, text=option)
                db_answer.save()

    respondent.page += 1
    respondent.save()
    return HttpResponseRedirect('/poll/')
    #except:
    #    return server_error(request)


