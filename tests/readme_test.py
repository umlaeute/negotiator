#!/usr/bin/env python


"""these tests are just the examples in the README"""

from negotiator import ContentNegotiator, AcceptParameters, ContentType, Language


def test_readme1():
    """the 1st example from the README"""
    default_params = AcceptParameters(ContentType("text/html"), Language("en"))
    acceptable = [AcceptParameters(ContentType("text/html"), Language("en"))]
    acceptable.append(AcceptParameters(ContentType("text/json"), Language("en")))
    cn = ContentNegotiator(default_params, acceptable)
    acceptable = cn.negotiate(accept="text/json;q=1.0, text/html;q=0.9")
    assert acceptable == AcceptParameters(ContentType("text/json"), Language("en"))
    assert acceptable.content_type.mimetype() == "text/json"
    assert acceptable.language.language == "en"


def test_readme2():
    """the 2nd example from the README"""
    default_params = AcceptParameters(ContentType("text/html"), Language("en"))
    acceptable = [AcceptParameters(ContentType("text/html"), Language("en"))]
    acceptable.append(AcceptParameters(ContentType("text/html"), Language("fr")))
    acceptable.append(AcceptParameters(ContentType("text/html"), Language("de")))
    acceptable.append(AcceptParameters(ContentType("text/json"), Language("en")))
    acceptable.append(AcceptParameters(ContentType("text/json"), Language("cz")))
    acceptable.append(AcceptParameters(ContentType("application/pdf"), Language("de")))
    weights = {"content_type": 1.0, "language": 0.5}
    cn = ContentNegotiator(default_params, acceptable, weights)
    accept = "text/html, text/json;q=1.0, application/pdf;q=0.5"
    accept_language = "en;q=0.5, de, cz, fr"
    acceptable = cn.negotiate(accept, accept_language)
    assert acceptable == AcceptParameters(ContentType("text/html"), Language("de"))
    assert acceptable.content_type.mimetype() == "text/html"
    assert acceptable.language.language == "de"


if __name__ == "__main__": # pragma: no cover
    test_readme1()
    test_readme2()
