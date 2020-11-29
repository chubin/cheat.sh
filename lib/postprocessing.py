import search
import fmt.comments

def postprocess(answer, keyword, options, request_options=None):
    answer = _answer_add_comments(answer, request_options=request_options)
    answer = _answer_filter_by_keyword(answer, keyword, options, request_options=request_options)
    return answer

def _answer_add_comments(answer, request_options=None):

    if answer['format'] != 'text+code':
        return answer

    topic = answer['topic']
    if "filetype" in answer:
        filetype = answer["filetype"]
    else:
        filetype = 'bash'
        if '/' in topic:
            filetype = topic.split('/', 1)[0]
            if filetype.startswith('q:'):
                filetype = filetype[2:]

    answer['answer'] = fmt.comments.beautify(
        answer['answer'], filetype, request_options)
    answer['format'] = 'code'
    answer['filetype'] = filetype
    return answer

def _answer_filter_by_keyword(answer, keyword, options, request_options=None):
    answer['answer'] = _filter_by_keyword(answer['answer'], keyword, options)
    return answer

def _filter_by_keyword(answer, keyword, options):

    def _join_paragraphs(paragraphs):
        answer = "\n".join(paragraphs)
        return answer

    def _split_paragraphs(text):
        answer = []
        paragraph = ""
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        for line in text.splitlines():
            if line == "":
                answer.append(paragraph)
                paragraph = ""
            else:
                paragraph += line+"\n"
        answer.append(paragraph)
        return answer

    paragraphs = [p for p in _split_paragraphs(answer)
                  if search.match(p, keyword, options=options)]
    if not paragraphs:
        return ""

    return _join_paragraphs(paragraphs)
