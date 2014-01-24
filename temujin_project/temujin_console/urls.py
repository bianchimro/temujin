from django.conf.urls import patterns, include, url

from .views import TestCaseView

urlpatterns = patterns('',
    
    url(r'^test/(?P<template>.+)/$', TestCaseView.as_view(), name="temujin_test_case"),
    
)
