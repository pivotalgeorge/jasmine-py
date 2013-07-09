import pytest
from jasmine.console import Parser, Formatter


def test_parser_should_return_a_correct_results_list():
    parser = Parser()

    results = parser.parse([
        {u'status': u'failed',
         u'fullName': u'Globals refer to the most holy.',
         u'failedExpectations': [{u'actual': u'Batman',
                                  u'matcherName': u'toEqual',
                                  u'passed': False,
                                  u'expected': u'PANTS',
                                  u'message': u"Expected 'Batman' to equal 'PANTS'.",
                                  u'stack': u"stack\n    stack\n    stack"}],
         u'id': 0,
         u'description': u'refer to the most holy'}
    ])

    assert len(results) == 1
    assert results[0].status == 'failed'
    assert results[0].fullName == 'Globals refer to the most holy.'
    assert len(results[0].failedExpectations) == 1
    assert results[0].failedExpectations[0]['stack'] == "stack\n    stack\n    stack"


@pytest.fixture
def results():
    parser = Parser()
    return parser.parse([
        {u'status': u'passed'},
        {u'status': u'failed'},
        {u'status': u'passed'},
        {u'status': u'pending', u'fullName': u'Context is this test is pending'},
    ])


def test_format_progress(results):
    formatter = Formatter(results, colors=False)

    assert formatter.format_progress() == ".X.*"


def test_format_summary(results):
    formatter = Formatter(results, colors=False)

    assert formatter.format_summary() == "4 specs, 1 failed, 1 pending"


def test_format_failures():
    parser = Parser()

    stack1 = u"""Error: Expected 'Batman' to equal 'PANTS'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:3"""

    stack2 = u"""Error: Expected 'Batman' to equal 'Superman'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:6"""

    results = parser.parse([
        {u'status': u'passed', u'fullName': u'Context is this test passes'},
        {u'status': u'failed', u'fullName': u'Context is this test fails', u'failedExpectations': [{u'stack': stack1}]},
        {u'status': u'failed', u'fullName': u'Context is this test also fails',
            u'failedExpectations': [{u'stack': stack2}]},
    ])

    formatter = Formatter(results, colors=False)

    assert formatter.format_failures() ==\
        "Context is this test fails\n" +\
        "Error: Expected 'Batman' to equal 'PANTS'.\n" +\
        "        at http://localhost:8888/__spec__/global_spec.js:3\n" +\
        "Context is this test also fails\n" +\
        "Error: Expected 'Batman' to equal 'Superman'.\n" +\
        "        at http://localhost:8888/__spec__/global_spec.js:6\n"


def test_clean_stack():
    formatter = Formatter(results, colors=False)

    dirty_stack = u"""Error: Expected 'Batman' to equal 'PANTS'.
        at stack (http://localhost:8888/__jasmine__/jasmine.js:1110)
        at http://localhost:8888/__spec__/global_spec.js:3"""

    assert formatter.clean_stack(dirty_stack) == """Error: Expected 'Batman' to equal 'PANTS'.
        at http://localhost:8888/__spec__/global_spec.js:3"""


def test_pending_stack(results):
    formatter = Formatter(results, colors=False)

    assert formatter.format_pending() == "Context is this test is pending\n"