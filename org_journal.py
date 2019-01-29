#!/usr/bin/env python

import sys
import re

BUFFER_TEXT = """#+TITLE: Sunday, 27-01-19
#+SEQ_TODO: TODO(t) WAITING(w) | DONE(d) CANCELLED(c)
#+LATEX_HEADER: \\usepackage[margin=0.5in]{geometry}

* MyfirstProj
** I'm not sure NOTHING HERE
* Sunday, 27-01-19
* MyfirstProj
** TODO I'm not sure
** DONE I'm sure
   some hextra textysex
* MysecondProj
** TODO I'm not sure DEF
   some hextra textyse
** DONE I'm sure DEF
* MyThirdProj
** Somthing i don't really want
*** Somthing i thingk want
**** TODO Somthing i thingk want
     some hextra textysekeep
**** DONE Somthing i thingk want
     some hextra textysethrow
** TODO I'm not sure DEF
** DONE I'm sure DEF


* MyfirstProj
** I'm not sure NOTHING HERE FIN
* MyfirstProj
** TODO I'm not sure FIN
** DONE I'm sure FIN
* MysecondProj
** TODO I'm not sure DEF FIN
** DONE I'm sure DEF FIN
* MyThirdProj
** TODO I'm not sure DEF FIN
** DONE I'm sure DEF FIN
"""


class emacs_element:
    def __init__(self, power, header, contents, raw_self, parent=None):
        self.power = power
        self.header = header
        self.contents = contents
        self.raw_self = raw_self
        self.parent = parent
        self.keep = False
        self.children = []

    def head(self):
        return f"{self.power*'*'} {self.header}"

    def __repr__(self):
        s = f"ele: parent={self.parent} keep={self.keep}"
        s = f"{s}\n{self.head()}"
        if self.contents:
            s = f"{s}\n{self.contents.rstrip()}"
        s = f"{s}\nraw:\n{self.raw_self}"
        return s

    def merge(self, other):
        assert self.power == other.power
        assert self.header == other.header
        assert self.parent is None
        assert other.parent is None
        other_raw = other.raw_self.replace(other.head(), '').strip('\n')
        self.raw_self += f"\n{other_raw}"
        for child in other.children:
            child.parent = self
            self.children.append(child)

    def recreate_contents(self):
        if self.contents:
            return self.contents
        else:
            return ''

    def recreate_children(self):
        return '\n'.join([child.recreate_self() for child in self.children])

    def children_only_keeps(self):
        keep_list = []
        for child in self.children:
            if child.keep:
                keep_list.append(child)
        return '\n'.join([child.self_only_keeps() for child in keep_list])

    def recreate_self(self):
        s = f"{self.power*'*'} {self.header}"
        if self.contents:
            s = f"{s}\n{self.recreate_contents()}"
        if self.children:
            s = f"{s}\n{self.recreate_children()}"
        return s.rstrip()

    def self_only_keeps(self):
        s = f"{self.power*'*'} {self.header}"
        if self.contents:
            s = f"{s}\n{self.recreate_contents()}"
        if self.children:
            s = f"{s}\n{self.children_only_keeps()}"
        return s.strip()

    def keep_sub(self):
        self.keep = True
        for child in self.children:
            child.keep_sub()

    def keep_parents(self):
        self.keep = True
        if self.parent:
            self.parent.keep_parents()

    def keep_this_tree(self):
        self.keep = True
        for child in self.children:
            child.keep_sub()
        if self.parent:
            self.parent.keep_parents()

    def build_children(self):
        contents = '\n'.join(self.raw_self.split('\n')[1:])
        child_block_starts = [x.start() for x in re.finditer('^\*', contents, re.MULTILINE)]
        child_block_starts.append(len(contents))
        child_blocks = []
        for i, header_start in enumerate(child_block_starts[:-1]):
            child_blocks.append(contents[header_start: child_block_starts[i+1]].rstrip())
        elements = []
        for block in child_blocks:
            block = block.rstrip()
            split_block = block.split()
            assert len(list(set(split_block[0]))) == 1
            power = len(list(split_block[0]))
            elements.append(
                    emacs_element(power, block.split('\n')[0][power+1:], '\n'.join(block.split('\n')[1:]), block))

        if not elements:
            return
        top_powers = {elements[0].power: elements[0]}
        for i, ele in enumerate(elements):
            if i == 0:
                continue
            if ele.power == elements[i-1].power+1:
                top_powers[ele.power-1].children.append(ele)
                ele.parent = elements[i-1]
                top_powers[ele.power] = ele
                continue
            elif ele.power == elements[i-1].power:
                if elements[i-1].parent:
                    ele.parent = elements[i-1].parent
                    elements[i-1].parent.children.append(ele)
                    top_powers[ele.power] = ele
                    continue
                else:  # must be top level
                    assert ele.power == 2
                    self.children.append(top_powers[ele.power])
                    top_powers[ele.power] = ele
                    continue
            else:  # must be above +1 or lower
                if ele.power in top_powers:
                    if not top_powers[ele.power].parent:
                        self.children.append(top_powers[ele.power])
                        top_powers[ele.power] = ele
                        continue
                    else:
                        ele.parent = top_powers[ele.power].parent
                        top_powers[ele.power] = ele
                        continue
                else:
                    assert False, ele
        if top_powers[elements[0].power] not in self.children:
            self.children.append(top_powers[elements[0].power])


def parse_journal_text(stdin):
    header_starts = [x.start() for x in re.finditer('^\* ', stdin, re.MULTILINE)]
    header_starts.append(len(stdin))

    blocks = []
    for i, header_start in enumerate(header_starts[:-1]):
        blocks.append(stdin[header_start: header_starts[i+1]])

    elements = []
    for block in blocks:
        split_block = block.split('\n')
        contents = []
        for line in split_block[1:]:
            if not line:
                continue
            if line.startswith('*'):
                break
            contents.append(line)
        elements.append(emacs_element(1, split_block[0][2:], '\n'.join(contents), block))

    for ele in elements:
        ele.build_children()
        recreated = ele.recreate_self()
        assert recreated == ele.raw_self.rstrip()
    known_heads = {}
    for ele in elements:
        head = ele.head()
        if head not in known_heads:
            known_heads[head] = []
        known_heads[head].append(ele)
    return known_heads


def tag_check(parent):
    tags = [' TODO ', ' WAITING ']
    parent_has_tag = any(tag in parent.head() for tag in tags)
    if parent_has_tag:
        parent.keep_this_tree()
        return
    for child in parent.children:
        should_keep_this_tree = any(tag in child.head() for tag in tags)
        if should_keep_this_tree:
            child.keep_this_tree()
            continue
        tag_check(child)


def trim_heads(heads):
    final_texts = []
    for head, children in heads.items():
        master_child = children[0]
        for child in children[1:]:
            master_child.merge(child)
        if len(master_child.children) == 0:
            continue
        tag_check(master_child)
        final_texts.append(master_child.self_only_keeps())
    return '\n'.join(final_texts)


def main():
    stdin = sys.argv[1]
    with open("test.txt", 'w') as fh:
        fh.write(stdin)
    # stdin = BUFFER_TEXT

    heads = parse_journal_text(stdin)
    final_text = trim_heads(heads)
    print(final_text, end='')


if __name__ == "__main__":
    main()
