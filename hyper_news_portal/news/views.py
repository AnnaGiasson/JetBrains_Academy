from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import Http404
import datetime as dt
import json


class WelcomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/index.html')


class MainPageView(View):

    def get(self, request, *args, **kwargs):

        with open(settings.NEWS_JSON_PATH, 'r') as file:
            news_stories = json.load(file)

        sorted_stories = sorted(news_stories, key=lambda s: s['created'],
                                reverse=True)
        # last_updated = sorted_stories[0]['created']
        last_updated = dt.datetime.strptime(sorted_stories[0]['created'],
                                            "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        return render(request, 'news/main.html',
                      context={"news_stories": sorted_stories,
                               "last_updated": last_updated})


class NewsStoryView(View):
    def read_story_info(self, link_number, most_recent=False):

        with open(settings.NEWS_JSON_PATH, 'r') as file:
            news_stories = json.load(file)

        if most_recent:
            return news_stories[-1]

        for story in news_stories:
            if str(story.get('link')) == link_number:
                return story.copy()

        return None

    def get(self, request, link_number=-1, *args, **kwargs):

        # get correct file
        story_info = self.read_story_info(link_number)

        if story_info is None:
            print(link_number)
            raise Http404

        # convert time str to datetime
        story_info['created'] = dt.datetime.strptime(story_info['created'],
                                                     "%Y-%m-%d %H:%M:%S")

        return render(request, 'news/news_story.html',
                      context={"story_info": story_info})


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/index.html')
