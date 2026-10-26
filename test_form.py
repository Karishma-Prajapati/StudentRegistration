import unittest
from pathlib import Path
from html.parser import HTMLParser


class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_found = False
        self.fields = set()
        self.submit_found = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "form" and attrs.get("id") == "registrationForm":
            self.form_found = True

        if tag == "input":
            field_id = attrs.get("id")
            if field_id:
                self.fields.add(field_id)

        if tag == "select":
            field_id = attrs.get("id")
            if field_id:
                self.fields.add(field_id)

        if tag == "button" and attrs.get("type") == "submit":
            self.submit_found = True


class TestStudentRegistration(unittest.TestCase):

    def setUp(self):
        html_file = Path(__file__).parent / "index.html"
        self.html = html_file.read_text(encoding="utf-8")

        self.parser = FormParser()
        self.parser.feed(self.html)

    def test_form_exists(self):
        self.assertTrue(
            self.parser.form_found,
            "Registration form not found"
        )

    def test_required_fields(self):
        required_fields = {
            "studentName",
            "rollNumber",
            "email",
            "course"
        }

        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.parser.fields,
                    f"Missing field: {field}"
                )

    def test_submit_button(self):
        self.assertTrue(
            self.parser.submit_found,
            "Submit button not found"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)