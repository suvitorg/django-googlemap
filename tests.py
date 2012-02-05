# -*- coding: utf-8 -*-
from __future__ import with_statement

from django.test import TestCase

from googlemap.widgets import LocationWidget, LocationField


class GoogleMapTest(TestCase):
    def test_widget(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        widget = LocationWidget()

        rendered = widget.render('location', '55,55')

        self.assertTrue('input type="hidden" name="location"' in rendered)
        self.assertTrue('55' in rendered)

        rendered = widget.render('location', None)

        self.assertTrue('input type="hidden" name="location"' in rendered)

    def test_field(self):
        field = LocationField()

        field.clean('55,55')
        with self.assertRaises(ValueError):
            field.clean('55.55')
        with self.assertRaises(ValueError):
            field.clean('aaa')
        with self.assertRaises(TypeError):
            field.clean(None)
        with self.assertRaises(ValueError):
            field.clean('55,aaa')
