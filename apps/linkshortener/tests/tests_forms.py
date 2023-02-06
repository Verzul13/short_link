
# from django.test import TestCase

# from ..forms import LinkshortenerCreateForm


# class TestsForms(TestCase):
#     def test_linkshortener_create_form_ok(self):
#         # Корректные данные
#         form_data = {
#             'link': 'http://test.com',
#             'subpart': 'QWERTY'
#         }
#         form = LinkshortenerCreateForm(data=form_data)
#         self.assertTrue(form.is_valid())

#     def test_linkshortener_create_form_invalid_link(self):
#         #  error - передаем пустой url
#         form_data = {
#             'link': '',
#             'subpart': 'QWERTY'
#         }
#         form = LinkshortenerCreateForm(data=form_data)
#         self.assertFalse(form.is_valid())

#     def test_linkshortener_create_form_invalid_subpart(self):
#         # error - передаем некорректный subpart
#         form_data = {
#             'link': 'http://test.com',
#             'subpart': 'A'
#         }
#         form = LinkshortenerCreateForm(data=form_data)
#         self.assertFalse(form.is_valid())
