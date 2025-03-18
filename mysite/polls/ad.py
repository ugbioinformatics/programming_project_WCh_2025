from polls.models import Choice, Question
from django.utils import timezone


q = Question(question_text="w pliku ad mozna edytowac tresc pytania", pub_date=timezone.now())
q.save()
print(q)
idq = q.id
q1=Question.objects.get(pk=idq)
q1.choice_set.create(choice_text='Not much', votes=0)
q1.choice_set.create(choice_text='The sky', votes=0)
q1.save()


