"""
Defines namespaces for operations that follow various API conventions.

In conjunction with the `Operation` enum, defines a naming convention for HTTP endpoints,
which in turn provides a discovery mechanism API routes.

"""
from urllib import urlencode
from urlparse import urljoin

from flask import request, url_for

from microcosm_flask.naming import (
    collection_path_for,
    instance_path_for,
    name_for,
    relation_path_for,
    singleton_path_for,
)
from microcosm_flask.operations import Operation


class Namespace(object):
    """
    Encapsulates the namespace for one or more operations.

    Each fully qualified operation can be viewed as a subject, verb, and optional object.

    The `Operation` enum defines the legal verbs (according to various conventions); this
    object encapsulates the rest.

    """

    def __init__(self, subject, object_=None, path="", version=None):
        self.subject = subject
        self.object_ = object_
        self.path = path
        self.version = version

    @property
    def object_ns(self):
        """
        Create a new namespace for the current namespace's object value.

        """
        return Namespace(
            path=self.path,
            subject=self.object_,
            object_=None,
            version=self.version,
        )

    @property
    def subject_name(self):
        return name_for(self.subject)

    @property
    def object_name(self):
        return name_for(self.object_)

    @property
    def collection_path(self):
        return self.path + collection_path_for(self.subject)

    @property
    def instance_path(self):
        return self.path + instance_path_for(self.subject)

    @property
    def relation_path(self):
        return self.path + relation_path_for(self.subject, self.object_)

    @property
    def singleton_path(self):
        return self.path + singleton_path_for(self.subject)

    def endpoint_for(self, operation):
        """
        Create a (unique) endpoint name from an operation and a namespace.

        This naming convention matches how Flask blueprints routes are resolved
        (assuming that the blueprint and resources share the same name).

        Examples: `foo.search`, `bar.search_for.baz`

        """
        if self.object_ is not None:
            return operation.value.pattern.format(
                self.subject_name,
                operation.value.name,
                self.object_name,
            )
        else:
            return operation.value.pattern.format(
                self.subject_name,
                operation.value.name,
            )

    @staticmethod
    def parse_endpoint(name):
        """
        Convert an endpoint name into an (operation, ns) tuple.

        """
        parts = name.split(".")
        operation = Operation.from_name(parts[1])
        if len(parts) > 2:
            return operation, Namespace(subject=parts[0], object_=parts[2])
        else:
            return operation, Namespace(subject=parts[0])

    def url_for(self, operation, **kwargs):
        """
        Construct a URL for an operation against a resource.

        :param kwargs: additional arguments for URL path expansion

        """
        return url_for(self.endpoint_for(operation), **kwargs)

    def href_for(self, operation, qs=None, **kwargs):
        """
        Construct an full href for an operation against a resource.

        :parm qs: the query string dictionary, if any
        :param kwargs: additional arguments for path expansion
        """
        return "{}{}".format(
            urljoin(request.url_root, self.url_for(operation, **kwargs)),
            "?{}".format(urlencode(qs)) if qs else "",
        )

    @classmethod
    def make(cls, value, path=None):
        """
        Create a Namespace from a value.

        Used to transition older APIs that relied on strings/objects/tuples/lists
        to pass subject and object information instead of Namespace instances.

        """
        if isinstance(value, Namespace):
            return value
        elif isinstance(value, (tuple, list)):
            return cls(
                subject=value[0],
                object_=value[1],
                path=path,
            )
        else:
            return cls(
                subject=value,
                path=path,
            )