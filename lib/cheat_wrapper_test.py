from cheat_wrapper import _add_section_name

unchanged = """
python/:list
ls
+
g++
g/+
clang++
btrfs~volume
:intro
:cht.sh
python/copy+file
python/rosetta/:list
emacs:go-mode/:list
g++g++
"""

split = """
python copy file
python/copy file

python  file
python/file

python+file
python/file

g++ -O1
g++/-O1
"""

def test_header_split():
    for inp in unchanged.strip().splitlines():
        assert inp == _add_section_name(inp)

    for test in split.strip().split('\n\n'):
        inp, outp = test.split('\n')
        assert outp == _add_section_name(inp)
