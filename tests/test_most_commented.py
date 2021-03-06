
import unittest
from data_source import MostCommentedDataSource, CommentCountInterpolator


most_commented_short_urls_with_counts = [('cheese', 23), ('egg', 19), ('mouse', 9)]
most_commented_content = ["my", "uncle", "norbert"]

class CommentCountInterpolatorStub(object):
    def interpolate(self, content_list, comment_count_list):
        return 'Interpolated content'


class IdRememberingMultiContentDataSourceStub(object):
    def __init__(self, client):
        self.fields = []
        self.content_ids = None
        self.fetch_all_was_called = False

    def fetch_data(self):
        self.fetch_all_was_called = True
        return []


class StubDiscussionFetcher(object):
    def __init__(self):
        self.actual_page_size = None
        self.most_commented_short_urls_with_counts = None

    def fetch_most_commented(self, page_size):
        self.actual_page_size = page_size
        return self.most_commented_short_urls_with_counts


class TestMostCommented(unittest.TestCase):

    def test_data_source_should_retrieve_most_commented_pieces_of_content(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts

        data_source = MostCommentedDataSource(n_items=23,
                                              multi_content_data_source=multi_content_data_source,
                                              discussion_fetcher=discussion_fetcher,
                                              comment_count_interpolator=CommentCountInterpolatorStub())
        data_source.fetch_data()
        self.assertEquals(set(multi_content_data_source.content_ids), set(['cheese', 'egg', 'mouse']))

    def test_should_fetch_specified_number_of_items(self):
        multi_content_data_source = IdRememberingMultiContentDataSourceStub('client')

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts

        data_source = MostCommentedDataSource(n_items=23,
                                              multi_content_data_source=multi_content_data_source,
                                              discussion_fetcher=discussion_fetcher,
                                              comment_count_interpolator=CommentCountInterpolatorStub())
        data_source.fetch_data()
        self.assertEquals(discussion_fetcher.actual_page_size, 23)


    def test_data_source_should_fetch_each_piece_of_content_from_api(self):
        multi_content_data_source_stub = IdRememberingMultiContentDataSourceStub('client')

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts
        data_source = MostCommentedDataSource(n_items=12,
                                              multi_content_data_source=multi_content_data_source_stub,
                                              discussion_fetcher=discussion_fetcher,
                                              comment_count_interpolator=CommentCountInterpolatorStub())
        data_source.fetch_data()
        self.assertTrue(multi_content_data_source_stub.fetch_all_was_called)

    def test_should_return_interpolated_content(self):
        multi_content_data_source_stub = IdRememberingMultiContentDataSourceStub('client')

        discussion_fetcher = StubDiscussionFetcher()
        discussion_fetcher.most_commented_short_urls_with_counts = most_commented_short_urls_with_counts
        data_source = MostCommentedDataSource(n_items=12,
                                              multi_content_data_source=multi_content_data_source_stub,
                                              discussion_fetcher=discussion_fetcher,
                                              comment_count_interpolator=CommentCountInterpolatorStub())

        self.assertEquals(data_source.fetch_data(), list('Interpolated content'))




class TestCommentCountInterpolator(unittest.TestCase):

    def test_should_interpolate_comment_counts_into_content(self):
        content_list = [
            {
                "id": "id_1",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f1xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
                "id": "id_2",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f2xj",
                    "thumbnail": "well thumbed 2",
                    "byline": "Branch line 2",
                    }},
            {
                "id": "id_3",
                "sectionId": "cif 3",
                "sectionName": "cif name 3",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails 3",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f3xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
                "id": "id_4",
                "sectionId": "cif 4",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails 4",
                    "standfirst": "Stand pipe 4",
                    "shortUrl": "http://gu.com/p/3f4xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }}]

        comment_count_list = [('/p/3f4xj', 99), ('/p/3f3xj', 3), ('/p/3f2xj', 28), ('/p/3f1xj', 102)]

        expected_interpolated_content = [
            {
            "comment_count": 102,
                "id": "id_1",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f1xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
            "comment_count": 28,
                "id": "id_2",
                "sectionId": "cif",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f2xj",
                    "thumbnail": "well thumbed 2",
                    "byline": "Branch line 2",
                    }},
            {
            "comment_count": 3,
                "id": "id_3",
                "sectionId": "cif 3",
                "sectionName": "cif name 3",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails 3",
                    "standfirst": "Stand pipe",
                    "shortUrl": "http://gu.com/p/3f3xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }},
            {
            "comment_count": 99,
                "id": "id_4",
                "sectionId": "cif 4",
                "sectionName": "cif name",
                "webPublicationDate": "2013-04-12T14:15:00Z",
                "webTitle": "Why I wish Huma Abedin had left Anthony Weiner in the dust | Jill Filipovic",
                "webUrl": "http://www.theguardian.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "apiUrl": "http://content.guardianapis.com/commentisfree/2013/apr/12/anthony-weiner-wife-huma-abedin",
                "fields": {
                    "trailText": "happy trails 4",
                    "standfirst": "Stand pipe 4",
                    "shortUrl": "http://gu.com/p/3f4xj",
                    "thumbnail": "well thumbed",
                    "byline": "Branch line",
                    }}]

        interpolator = CommentCountInterpolator()
        interpolated_content = interpolator.interpolate(comment_count_list=comment_count_list, content_list=content_list)
        self.assertListEqual(expected_interpolated_content, interpolated_content)
