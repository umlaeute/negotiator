#!/usr/bin/env python

"""these tests bilfered from negotiator.py:__main__"""

from negotiator import ContentNegotiator, AcceptParameters, ContentType, Language


def test_contenttype1():
    print("+++ text/plain only +++")
    accept = "text/plain"
    server = [AcceptParameters(ContentType("text/plain"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/plain")) == ap
    assert "text/plain" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype2():
    print("+++ application/atom+xml vs application/rdf+xml without q values +++")
    accept = "application/atom+xml, application/rdf+xml"
    server = [
        AcceptParameters(ContentType("application/rdf+xml")),
        AcceptParameters(ContentType("application/atom+xml")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("application/atom+xml")) == ap
    assert "application/atom+xml" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype3():
    print("+++ application/atom+xml vs application/rdf+xml with q values +++")
    accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9"
    server = [
        AcceptParameters(ContentType("application/rdf+xml")),
        AcceptParameters(ContentType("application/atom+xml")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("application/rdf+xml")) == ap
    assert "application/rdf+xml" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype4():
    print(
        "+++ application/atom+xml vs application/rdf+xml vs text/html with mixed q values +++"
    )
    accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
    server = [
        AcceptParameters(ContentType("application/rdf+xml")),
        AcceptParameters(ContentType("application/atom+xml")),
        AcceptParameters(ContentType("text/html")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/html")) == ap
    assert "text/html" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype5():
    print("+++ text/plain only, unsupported by server +++")
    accept = "text/plain"
    server = [AcceptParameters(ContentType("text/html"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert None == ap


def test_contenttype6():
    print(
        "+++ application/atom+xml vs application/rdf+xml vs text/html with mixed q values, most preferred unavailable +++"
    )
    accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
    server = [
        AcceptParameters(ContentType("application/rdf+xml")),
        AcceptParameters(ContentType("application/atom+xml")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("application/rdf+xml")) == ap
    assert "application/rdf+xml" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype7():
    print(
        "+++ application/atom+xml vs application/rdf+xml vs text/html with mixed q values, most preferred available +++"
    )
    accept = "application/atom+xml;q=0.6, application/rdf+xml;q=0.9, text/html"
    server = [
        AcceptParameters(ContentType("application/rdf+xml")),
        AcceptParameters(ContentType("text/html")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/html")) == ap
    assert "text/html" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype8():
    print("+++ application/atom+xml;type=feed supported by server +++")
    accept = "application/atom+xml;type=feed"
    server = [AcceptParameters(ContentType("application/atom+xml;type=feed"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("application/atom+xml;type=feed")) == ap
    assert "application/atom+xml;type=feed" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype9():
    print("+++ image/* supported by server +++")
    accept = "image/*"
    server = [
        AcceptParameters(ContentType("text/plain")),
        AcceptParameters(ContentType("image/png")),
        AcceptParameters(ContentType("image/jpeg")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("image/png")) == ap
    assert "image/png" == ap.content_type.mimetype()
    assert None == ap.language


def test_contenttype10():
    print("+++ */* supported by server +++")
    accept = "*/*"
    server = [
        AcceptParameters(ContentType("text/plain")),
        AcceptParameters(ContentType("image/png")),
        AcceptParameters(ContentType("image/jpeg")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/plain")) == ap
    assert "text/plain" == ap.content_type.mimetype()
    assert None == ap.language


def test_language1():
    print("+++ en only +++")
    accept_language = "en"
    server = [AcceptParameters(language=Language("en"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept_language)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("en")) == ap
    assert None == ap.content_type
    assert "en" == ap.language.language


def test_language2():
    print("+++ en vs de without q values +++")
    accept = "en, de"
    server = [
        AcceptParameters(language=Language("en")),
        AcceptParameters(language=Language("de")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("en")) == ap
    assert None == ap.content_type
    assert "en" == ap.language.language


def test_language3():
    print("+++ fr vs no with q values +++")
    accept = "fr;q=0.7, no;q=0.8"
    server = [
        AcceptParameters(language=Language("fr")),
        AcceptParameters(language=Language("no")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("no")) == ap
    assert None == ap.content_type
    assert "no" == ap.language.language


def test_language4():
    print("+++ en vs de vs fr with mixed q values +++")
    accept = "en;q=0.6, de;q=0.9, fr"
    server = [
        AcceptParameters(language=Language("en")),
        AcceptParameters(language=Language("de")),
        AcceptParameters(language=Language("fr")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("fr")) == ap
    assert None == ap.content_type
    assert "fr" == ap.language.language


def test_language5():
    print("+++ en only, unsupported by server +++")
    accept = "en"
    server = [AcceptParameters(language=Language("de"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert None == ap


def test_language6():
    print("+++ en vs no vs de with mixed q values, most preferred unavailable +++")
    accept = "en;q=0.6, no;q=0.9, de"
    server = [
        AcceptParameters(language=Language("en")),
        AcceptParameters(language=Language("no")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("no")) == ap
    assert None == ap.content_type
    assert "no" == ap.language.language


def test_language7():
    print("+++ en vs no vs de with mixed q values, most preferred available +++")
    accept = "en;q=0.6, no;q=0.9, de"
    server = [
        AcceptParameters(language=Language("no")),
        AcceptParameters(language=Language("de")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("de")) == ap
    assert None == ap.content_type
    assert "de" == ap.language.language


def test_language8():
    print("+++ en-gb supported by server +++")
    accept = "en-gb"
    server = [AcceptParameters(language=Language("en-gb"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("en-gb")) == ap
    assert None == ap.content_type
    assert "en" == ap.language.language


def test_language9():
    print("+++ en-gb, unsupported by server +++")
    accept = "en-gb"
    server = [AcceptParameters(language=Language("en"))]
    cn = ContentNegotiator(acceptable=server, ignore_language_variants=False)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert None == ap


def test_language10():
    print("+++ en-gb, supported by server through language variants +++")
    accept = "en-gb"
    server = [AcceptParameters(language=Language("en"))]
    cn = ContentNegotiator(acceptable=server, ignore_language_variants=True)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("en")) == ap
    assert None == ap.content_type
    assert "en" == ap.language.language


def test_language11():
    print("+++ en, partially supported by server +++")
    accept = "en"
    server = [AcceptParameters(language=Language("en-gb"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("en-gb")) == ap
    assert None == ap.content_type
    assert "en" == ap.language.language


def test_language12():
    print("+++ * by itself +++")
    accept = "*"
    server = [
        AcceptParameters(language=Language("no")),
        AcceptParameters(language=Language("de")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("no")) == ap
    assert None == ap.content_type
    assert "no" == ap.language.language


def test_language13():
    print("+++ * with other options, primary option unsupported +++")
    accept = "en, *"
    server = [
        AcceptParameters(language=Language("no")),
        AcceptParameters(language=Language("de")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("no")) == ap
    assert None == ap.content_type
    assert "no" == ap.language.language


def test_language14():
    print("+++ * with other options, primary option supported +++")
    accept = "en, *"
    server = [
        AcceptParameters(language=Language("en")),
        AcceptParameters(language=Language("de")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept_language=accept)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(language=Language("en")) == ap
    assert None == ap.content_type
    assert "en" == ap.language.language


def test_contentlanguage1():
    print("+++ content type and language specified +++")
    accept = "text/html"
    accept_lang = "en"
    server = [AcceptParameters(ContentType("text/html"), Language("en"))]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept, accept_language=accept_lang)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/html"), Language("en")) == ap
    assert "text/html" == ap.content_type.mimetype()
    assert "en" == ap.language.language


def test_contentlanguage2():
    print("+++ 2 content types and one language specified +++")
    accept = "text/html, text/plain"
    accept_lang = "en"
    server = [
        AcceptParameters(ContentType("text/html"), Language("de")),
        AcceptParameters(ContentType("text/plain"), Language("en")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept, accept_language=accept_lang)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/plain"), Language("en")) == ap
    assert "text/plain" == ap.content_type.mimetype()
    assert "en" == ap.language.language


def test_contentlanguage3():
    print("+++ 2 content types and 2 languages specified +++")
    accept = "text/html, text/plain"
    accept_lang = "en, de"
    server = [
        AcceptParameters(ContentType("text/html"), Language("de")),
        AcceptParameters(ContentType("text/plain"), Language("en")),
    ]
    cn = ContentNegotiator(acceptable=server)
    ap = cn.negotiate(accept=accept, accept_language=accept_lang)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/html"), Language("de")) == ap
    assert "text/html" == ap.content_type.mimetype()
    assert "de" == ap.language.language


def test_contentlanguage4():
    print("+++ 2 content types and one language specified, with weights +++")
    weights = {"content_type": 2.0, "language": 1.0, "charset": 1.0, "encoding": 1.0}
    accept = "text/html, text/plain"
    accept_lang = "en"
    server = [
        AcceptParameters(ContentType("text/html"), Language("de")),
        AcceptParameters(ContentType("text/plain"), Language("en")),
    ]
    cn = ContentNegotiator(acceptable=server, weights=weights)
    ap = cn.negotiate(accept=accept, accept_language=accept_lang)
    print("+++ " + str(ap) + " +++")
    assert AcceptParameters(ContentType("text/plain"), Language("en")) == ap
    assert "text/plain" == ap.content_type.mimetype()
    assert "en" == ap.language.language


if __name__ == "__main__": # pragma: no cover
    test_contenttype1()
    test_contenttype2()
    test_contenttype3()
    test_contenttype4()
    test_contenttype5()
    test_contenttype6()
    test_contenttype7()
    test_contenttype8()
    test_contenttype9()
    test_contenttype10()
    test_language1()
    test_language2()
    test_language3()
    test_language4()
    test_language5()
    test_language6()
    test_language7()
    test_language8()
    test_language9()
    test_language10()
    test_language11()
    test_language12()
    test_language13()
    test_language14()
    test_contentlanguage1()
    test_contentlanguage2()
    test_contentlanguage3()
    test_contentlanguage4()
