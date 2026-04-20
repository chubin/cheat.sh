from frontend.html import _edit_page_link, _extract_stackoverflow_post_id


def test_extract_stackoverflow_post_id():
    answer = "#  [Swati] [so/q/123198] [cc by-sa 3.0]\n"

    assert _extract_stackoverflow_post_id(answer) == "123198"


def test_edit_page_link_for_question_answer():
    answer = {
        "topic": "python/copy+file",
        "topic_type": "question",
        "answer": "#  [Swati] [so/q/123198] [cc by-sa 3.0]\n",
        "format": "code",
    }

    assert (
        _edit_page_link("python/copy+file", answer)
        == "https://stackoverflow.com/posts/123198/edit"
    )


def test_edit_page_link_for_cheat_sheet_answer():
    answer = {
        "topic": "python/file",
        "topic_type": "cheat.sheets",
        "answer": "",
        "format": "text",
    }

    assert (
        _edit_page_link("python/file", answer)
        == "https://github.com/chubin/cheat.sheets/edit/master/sheets/_python/file"
    )
