import glob

from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
from markdown_to_json.vendor.CommonMark import CommonMark
from tests.util import locate_file


def test_examples():
    absolute_file_paths = []
    for file in glob.glob(locate_file("../examples", __file__) + "/*.md"):
        sample_search_results_file: str = locate_file(file, __file__)
        absolute_file_paths.append(sample_search_results_file)
    assert absolute_file_paths

    for file_name in absolute_file_paths:
        if "bad_nest.md" in file_name:
            # not expecting that one to pass
            continue
        with open(file_name, encoding="utf-8") as file:
            ast = CommonMark.DocParser().parse(file.read())
            dictionary = CMarkASTNester().nest(ast)
            stringified = Renderer().stringify_dict(dictionary)
            assert stringified
