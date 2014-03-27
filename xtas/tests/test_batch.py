# Tests for batch operations.
from nose.tools import assert_equal

from xtas.tasks.cluster import (big_kmeans, kmeans, lda, lsa,
                                parsimonious_wordcloud)


# The clusters in these should be obvious.
DOCS = [
    "apple pear banana fruit",
    "apple apple cherry banana",
    "pear fruit banana pineapple",
    "beer pizza pizza beer",
    "pizza pineapple coke",
    "beer coke sugar"
]


def test_kmeans():
    clusters = kmeans.s(2).delay(DOCS).get()
    assert_equal(len(clusters), len(DOCS))
    assert_equal(set([0, 1]), set(clusters))

    clusters = big_kmeans.s(2).delay(DOCS).get()
    assert_equal(len(clusters), len(DOCS))
    assert_equal(set([0, 1]), set(clusters))


def test_topic_models():
    n_topics = 3
    for estimator in [lda, lsa]:
        topics = estimator.s(n_topics).delay(DOCS).get()
        assert_equal(len(topics), n_topics)
        assert_equal(set(term for term, _ in topics[0]),
                     set(term for term, _ in topics[1]))


def test_wordcloud():
    cloud = parsimonious_wordcloud([doc.split() for doc in DOCS])
    assert_equal(len(cloud), len(DOCS))
    assert_equal(len(cloud[0]), 10)
