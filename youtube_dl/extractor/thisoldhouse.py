# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor

from ..utils import (
    int_or_none
)

class ThisOldHouseIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?thisoldhouse\.com/(?:watch|how-to|tv-episode|(?:[^/]+/)?\d+)/(?P<id>[^/?#]+)'
    _TESTS = [{
        'url': 'https://www.thisoldhouse.com/how-to/how-to-build-storage-bench',
        'info_dict': {
            'id': '5dcdddf673c3f956ef5db202',
            'ext': 'mp4',
            'title': 'How to Build a Storage Bench',
            'description': 'In the workshop, Tom Silva and Kevin O\'Connor build a storage bench for an entryway.',
            'timestamp': 1442548800,
            'upload_date': '20150918',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://www.thisoldhouse.com/watch/arlington-arts-crafts-arts-and-crafts-class-begins',
        'only_matching': True,
    }, {
        'url': 'https://www.thisoldhouse.com/tv-episode/ask-toh-shelf-rough-electric',
        'only_matching': True,
    }, {
        'url': 'https://www.thisoldhouse.com/furniture/21017078/how-to-build-a-storage-bench',
        'only_matching': True,
    }, {
        'url': 'https://www.thisoldhouse.com/21113884/s41-e13-paradise-lost',
        'only_matching': True,
    }, {
        # iframe www.thisoldhouse.com
        'url': 'https://www.thisoldhouse.com/21083431/seaside-transformation-the-westerly-project',
        'only_matching': True,
    }]
    _ZYPE_TMPL = 'https://www.thisoldhouse.com/videos/zype/%s'

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)
        video_id = self._search_regex(
            r'<iframe[^>]+src=[\'"](?:https?:)?//(?:www\.)?thisoldhouse\.(?:chorus\.build|com)/videos/zype/([0-9a-f]{24})',
            webpage, 'video id')

        page_title = self._html_search_regex(r'<h1 class="c-page-title">(.+)<\/h1>', webpage, 'title')
        series = self._html_search_meta('author', webpage)
        season_number = int_or_none(self._search_regex(
            r'S(\d+)', page_title, 'season number',
            default=None))
        episode_number = int_or_none(self._search_regex(
            r'E(\d+)', page_title, 'episode number',
            default=None))
        title = self._search_regex(
            r': (.+)', page_title, 'episode title',
            default=None)

        if series:
            series = series.replace(' TV', '')

        test = self._request_webpage(self._ZYPE_TMPL % video_id, video_id)
        zype_url = test.geturl()

        return {
            '_type': 'url_transparent',
            'id': video_id,
            'title': title,
            'series': series,
            'season_number': season_number,
            'episode_number': episode_number,
            'url': zype_url,
            'ie_key': 'Zype',
        }
