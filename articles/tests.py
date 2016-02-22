from django.test import TestCase
from django.contrib.auth.models import User
import os

from core import test_utils
from Iincho.settings import BASE_DIR
from .views import ArticleDetailAndCreateCommentView, ArticleCreateView
from .models import Article


class ArticleModelTest(TestCase):
    def setUp(self):
        test_utils.create_test_user(3)

    def test_titles_default_value(self):
        a1 = Article(owner=User.objects.get(pk=1), body='')
        a1.save()
        saved_items = Article.objects.all()
        self.assertEqual('no title', saved_items[0].title)

    def test_can_save_article_has_large_size_body(self):
        fp = os.path.join(BASE_DIR, 'articles/tests/20000chars.txt')

        a1 = Article(owner=User.objects.get(pk=1))
        f = open(fp)
        chars = f.read()
        f.close()

        a1.body = chars
        a1.save()
        saved_items = Article.objects.all()
        self.assertEqual(chars, saved_items[0].body)


class DetailViewTest(TestCase):
    def setUp(self):
        test_utils.create_test_user(3)
        self.a1 = Article(owner=User.objects.get(pk=1), body='spam')
        self.a1.save()

    def test_return_200_when_exists_article_view(self):
        res = self.client.get('/articles/{0}/'.format(self.a1.id))
        self.assertEqual(res.status_code, 200)

    def test_return_404_when_not_exists_article_view(self):
        res = self.client.get('/articles/{0}/'.format(999))
        self.assertEqual(res.status_code, 404)

    def test_use_detail_view(self):
        res = self.client.get('/articles/{0}/'.format(self.a1.id))
        self.assertEqual(
            res.resolver_match.func.__name__,
            ArticleDetailAndCreateCommentView.as_view().__name__)

    def test_passes_correct_article(self):
        Article.objects.create(owner=User.objects.get(pk=2), body='spam')
        correct_article = Article.objects.create(owner=User.objects.get(pk=1), body='ham')
        response = self.client.get('/articles/%d/' % (correct_article.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['article'], correct_article)


class CreateViewTest(TestCase):
    def setUp(self):
        test_utils.create_test_user(3)
        self.a1 = Article(owner=User.objects.get(pk=1), body='spam')
        self.a1.save()

    def test_redirects_when_not_loggedIn(self):
        res = self.client.get('/articles/new/', follow=True)
        self.assertRedirects(res, '/login/')

    def test_return_200_when_loggedIn(self):
        self.client.login(username='test_user_1', password='password_1')
        res = self.client.get('/articles/new/', follow=True)
        self.assertEqual(res.status_code, 200)
        self.client.logout()

    def test_use_create_view(self):
        self.client.login(username='test_user_1', password='password_1')
        res = self.client.get('/articles/new/')
        self.assertEqual(res.resolver_match.func.__name__, ArticleCreateView.as_view().__name__)
        self.client.logout()

    def test_redirects_after_post(self):
        self.client.login(username='test_user_1', password='password_1')
        res = self.client.post('/articles/new/',
                              data={'title': 'a new article', 'body': 'articles body'})

        self.assertEqual(res.status_code, 302)

    def test_create_a_new_article(self):
        self.client.login(username='test_user_1', password='password_1')
        res = self.client.post('/articles/new/',
                               data={'title': 'a new article', 'body': 'articles body'})
        id = int(str(res.url).split('/')[-2])
        obj = Article.objects.get(id=id)
        obj.title = 'a new article'
