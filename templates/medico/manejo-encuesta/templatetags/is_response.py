from django import template
register = template.Library()

@register.filter
def get_responses(responses, pk):
    return responses.response.filter(answer_to__pk = pk)

@register.filter
def is_response(responses, pk):
    for response in responses:
        if int(response.answer_to.pk) == int(pk):
            print(response.answer_to.pk)
            return True
    return False
