# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.http import HttpResponse
import json
import datetime

class sCart(TemplateView):

	def post(self, request, *args, **kwargs):
		session = request.session

		session['cart'] = request.POST.get("set") or ""

		return HttpResponse( json.dumps({}), mimetype="application/json" )


	def get(self, request, *args, **kwargs):
		session = request.session

		if session.get("cart") == None:
			session['cart'] = ""

		return HttpResponse( json.dumps({}), mimetype="application/json" )