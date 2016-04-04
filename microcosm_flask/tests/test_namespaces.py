"""
Namespace tests.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
    none,
)

from microcosm.api import create_object_graph
from microcosm_flask.namespaces import Namespace
from microcosm_flask.operations import Operation


def test_endpoint_for():
    """
    Simple (subject-only) endpoint naming works.

    """
    ns = Namespace(subject="foo")
    endpoint = ns.endpoint_for(Operation.Search)
    assert_that(endpoint, is_(equal_to("foo.search")))


def test_operation_naming_relation():
    """
    Complext (subject+object) endpoint naming works.

    """
    ns = Namespace(subject="foo", object_="bar")
    endpoint = ns.endpoint_for(Operation.SearchFor)
    assert_that(endpoint, is_(equal_to("foo.search_for.bar")))


def test_parse_endpoint():
    """
    Simple (subject-only) endpoints can be parsed.

    """
    operation, ns = Namespace.parse_endpoint("foo.search")
    assert_that(operation, is_(equal_to(Operation.Search)))
    assert_that(ns.subject, is_(equal_to("foo")))
    assert_that(ns.object_, is_(none()))


def test_parse_endpoint_relation():
    """
    Complex (subject+object) endpoints can be parsed.

    """
    operation, ns = Namespace.parse_endpoint("foo.search_for.bar")
    assert_that(operation, is_(equal_to(Operation.SearchFor)))
    assert_that(ns.subject, is_(equal_to("foo")))
    assert_that(ns.object_, is_(equal_to("bar")))


def test_operation_url_for():
    """
    Operations can resolve themselves via Flask's `url_for`.

    """
    graph = create_object_graph(name="example", testing=True)
    ns = Namespace(subject="foo")

    @graph.route(ns.collection_path, Operation.Search, ns)
    def search_foo():
        pass

    with graph.app.test_request_context():
        url = ns.url_for(Operation.Search)
        assert_that(url, is_(equal_to("/api/foo")))


def test_operation_href_for():
    """
    Operations can resolve themselves as fully expanded hrefs.

    """
    graph = create_object_graph(name="example", testing=True)
    ns = Namespace(subject="foo")

    @graph.route(ns.collection_path, Operation.Search, ns)
    def search_foo():
        pass

    with graph.app.test_request_context():
        url = ns.href_for(Operation.Search)
        assert_that(url, is_(equal_to("http://localhost/api/foo")))