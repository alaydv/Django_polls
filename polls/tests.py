import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given "question_text",
    and with the given "pub_date"(negative for questions in the past, and
    positive for questions in the future) 
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(pk, choice_text, votes=0):
    """
    Create a choice that have the pk(primary key is a number) of a specific question
    with the given "choice_text" and with the given "votes"(votes starts in zero)
    """
    question = Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text=choice_text, votes=votes)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recently returns False for questions whose pud_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Cual es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_publishes_recently_with_present_questions(self):
        """
        was_published_recently returns True for questions whose pud_date is in the present
        """
        time = timezone.now()
        present_question = Question(question_text="¿Cual es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

    def test_was_publishes_recently_with_past_questions(self):
        """
        was_published_recently returns False for questions whose pud_date is in the past
        """
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="¿Cual es el mejor Course Director de Platzi?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
        

class QuestionIndexViesTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropiate message is displayed
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avaible.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_questions_with_future_pub_date(self):
        """
        If a question have a future date, then it isn't displayed
        """
        create_question("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are avaible.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        A question with past date have to be displayed
        """
        question = create_question("past question", days=-30)
        choice1 = create_choice(pk=question.id, choice_text="choice 1", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="choice 2", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
        If we have both questions(past and future), only past questions are displayed
        """
        future_question = create_question("future question", days=30)
        past_question = create_question("past question", days=-20)
        choice1 = create_choice(pk=past_question.id, choice_text="choice 1", votes=0)
        choice2 = create_choice(pk=past_question.id, choice_text="choice 2", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])


    def test_two_past_questions(self):
        """
        With two past questions, both are displayed
        """
        past_question1 = create_question("past question1", days=-30)
        choice1 = create_choice(pk=past_question1.id, choice_text="choice 1", votes=0)
        choice2 = create_choice(pk=past_question1.id, choice_text="choice 2", votes=0)
        past_question2 = create_question("past question2", days=-40)
        choice3 = create_choice(pk=past_question2.id, choice_text="choice 3", votes=0)
        choice4 = create_choice(pk=past_question2.id, choice_text="choice 4", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_questions(self):
        """
        With two future questions, both aren't displayed
        """
        future_question1 = create_question("future question1", days=40)
        future_question2 = create_question("future question2", days=50)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avaible.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_question_without_choices(self):
        """
        Quetions have no choices aren't displayed in the index view
        """
        question = create_question("Cuál es tu curso favorito?", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_question_with_choices(self):
        """
        Question with choices are displayed in the index view
        """
        question = create_question("Cuál es tu curso favorito?", days=-10)
        choice1 = create_choice(pk=question.id, choice_text="Curso Básico de Django", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Curso de Introducción a la Nube con Azure", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])

class QuestionDetailViewTest(TestCase):

    def test_future_questions(self):
        """
        The detail view of a question with a pub date in the future
        returns a 404 error(not found)
        """
        future_question = create_question("future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_questions(self):
        """
        The detail view with a pub date in the past display the 
        question's text
        """
        past_question = create_question("past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class ResultViewTest(TestCase):

    def test_with_past_question(self):
        """
        The result view with a pub date in the past display the 
        question's text
        """
        past_question = create_question("past question", days=-15)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_with_future_question(self):
        """
        Questions with a future date aren't displayed and this return a 404 error(not found) 
        until the date is the specified date
        """
        future_question = create_question("this is a future question", days=30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        