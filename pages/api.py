import json

import datetime
import requests

from bcapps.cronjob_tasks import refresh_tokens
from pages.models import Page


class GetException(Exception):
    pass


class PutException(Exception):
    pass


class DeleteException(Exception):
    pass


class PageClient(object):
    """
    Docs https://docs.worldsecuresystems.com/reference/rest-apis/pages/pages.html
    API client for consuming BC's pages.
    BC get request:
    var request = $.ajax({
        url: "/webresources/api/v3/sites/current/pages",
        type: "GET",
        connection: "keep-alive",
        contentType: "application/json",
        headers: {
            "Authorization": $.cookie('access_token')
        }
        {
      "items": [
        {
         "id":9017917,
         "siteId":2163596,
         "workflowId":-1,
         "roleId":-1,
         "templateId":0,
         "parentId":-1,
         "livePageId":null,
         "pageUrl":"/about.html",
         "name":"About Us",
         "displayFileName":"about.html",
         "size":5281,
         "enabled":true,
         "startPage":false,
         "createDate":"2015-07-14T01:22:17.67",
         "lastUpdateDate":"2015-07-31T11:49:02.1",
         "releaseDate":"2015-07-31T11:49:02.1",
         "expiryDate":"9998-12-31T15:00:00",
         "displayable":true,
         "excludeFromSearch":false,
         "content":"Content here",
         "redirect301":"",
         "title":"About Us",
         "seoMetadataDescription":"Sample description"
        },
        {
         "id":9017918,
         "siteId":2163596,
         "workflowId":-1,
         "roleId":-1,
         "templateId":0,
         "parentId":-1,
         "livePageId":null,
         "pageUrl":"/contact",
         "name":"Contact",
         "displayFileName":"contact.html",
         "size":2810,
         "enabled":true,
         "startPage":false,
         "createDate":"2015-07-14T01:22:17.67",
         "lastUpdateDate":"2015-08-06T13:21:41.373",
         "releaseDate":"2015-08-03T00:00:00",
         "expiryDate":"9998-12-31T15:00:00",
         "displayable":true,
         "excludeFromSearch":false,
         "content": "Page2 content",
         "redirect301": "",
         "title": "Contact Us",
         "seoMetadataDescription": "Sample metadata"
        }
    ],
    "totalItemsCount": 2,
    "skip": 0,
    "limit": 10
    }

    """
    def __init__(self, site):
        self.base_url = site.secure_url
        self.pages_url = self.base_url + '/webresources/api/v3/sites/%s/pages' % site.site_id
        self.access_token = site.site_code.access_token
        self.site = site

    def commit_items(self, response_dict):
        """
        Accepts a dict like this:
        {"items":[{"id":18697,"siteId":8162,"roleId":-1,"name":"Annual Report 2007 ...}],"totalItemsCount":1010,"skip":0,"limit":10}
        :param response_dict: dict of items
        :return:
        """
        for item in response_dict['items']:
            try:
                p = Page.objects.get(page_id=item.get('id'))
            except Page.DoesNotExist:
                p = Page()
            exp_date = item.get('expiryDate')
            exp_date = datetime.datetime.strptime(exp_date.split('T')[0], '%Y-%m-%d')
            p.name = item.get('name')
            p.url = item.get('pageUrl')
            p.enabled = item.get('enabled')
            p.expires = exp_date
            p.page_id = item.get('id')
            p.content = item.get('content')
            p.title = item.get('title')
            p.template_id = item.get('templateId')
            p.seo_description = item.get('seoMetadataDescription')
            p.save()

    def get_items(self, url):
        headers = {"Authorization": self.site.site_code.access_token, 'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 401:
            refresh_tokens()
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp_dict = json.loads(resp.text)
            self.commit_items(resp_dict)
            return resp_dict["totalItemsCount"]
        raise GetException("There was an issue in GET for media items. Error: %s" % resp.text)

    def get_all_items(self):
        skip = 0
        limit = 10
        skip_url = self.pages_url + "?skip=%s&limit=%s" % (skip, limit)
        items_total = self.get_items(skip_url)
        pages = int(items_total/limit)
        for i in range(1, pages):
            next_url = self.pages_url + "?skip=%s&limit=%s" % (skip, limit)
            self.get_items(next_url)
            skip += limit

    def update_page(self, page):
        headers = {"Authorization": self.site.site_code.access_token, 'Content-Type': 'application/json'}
        page_url = self.pages_url + "/%s" % page.page_id
        expiry_date = page.expires.strftime('%Y-%m-%dT00:00:00')  # 9998-12-31T15:00:00
        data = json.dumps({'name': page.name, 'pageUrl': page.url, 'expiryDate': expiry_date, 'enabled': page.enabled,
                           'templateId': page.template_id})
        resp = requests.put(page_url, headers=headers, data=data)
        if resp.status_code == 401:
            refresh_tokens()
            resp = requests.put(page_url, headers=headers, data=data)
        if resp.status_code != 204 and resp.status_code != 200:
            raise PutException("Page could not be updated. Response code: %s. Message from the website: %s" % (resp.status_code, resp.text))
        return resp
