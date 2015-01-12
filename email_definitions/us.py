import pysistence as immutable

import mail_renderer as mr

from data_source import BusinessDataSource, \
	CommentIsFreeDataSource, CultureDataSource, TopStoriesDataSource, \
	VideoDataSource
from data_source import MultiContentDataSource, MostSharedCountInterpolator, MostSharedDataSource

from data_sources import us as data
from data_sources import technology as tech_data

from ophan_calls import OphanClient, MostSharedFetcher

clientUS = mr.clientUS
ophan_client = OphanClient(mr.ophan_base_url, mr.ophan_key)

class DailyEmailUS(mr.EmailTemplate):
    recognized_versions = immutable.make_list('v1', 'v3', 'v6', 'v7')

    ad_tag = 'email-guardian-today-us'
    ad_config = {
        'leaderboard_v1': 'Top',
        'leaderboard_v2': 'Bottom'
    }

    base_data_sources = immutable.make_dict({
        'business': BusinessDataSource(clientUS),
        'money': data.USMoneyDataSource(clientUS),
        'technology': tech_data.TechnologyDataSource(clientUS),
        'sport': data.SportUSDataSource(clientUS),
        'comment': CommentIsFreeDataSource(clientUS),
        'culture': CultureDataSource(clientUS),
        'top_stories': TopStoriesDataSource(clientUS),
        'video': VideoDataSource(clientUS),
    })

    most_shared_us = MostSharedDataSource(
                most_shared_fetcher=MostSharedFetcher(ophan_client, country='us'),
                multi_content_data_source=MultiContentDataSource(client=clientUS, name='most_shared_us'),
                shared_count_interpolator=MostSharedCountInterpolator()
            )

    data_sources = immutable.make_dict({
        'v1': base_data_sources,
        'v3': base_data_sources,
        'v6': base_data_sources.using(
            most_shared_us = most_shared_us
        ),
        'v7': base_data_sources.using(
            most_shared_us = most_shared_us
        ),
    })

    base_priorities = immutable.make_list(('top_stories', 6),
        ('video', 3), ('sport', 3), ('comment', 3),
        ('culture', 3), ('business', 2), ('money', 2),
        ('technology', 2), ('most_shared_us', 6), )

    priority_list = immutable.make_dict({
        'v1': [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)],
        'v3': [('top_stories', 6), ('video', 3), ('sport', 3), ('comment', 3),
                           ('culture', 3), ('business', 2), ('money', 2), ('technology', 2)],
        'v6': [('top_stories', 6), ('video', 3), ('sport', 3),
            ('comment', 3), ('culture', 3), ('business', 2), ('money', 2),
            ('technology', 2), ('most_shared_us', 6), ],
        'v7': [('top_stories', 6), ('video', 3), ('sport', 3),
            ('comment', 3), ('culture', 3), ('business', 3), ('money', 3),
            ('technology', 2), ('most_shared_us', 6), ],
    })

    template_names = immutable.make_dict({
        'v1': 'us/daily/v1',
        'v3': 'us/daily/v3',
        'v6': 'us/daily/v6',
        'v7': 'us/daily/v7',
    })