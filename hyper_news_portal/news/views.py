from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import Http404
import datetime as dt
import json


def format_date_string(date_str, format_code="%Y-%m-%d"):
    return dt.datetime.strptime(date_str, settings.DATETIME_STR_FORMAT).strftime(format_code)


class WelcomePageView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class MainPageView(View):

    def get(self, request, *args, **kwargs):

        with open(settings.NEWS_JSON_PATH, 'r') as file:
            news_stories = json.load(file)

        # filter by search term
        if request.GET.get('q'):
            filtered_stories = []

            for story in news_stories:
                if request.GET.get('q') in story["title"]:
                    print(story)
                    filtered_stories.append(story)
        else:
            filtered_stories = news_stories

        sorted_stories = sorted(filtered_stories, key=lambda s: s['created'], reverse=True)
        if sorted_stories:
            # last_updated = sorted_stories[0]['created']
            last_updated = format_date_string(sorted_stories[0]['created'])
        else:
            last_updated = ''
        for idx, item in enumerate(sorted_stories):
            sorted_stories[idx]['render_date'] = format_date_string(item['created'])

        return render(request, 'news/main.html', context={"news_stories": sorted_stories,
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
        story_info['created'] = dt.datetime.strptime(story_info['created'], "%Y-%m-%d %H:%M:%S")

        return render(request, 'news/news_story.html', context={"story_info": story_info})


class CreateNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_page.html')

    def post(self, request, *args, **kwargs):

        # open file
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            news_stories = json.load(file)

        # update file
        news_stories.append({
                             'title': request.POST.get('title'),
                             'text': request.POST.get('text'),
                             'created': dt.datetime.now().strftime(settings.DATETIME_STR_FORMAT),
                             'link': max([story['link'] for story in news_stories]) + 1,
                             })

        # save file
        with open(settings.NEWS_JSON_PATH, 'w') as file:
            json.dump(news_stories, file, indent=4)

        return redirect('/news/')
