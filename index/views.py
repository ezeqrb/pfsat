from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Choices, Questions, Answer, Form, Responses
from paciente.models import Paciente,PacienteRealizaEncuesta
from medico.models import Medico,MedicoCreaEncuesta
from sat.views import es_medico, es_paciente
import json
import random
import string

# Create your views here.
def list_encuestas(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            forms = Form.objects.all().order_by("-updatedAt")
        elif es_medico(request.user):
            medico = Medico.objects.get(user_id=request.user.id)
            forms_all = Form.objects.all().order_by("-updatedAt")
            forms_medicos = MedicoCreaEncuesta.objects.all()
            forms_otros_medicos = [form.encuesta_id for form in forms_medicos if form.medico.id != medico.id] #me quedo con los ids de los forms creados por otros médicos
            forms = [form for form in forms_all if (form.id not in forms_otros_medicos)] #me quedo con los forms del médico y de los admin
        else: #es paciente
            paciente = Paciente.objects.get(user_id=request.user.id)
            forms = Form.objects.filter(medicocreaencuesta__medico__pacientes=paciente.id,status='p').order_by("-updatedAt")            
            responses = []
            encuestas_respondidas = []
            for form in forms:
                response = Responses.objects.filter(response_to=form.id, responder_email=request.user.email) 
                if response.count() > 0:
                    for r in response: 
                        responses.append(r) 
                else:
                    responses.append(form.id)           
                encuestas_realizadas = PacienteRealizaEncuesta.objects.filter(paciente_id=paciente.id,encuesta_id=form.id)
                if encuestas_realizadas.count() > 0:
                    for encuesta in encuestas_realizadas: #el paciente puede responder una encuesta más de una vez
                        encuestas_respondidas.append(encuesta)
                else:
                    encuestas_respondidas.append(form.id)
            encuestas_hechas = list(zip(encuestas_respondidas,responses))
            for e,r in encuestas_hechas:
                print(e,r)
                    

            return render(request, "medico/manejo-encuesta/list-encuestas.html", {"forms": forms,'encuestas_con_respuestas':encuestas_hechas})
        return render(request, "medico/manejo-encuesta/list-encuestas.html", {"forms": forms})
    else:
        messages.error(request,'Permiso denegado: Debe iniciar sesión!')
        return redirect('index')

def view_encuesta(request,code):
    if request.user.is_authenticated:
        try:
            formInfo = Form.objects.get(code = code)
        except Form.DoesNotExist:
            return render(request,"error/404.html")
        
        return render(request, "medico/manejo-encuesta/view-encuesta.html", {"code": code,"form": formInfo})
    else:
        messages.error(request,'Permiso denegado: Debe iniciar sesión!')
        return redirect('index')
    
def add_encuesta(request):
    if request.user.is_staff or es_medico(request.user):
        if request.method == "POST":
            data = json.loads(request.body)
            title = data["title"]
            code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
            choices = Choices(choice = "")
            choices.save()
            question = Questions(question_type = "checkbox", question= "", required= False)
            question.save()
            question.choices.add(choices)
            question.save()
            form = Form(code = code, title = title)
            form.save()
            form.questions.add(question)
            form.save()
            if es_medico(request.user):
                medico = Medico.objects.get(user_id=request.user.id)
                nv_encuesta = MedicoCreaEncuesta.objects.create(medico_id=medico.id,encuesta_id=form.id)
            return JsonResponse({"message": "Sucess", "code": code})
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

def edit_encuesta(request, code):
    if request.user.is_staff or es_medico(request.user):
        formInfo = Form.objects.filter(code = code)
        if formInfo.count() == 0:
            return render(request,'error/404.html')
        else: formInfo = formInfo[0]
        return render(request, "medico/manejo-encuesta/edit_encuesta.html", {"code": code,"form": formInfo})
    else:
        return render(request,"error/403.html")
    
def edit_title(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data["title"]) > 0:
            formInfo.title = data["title"]
            formInfo.save()
        else:
            formInfo.title = formInfo.title[0]
            formInfo.save()
        return JsonResponse({"message": "Success", "title": formInfo.title})

def edit_description(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.description = data["description"]
        formInfo.save()
        return JsonResponse({"message": "Success", "description": formInfo.description})

def edit_bg_color(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.background_color = data["bgColor"]
        formInfo.save()
        return JsonResponse({"message": "Success", "bgColor": formInfo.background_color})

def edit_text_color(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.text_color = data["textColor"]
        formInfo.save()
        return JsonResponse({"message": "Success", "textColor": formInfo.text_color})

def edit_setting(request, code):
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.collect_email = data["collect_email"]
        formInfo.is_quiz = data["is_quiz"]
        formInfo.authenticated_responder = data["authenticated_responder"]
        formInfo.confirmation_message = data["confirmation_message"]
        formInfo.edit_after_submit = data["edit_after_submit"]
        formInfo.allow_view_score = data["allow_view_score"]
        formInfo.save()
        return JsonResponse({'message': "Success"})

def delete_form(request, code):
    formInfo = Form.objects.filter(code = code)
    # chequeo que existe
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: 
        formInfo = formInfo[0]
    
    # elimino preguntas y respuestas asociadas
    for i in formInfo.questions.all():
        for j in i.choices.all():
            j.delete()
        i.delete()
        for i in Responses.objects.filter(response_to = formInfo):
            for j in i.response.all():
                j.delete()
            i.delete()
    formInfo.delete()
    messages.success(request,'Encuesta eliminada con éxito!')
    return redirect('list_encuestas')
        
def edit_question(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data["id"]
        question = Questions.objects.filter(id = question_id)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else: question = question[0]
        question.question = data["question"]
        question.question_type = data["question_type"]
        question.required = data["required"]
        if(data.get("score")): question.score = data["score"]
        if(data.get("answer_key")): question.answer_key = data["answer_key"]
        question.save()
        return JsonResponse({'message': "Success"})

def edit_choice(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        choice_id = data["id"]
        choice = Choices.objects.filter(id = choice_id)
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else: choice = choice[0]
        choice.choice = data["choice"]
        if(data.get('is_answer')): choice.is_answer = data["is_answer"]
        choice.save()
        return JsonResponse({'message': "Success"})

def add_choice(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices(choice="")
        choice.save()
        formInfo.questions.get(pk = data["question"]).choices.add(choice)
        formInfo.save()
        return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id})

def remove_choice(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]

    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices.objects.filter(pk = data["id"])
        if choice.count() == 0:
            return render(request,"error/404.html")
        else: choice = choice[0]
        choice.delete()
        return JsonResponse({"message": "Success"})

def get_choice(request, code, question):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    if request.method == "GET":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return render(request,'error/404.html')
        else: question = question[0]
        choices = question.choices.all()
        choices = [{"choice":i.choice, "is_answer":i.is_answer, "id": i.id} for i in choices]
        return JsonResponse({"choices": choices, "question": question.question, "question_type": question.question_type, "question_id": question.id})

def add_question(request, code):
    formInfo = Form.objects.filter(code = code)

    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    if request.method == "POST":
        choices = Choices(choice = "")
        choices.save()
        question = Questions(question_type = "checkbox", question= "", required= False)
        question.save()
        question.choices.add(choices)
        question.save()
        formInfo.questions.add(question)
        formInfo.save()
        return JsonResponse({'question': {'question': "", "question_type": "checkbox", "required": False, "id": question.id}, 
        "choices": {"choice": "", "is_answer": False, 'id': choices.id}})


def repeat_question(request, code, question):
    formInfo = Form.objects.filter(code = code)

    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    if request.method == "POST":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return render(request,'error/404.html')
        else: question = question[0]
        nueva = Questions(question_type = question.question_type, question = question.question)
        choices = Choices(choice = question.choices)
        choices.save()
        nueva.save()
        nueva.choices.add(choices)
        nueva.save()
        print('hola')
        formInfo.questions.add(nueva)
        formInfo.save()
        choices_list = []
        for choice in question.choices.all():
            choices_list.append({
            'choice': choice.choice,
            'is_answer': False,
            'id': choice.id,
        })
        return JsonResponse({'question': {'question': nueva.question, "question_type": nueva.question_type, "required": False, "id": question.id}, 
        "choices": choices_list})


def delete_question(request, code, question):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    if request.method == "DELETE":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return render(request,'error/404.html')
        else: question = question[0]
        for i in question.choices.all():
            i.delete()
            question.delete()
    return JsonResponse({"message": "Success"})
    
def publish_encuesta(request,code):
    if request.user.is_authenticated:
        try:
            formInfo = Form.objects.get(code=code)
        except Form.DoesNotExist:
            return render(request,'error/404.html')
    
        if es_medico(request.user) or request.user.is_staff:
            formInfo.status = 'p'
            formInfo.save()
        else: #si no es médico ni admin, es paciente
            paciente = Paciente.objects.get(user_id=request.user.id)
            try:
                encuesta_completada = PacienteRealizaEncuesta.objects.get(paciente=paciente.id,encuesta=formInfo.id,estado='b')
                encuesta_completada.estado = 'p'
                encuesta_completada.save()
            except:
                messages.error(request,"Hay más de una misma encuesta en borrador. Debe eliminar la que no corresponda!")
        messages.success(request,'Encuesta publicada con éxito!')
        return redirect('list_encuestas')
    else:
        messages.error(request,'Permiso denegado: Debe iniciar sesión!')
        return redirect('index')

def unpublish_encuesta(request,code):
    if request.user.is_authenticated:
        try:
            formInfo = Form.objects.get(code=code)
        except Form.DoesNotExist:
            return render(request,'error/404.html')
    
        if es_medico(request.user) or request.user.is_staff:
            formInfo.status = 'b'
            formInfo.save()
            messages.success(request,'Encuesta pasada a Borrador con éxito!')
        else:
            messages.error(request,'Permiso denegado: Debe iniciar sesión!')
        return redirect('list_encuestas')
    else:
        messages.error(request,'Permiso denegado: Debe iniciar sesión!')
        return redirect('index')

def reassign_encuesta(request,code):
    if es_medico(request.user):
        formInfo = Form.objects.filter(code = code)
        if formInfo.count() == 0:
            return render(request,'error/404.html')
        else: formInfo = formInfo[0]

        medico = Medico.objects.get(user_id=request.user.id)
        mis_pacientes = Paciente.objects.filter(tratamiento__medico=medico.id,status=True,baja=False).distinct()
        for paciente in mis_pacientes:
            nv_encuesta = PacienteRealizaEncuesta.objects.create(encuesta_id=formInfo.id,paciente_id=paciente.id,estado='r')
        messages.success(request,'Encuesta reasignada con éxito!')
        return redirect('list_encuestas')
    else:
        messages.error(request,'Permiso denegado!')
        return redirect('afterlogin')

def score(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]

    if not formInfo.is_quiz:
        messages.error(request,'Error: La encuesta no tiene puntajes!')
        return HttpResponseRedirect(reverse("edit_encuesta", args = [code]))
    else:
        return render(request, "medico/manejo-encuesta/score.html", {"form": formInfo})

def edit_score(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]

    if not formInfo.is_quiz:
        messages.error(request,'Error: La encuesta no tiene puntajes!')
        return HttpResponseRedirect(reverse("edit_encuesta", args = [code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question_id = data["question_id"]
            question = formInfo.questions.filter(id = question_id)
            if question.count() == 0:
                messages.error(request,'Error: La encuesta no tiene preguntas!')
                return HttpResponseRedirect(reverse("edit_encuesta", args = [code]))
            else: question = question[0]
            score = data["score"]
            if score == "": score = 0
            question.score = score
            question.save()
            return JsonResponse({"message": "Success"})
        else:
            return JsonResponse({'message': 'Metodo no permitido'}, status=405)

def answer_key(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,"error/404.html")
    else: formInfo = formInfo[0]
    
    if not formInfo.is_quiz:
        messages.error(request,'Error: La encuesta no tiene preguntas!')
        return HttpResponseRedirect(reverse("edit_encuesta", args = [code]))
    else:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                question = Questions.objects.filter(id = data["question_id"])
                if question.count() == 0: return HttpResponseRedirect(reverse("edit_encuesta", args = [code]))
                else: question = question[0]
                if question.question_type == "short" or question.question_type == "paragraph":
                    question.answer_key = data["answer_key"]
                    question.save()
                else:
                    for i in question.choices.all():
                        i.is_answer = False
                        i.save()
                    if question.question_type == "checkbox":
                        choice = question.choices.get(pk = data["answer_key"])
                        choice.is_answer = True
                        choice.save()
                    else:
                        for i in data["answer_key"]:
                            choice = question.choices.get(id = i)
                            choice.is_answer = True
                            choice.save()
                    question.save()
                    return JsonResponse({'message': "success"})
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=500)
        else:
            return JsonResponse({'message': 'Metodo no permitido'}, status=405)

def feedback(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        messages.error(request,'Error: La encuesta no tiene preguntas!')
    else: formInfo = formInfo[0]

    if not formInfo.is_quiz:
        messages.error(request,'Error: La encuesta no tiene puntaje!')
        return HttpResponseRedirect(reverse("edit_encuesta", args = [code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = formInfo.questions.get(id = data["question_id"])
            question.feedback = data["feedback"]
            question.save()
            return JsonResponse({'message': "success"})
        else:
            return JsonResponse({'message': 'Metodo no permitido'}, status=405)

def complete_encuesta(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]
    
    if request.user.is_authenticated:
        if es_paciente(request.user):
            paciente = Paciente.objects.get(user_id=request.user.id)
            try: # si la encuesta fue reasignada, no creo una nueva
                encuesta_reasignada = PacienteRealizaEncuesta.objects.get(paciente_id=paciente.id,encuesta_id=formInfo.id,estado='r')
                encuesta_reasignada.estado = 'b'
                encuesta_reasignada.save()
            except: # si la encuesta no fue reasignada, creo una nueva
                nv_encuesta = PacienteRealizaEncuesta.objects.create(paciente_id=paciente.id,encuesta_id=formInfo.id)
    else:
        if formInfo.authenticated_responder:
            messages.error(request,"Permiso denegado: Debe iniciar sesión!")
            return redirect('index')
    return render(request, "medico/manejo-encuesta/complete_encuesta.html", {"form": formInfo})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def submit_form(request, code):
    formInfo = Form.objects.filter(code = code)

    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))
        #response = Responses.objects.create(response_code = code, response_to = formInfo, responder_ip = request.user.id)
        if formInfo.authenticated_responder:
            response = Responses(response_code = code, response_to = formInfo, responder_ip = get_client_ip(request), responder_email=request.user.email)
        else:
            if not formInfo.collect_email:
                response = Responses(response_code = code, response_to = formInfo, responder_ip = get_client_ip(request))
            else:
                response = Responses(response_code = code, response_to = formInfo, responder_ip = get_client_ip(request), responder_email=request.POST["email-address"])
        response.save()
        for i in request.POST:
            #Excluding csrf token
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = formInfo.questions.get(id = i)
            for j in request.POST.getlist(i):
                answer = Answer.objects.create(answer=j, answer_to = question)
                answer.save()
                response.response.add(answer)
                response.save()
        #return render(request, "index/form_response.html", {"form": formInfo, "code": code})
        messages.success(request,f"{formInfo.confirmation_message}")
        if request.user.is_authenticated:
            messages.info(request,'Tenga en cuenta que si desea envíar la encuesta a su médico, debe presionar el ícono "Publicar" que se encuentra en Acciones.')
            return redirect('list_encuestas')
        else:
            return redirect('index')
        #return render(request, "medico/manejo-encuesta/form_response.html", {"form": formInfo, "code": code})

def responses(request, code):
    formInfo = Form.objects.filter(code = code)

    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    try:
        responsesSummary = []
        choiceAnswered = {}
        filteredResponsesSummary = {}
        for question in formInfo.questions.all():
            answers = Answer.objects.filter(answer_to = question.id)
            if question.question_type == "checkbox" or question.question_type == "multiple choice":
                choiceAnswered[question.question] = choiceAnswered.get(question.question, {})
                for answer in answers:
                    choice = answer.answer_to.choices.get(id = answer.answer).choice
                    choiceAnswered[question.question][choice] = choiceAnswered.get(question.question, {}).get(choice, 0) + 1
            responsesSummary.append({"question": question, "answers":answers })
        for answr in choiceAnswered:
            filteredResponsesSummary[answr] = {}
            keys = choiceAnswered[answr].values()
            for choice in choiceAnswered[answr]:
                filteredResponsesSummary[answr][choice] = choiceAnswered[answr][choice]
        return render(request, "medico/manejo-encuesta/responses.html", {
            "form": formInfo,
            "responses": Responses.objects.filter(response_to = formInfo),
            "responsesSummary": responsesSummary,
            "filteredResponsesSummary": filteredResponsesSummary
        })
    except:
        messages.error(request,"Error al acceder a las respuestas de la encuesta!")
        return redirect('list_encuestas')

def response(request, code, response_code):
    formInfo = Form.objects.filter(code = code)

    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    total_score = 0
    score = 0
    responseInfo = Responses.objects.filter(response_code = response_code)
    if responseInfo.count() == 0:
        return render(request,'error/404.html')
    else: responseInfo = responseInfo[0]
    if formInfo.is_quiz:
        for i in formInfo.questions.all():
            total_score += i.score
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "short" or i.answer_to.question_type == "paragraph":
                if i.answer == i.answer_to.answer_key: score += i.answer_to.score
            elif i.answer_to.question_type == "checkbox":
                answerKey = None
                for j in i.answer_to.choices.all():
                    if j.is_answer: answerKey = j.id
                if answerKey is not None and int(answerKey) == int(i.answer):
                    score += i.answer_to.score
        _temp = []
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "multiple choice" and i.answer_to.pk not in _temp:
                answers = []
                answer_keys = []
                for j in responseInfo.response.filter(answer_to__pk = i.answer_to.pk):
                    answers.append(int(j.answer))
                    for k in j.answer_to.choices.all():
                        if k.is_answer and k.pk not in answer_keys: answer_keys.append(k.pk)
                    _temp.append(i.answer_to.pk)
                if answers == answer_keys: score += i.answer_to.score
    #if formInfo.is_quiz:return HttpResponseRedirect(reverse("response", args = [formInfo.code, response.response_code]))
    return render(request, "medico/manejo-encuesta/response.html", {
        "form": formInfo,
        "response": responseInfo,
        "score": score,
        "total_score": total_score
    })

def edit_response(request, code, response_code):
    formInfo = Form.objects.filter(code = code)

    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]
    
    response = Responses.objects.filter(response_code = response_code, response_to = formInfo)
    if response.count() == 0:
        return render(request,'error/404.html')
    else: response = response[0]
    
    if request.method == "POST":
        if formInfo.authenticated_responder and not response.responder_ip:
            response.save()
        if formInfo.collect_email:
            response.responder_email = request.POST["email-address"]
            response.save()
        #Deleting all existing answers
        for i in response.response.all():
            i.delete()
        for i in request.POST:
            #Excluding csrf token and email address
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = formInfo.questions.get(id = i)
            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to = question)
                answer.save()
                response.response.add(answer)
                response.save()
        messages.success(request,f"{formInfo.confirmation_message}")
        messages.info(request,'Tenga en cuenta que si desea envíar la encuesta a su médico, debe presionar el ícono "Publicar" que se encuentra en Acciones.')
        return redirect('list_encuestas')
        #return render(request, "medico/manejo-encuesta/form_response.html", {"form": formInfo,"code": response.response_code})   
    return render(request, "medico/manejo-encuesta/edit_response.html", {"form": formInfo,"response": response})

def contact_form_template(request):

    # Create a blank form API
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        name = Questions(question_type = "short", question= "Nombre", required= True)
        name.save()
        email = Questions(question_type="short", question = "Correo electrónico", required = True)
        email.save()
        address = Questions(question_type="paragraph", question="Dirección", required = True)
        address.save()
        phone = Questions(question_type="short", question="Teléfono", required = False)
        phone.save()
        comments = Questions(question_type = "paragraph", question = "Comentarios", required = False)
        comments.save()
        form = Form(code = code, title = "Información de Contacto", background_color="#e2eee0", allow_view_score = False, edit_after_submit = True)
        form.save()
        form.questions.add(name)
        form.questions.add(email)
        form.questions.add(address)
        form.questions.add(phone)
        form.questions.add(comments)
        form.save()
        return JsonResponse({"message": "Sucess", "code": code})

def customer_feedback_template(request):

    # Create a blank form API
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        comment = Choices(choice = "")
        comment.save()
        question = Choices(choice = "")
        question.save()
        bug = Choices(choice = "")
        bug.save()
        feature = Choices(choice = "")
        feature.save()
        feedback_type = Questions(question = "", question_type="checkbox", required=False)
        feedback_type.save()
        feedback_type.choices.add(comment)
        feedback_type.choices.add(bug)
        feedback_type.choices.add(question)
        feedback_type.choices.add(feature)
        feedback_type.save()
        feedback = Questions(question = "", question_type="paragraph", required=True)
        feedback.save()
        suggestion = Questions(question = "", question_type="paragraph", required=False)
        suggestion.save()
        name = Questions(question = "", question_type="short", required=False)
        name.save()
        email = Questions(question= "", question_type="short", required=False)
        email.save()
        form = Form(code = code, title = "",  background_color="#e2eee0", confirmation_message="Gracias por sus comentarios! Los tendremos en cuenta...",
        description = "Por favor, agregue un comentario que nos ayude a mejorar!", allow_view_score = False, edit_after_submit = True)
        form.save()
        form.questions.add(feedback_type)
        form.questions.add(feedback)
        form.questions.add(suggestion)
        form.questions.add(name)
        form.questions.add(email)
        return JsonResponse({"message": "Sucess", "code": code})

def event_registration_template(request):
    # Create a blank form API
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        name = Questions(question="", question_type= "short", required=False)
        name.save()
        email = Questions(question = "", question_type="short", required=True)
        email.save()
        organization = Questions(question = "", question_type= "short", required=True)
        organization.save()
        day1 = Choices(choice="")
        day1.save()
        day2 = Choices(choice= "")
        day2.save()
        day3 = Choices(choice= "")
        day3.save()
        day = Questions(question="", question_type="multiple choice", required=True)
        day.save()
        day.choices.add(day1)
        day.choices.add(day2)
        day.choices.add(day3)
        day.save()
        dietary_none = Choices(choice="")
        dietary_none.save()
        dietary_vegetarian = Choices(choice="")
        dietary_vegetarian.save()
        dietary_kosher = Choices(choice="")
        dietary_kosher.save()
        dietary_gluten = Choices(choice = "")
        dietary_gluten.save()
        dietary = Questions(question = "", question_type="checkbox", required = True)
        dietary.save()
        dietary.choices.add(dietary_none)
        dietary.choices.add(dietary_vegetarian)
        dietary.choices.add(dietary_gluten)
        dietary.choices.add(dietary_kosher)
        dietary.save()
        accept_agreement = Choices(choice = "")
        accept_agreement.save()
        agreement = Questions(question = "", question_type="multiple choice", required=True)
        agreement.save()
        agreement.choices.add(accept_agreement)
        agreement.save()
        form = Form(code = code, title = "Registro de Evento", background_color="#fdefc3", 
        confirmation_message="Hemos recibido su registro.\n\
Insert other information here.\n\
\n\
Save the link below, which can be used to edit your registration up until the registration closing date.",
        description = "Event Timing: January 4th-6th, 2016\n\
Event Address: 123 Your Street Your City, ST 12345\n\
Contact us at (123) 456-7890 or no_reply@example.com", edit_after_submit=True, allow_view_score=False)
        form.save()
        form.questions.add(name)
        form.questions.add(email)
        form.questions.add(organization)
        form.questions.add(day)
        form.questions.add(dietary)
        form.questions.add(agreement)
        form.save()
        return JsonResponse({"message": "Sucess", "code": code})

def delete_responses(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return render(request,'error/404.html')
    else: formInfo = formInfo[0]

    if request.method == 'DELETE':
        responses = Responses.objects.filter(response_to = formInfo)
        if responses:
            # elimino respuestas
            for response in responses:
                for i in response.response.all():
                    i.delete()
                response.delete()
            # elimino las encuestas publicadas por los pacientes
            forms_pacientes = PacienteRealizaEncuesta.objects.filter(encuesta_id = formInfo.id,estado='p')
            for form_paciente in forms_pacientes:
                form_paciente.delete()
            messages.success(request,'Respuestas eliminadas con éxito!')
            return redirect('list_encuestas')
        else: messages.info(request,'Todavía no se registraron respuestas!')
    return redirect('reponses')

# Error handler
def FourZeroThree(request):
    return render(request, "error/403.html")

def FourZeroFour(request):
    return render(request, "error/404.html")
