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
BUFFER_TEXT_2 = """#+TITLE: Friday, 25-01-19
#+SEQ_TODO: TODO(t) WAITING(w) | DONE(d) CANCELLED(c)
#+LATEX_HEADER: \\usepackage[margin=0.5in]{geometry}

* Read ML papers [0/1]
** TODO jibnbo xu distance-powered
*** Deep convolutional neural netorks (DCNN)    (ResNet)
**** 1. May capture higher-order residue correlation while DCA is mainly pairwise
**** 2. tries to learn the global context of a protein contact matrix and uses it to predict the status of one residue pair
**** 3. Existing DCA methods are roughly a linear model, while ResNet is a nonlinear model

* DeepThoughts [3/3]
** DONE make script to make contact predictions from DeepCov
   CLOSED: [2019-01-18 Fri 15:24]
** DONE make production run script
   CLOSED: [2019-01-18 Fri 15:24]
** DONE make gremlin script for running gremlin from cmdline
   CLOSED: [2019-01-22 Tue 16:39]
** DONE re-run all a3ms with 2 different databases. Going to use the uniprot_2015_06 database, and log the database from now on for consistency
   CLOSED: [2019-01-24 Thu 09:59]
** DONE Re-run deepcov and gremlin with older uniprot_2015_06 database so we can find better targets
   CLOSED: [2019-01-24 Thu 09:59]
** DONE Find targets (using (# seq)/(sqrt(len(seq))):
   CLOSED: [2019-01-24 Thu 10:41]
*** ('target_name', 'hardness', '#seq', 'len seq')
*** 0-15 = Very hard
**** 'casp12/T0885/uniprot_20_2015_06/aln.psicov', '8', 88, 116
**** 'casp12/T0894/uniprot_20_2015_06/aln.psicov', '9', 158, 324
**** 'casp12/T0904/uniprot_20_2015_06/aln.psicov', '9', 163, 341
**** 'casp12/T0872/uniprot_20_2015_06/aln.psicov', '10', 98, 91
**** 'casp13/T0968s2/uniprot_20_2015_06/aln.psicov', '11', 121, 116
*** 16-55 = medium hardness
**** 'casp13/T0960/uniprot_20_2015_06/aln.psicov', '30', 584, 384
**** 'casp13/T0963/uniprot_20_2015_06/aln.psicov', '32', 618, 372
**** 'casp12/T0877/uniprot_20_2015_06/aln.psicov', '32', 385, 142
**** 'casp12/T0882/uniprot_20_2015_06/aln.psicov', '32', 302, 89
*** 56-128 = almost easy
**** 'casp12/T0891/uniprot_20_2015_06/aln.psicov', '83', 950, 130
**** 'casp12/T0922/uniprot_20_2015_06/aln.psicov', '117', 1151, 96
*** 128+ = easy
**** 'casp12/T0947/uniprot_20_2015_06/aln.psicov', '785', 11647, 220
**** 'casp12/T0866/uniprot_20_2015_06/aln.psicov', '938', 12685, 183
**** 'casp12/T0917/uniprot_20_2015_06/aln.psicov', '1187', 24003, 409
**** 'casp12/T0879/uniprot_20_2015_06/aln.psicov', '1472', 21978, 223
***  Legend: Dots above the red line, indicates positions where there is > 5 sequences per length (if visible, green bar = 20 seq/len). Point of this graphic is to give you an idea if resubmitting a sub-portion of your sequence might help increase the overall Seq/Len (which after applying the coverage filter is at: 0.047).
('target_name', 'hardness', '#seq', 'len seq')
('casp13/T0955/uniprot_20_2015_06/aln.psicov', '0', 1, 41)
('casp12/T0900/uniprot_20_2015_06/aln.psicov', '0', 1, 106)
('casp12/T0860/uniprot_20_2015_06/aln.psicov', '0', 4, 137)
('casp12/T0859/uniprot_20_2015_06/aln.psicov', '0', 2, 133)
('casp12/T0896/uniprot_20_2015_06/aln.psicov', '0', 11, 486)
('casp13/T0957s1/uniprot_20_2015_06/aln.psicov', '1', 10, 163)
('casp12/T0869/uniprot_20_2015_06/aln.psicov', '1', 11, 120)
('casp12/T0921/uniprot_20_2015_06/aln.psicov', '2', 30, 149)
('casp12/T0868/uniprot_20_2015_06/aln.psicov', '2', 27, 161)
('casp13/T0968s1/uniprot_20_2015_06/aln.psicov', '3', 37, 126)
('casp13/T0957s2/uniprot_20_2015_06/aln.psicov', '3', 34, 164)
('casp13/T0958/uniprot_20_2015_06/aln.psicov', '3', 35, 96)
('casp12/T0884/uniprot_20_2015_06/aln.psicov', '3', 23, 75)
('casp12/T0862-D1/uniprot_20_2015_06/aln.psicov', '3', 27, 101)
('casp12/T0897/uniprot_20_2015_06/aln.psicov', '5', 90, 285)
('casp12/T0870/uniprot_20_2015_06/aln.psicov', '6', 74, 138)
('casp13/T0950/uniprot_20_2015_06/aln.psicov', '7', 135, 353)
('casp12/T0909/uniprot_20_2015_06/aln.psicov', '7', 126, 340)
('casp12/T0885/uniprot_20_2015_06/aln.psicov', '8', 88, 116)
('casp12/T0894/uniprot_20_2015_06/aln.psicov', '9', 158, 324)
('casp12/T0904/uniprot_20_2015_06/aln.psicov', '9', 163, 341)
('casp12/T0872/uniprot_20_2015_06/aln.psicov', '10', 98, 91)
('casp13/T0968s2/uniprot_20_2015_06/aln.psicov', '11', 121, 116)
('casp13/T0953s2/uniprot_20_2015_06/aln.psicov', '11', 169, 249)
('casp12/T0863/uniprot_20_2015_06/aln.psicov', '11', 292, 670)
('casp12/T0895/uniprot_20_2015_06/aln.psicov', '11', 121, 129)
('casp13/T0966/uniprot_20_2015_06/aln.psicov', '13', 291, 494)
('casp12/T0898/uniprot_20_2015_06/aln.psicov', '13', 164, 169)
('casp12/T0948/uniprot_20_2015_06/aln.psicov', '15', 196, 166)
('casp12/T0941/uniprot_20_2015_06/aln.psicov', '23', 491, 470)
('casp13/T0953s1/uniprot_20_2015_06/aln.psicov', '26', 220, 72)
('casp12/T0865/uniprot_20_2015_06/aln.psicov', '27', 234, 75)
('casp12/T0905/uniprot_20_2015_06/aln.psicov', '28', 522, 353)
('casp13/T0960/uniprot_20_2015_06/aln.psicov', '30', 584, 384)
('casp13/T0963/uniprot_20_2015_06/aln.psicov', '32', 618, 372)
('casp12/T0877/uniprot_20_2015_06/aln.psicov', '32', 385, 142)
('casp12/T0882/uniprot_20_2015_06/aln.psicov', '32', 302, 89)
('casp12/T0864/uniprot_20_2015_06/aln.psicov', '46', 729, 246)
('casp12/T0892/uniprot_20_2015_06/aln.psicov', '55', 763, 193)
('casp12/T0891/uniprot_20_2015_06/aln.psicov', '83', 950, 130)
('casp12/T0922/uniprot_20_2015_06/aln.psicov', '117', 1151, 96)
('casp12/T0912/uniprot_20_2015_06/aln.psicov', '138', 3460, 624)
('casp12/T0943/uniprot_20_2015_06/aln.psicov', '146', 3472, 563)
('casp12/T0886/uniprot_20_2015_06/aln.psicov', '181', 3375, 346)
('casp12/T0902/uniprot_20_2015_06/aln.psicov', '194', 3443, 315)
('casp12/T0873/uniprot_20_2015_06/aln.psicov', '196', 4384, 501)
('casp12/T0944/uniprot_20_2015_06/aln.psicov', '303', 5048, 277)
('casp12/T0913/uniprot_20_2015_06/aln.psicov', '375', 7378, 386)
('casp12/T0871/uniprot_20_2015_06/aln.psicov', '463', 8958, 375)
('casp12/T0945/uniprot_20_2015_06/aln.psicov', '513', 10380, 409)
('casp12/T0918/uniprot_20_2015_06/aln.psicov', '711', 16603, 546)
('casp12/T0947/uniprot_20_2015_06/aln.psicov', '785', 11647, 220)
('casp12/T0866/uniprot_20_2015_06/aln.psicov', '938', 12685, 183)
('casp12/T0917/uniprot_20_2015_06/aln.psicov', '1187', 24003, 409)
('casp12/T0879/uniprot_20_2015_06/aln.psicov', '1472', 21978, 223)
('casp12/T0920/uniprot_20_2015_06/aln.psicov', '2062', 49134, 568)
('casp12/T0942/uniprot_20_2015_06/aln.psicov', '2137', 47151, 487)
('casp12/T0911/uniprot_20_2015_06/aln.psicov', '2149', 45339, 445)
('casp12/T0928/uniprot_20_2015_06/aln.psicov', '2497', 49196, 388)
('casp12/T0861/uniprot_20_2015_06/aln.psicov', '2586', 46482, 323)
('casp13/T0954/uniprot_20_2015_06/aln.psicov', '2687', 50264, 350)
('casp12/T0903/uniprot_20_2015_06/aln.psicov', '2836', 55430, 382)
('casp12/T0893/uniprot_20_2015_06/aln.psicov', '3096', 48156, 242)
('casp13/T0951/uniprot_20_2015_06/aln.psicov', '3120', 51842, 276)
('casp12/T0889/uniprot_20_2015_06/aln.psicov', '3224', 50157, 242)
** TODO run abinitio on found targets
     
* dgdp weird docking [0/1]
** TODO Investigate weird docking
    :LOGBOOK:
    CLOCK: [2018-11-27 Tue 15:36]
    :END:

* non_global_density [1/2]
** DONE Need to implement new data_cache task
    SCHEDULED: <2018-11-01 Thu>
** TODO Find out why tests are failing

* SWISNF [1/2]
** DONE Come up with a way to divvy up non-built loop
   SCHEDULED: <2018-11-01 Thu>
** TODO Run abinitio on all inter subunits
   SCHEDULED: <2018-11-01 Thu>
** TODO Compile crosslinks for swisnf
   :LOGBOOK:
   CLOCK: [2019-01-02 Wed 12:47]
   :END:
** DONE still need to setup the new runs for 01.7
   :LOGBOOK:
   CLOCK: [2019-01-09]--[2019-01-09]
   :END:
** TODO still need to run interactions on new db

* Julian project [0/1]
** WAITING Run hybridize on all results from our relax (make sure frag sampling is high)
   SCHEDULED: <2018-11-01 Thu>
   :LOGBOOK:
   CLOCK: [2018-11-01 Thu 11:42]--[2018-11-01 Thu 12:57] =>  1:15
   :END:

* BBSOME [1/2]
** TODO Mutate N-terminal residues on BBS_7
** DONE Fix sup figure 4 for Max
   CLOSED: [2019-01-08 Tue 18:15]
*** So I can't figure out how I got the ~40 number that's in the text.
*** Ok recreated it, it should be 44 and 41 now.

* rosetta_cryo_assembly [2/2]
** DONE Finish abinitio dask integration
   SCHEDULED: <2018-11-01 Thu>
** DONE Integrate into dask
   SCHEDULED: <2018-11-01 Thu>
** DONE Integrate abinitio into dask
** TODO Run everything on benchmark set [0/1]
** TODO Fix minimization not same both directions [0/1]

* MMTF [1/1]
** DONE Finish tests for mmtf-cpp module
   SCHEDULED: <2018-11-01 Thu>

* ~Some Time~   

* Re run banchmarks
** TODO redo first 3-4 checking if 'benchmark' is set
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
        self.track_todo_num = True

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

    def recreate_count_only_keeps(self):
        total_count = 0
        done_count = 0
        not_done_tags = [' TODO ', ' WAITING ']
        for child in self.children:
            if not child.keep:
                continue
            if any(tag in child.head() for tag in not_done_tags):
                total_count += 1
            elif ' DONE ' in child.head():
                total_count += 1
                done_count += 1
        return total_count, done_count

    def recreate_counts(self):
        total_count = 0
        done_count = 0
        not_done_tags = [' TODO ', ' WAITING ']
        for child in self.children:
            if any(tag in child.head() for tag in not_done_tags):
                total_count += 1
            elif ' DONE ' in child.head():
                total_count += 1
                done_count += 1
        return total_count, done_count

    def recreate_self(self):
        s = f"{self.power*'*'} {self.header}"
        if self.track_todo_num:
            total_count, done_count = self.recreate_counts()
            if total_count:
                s = f"{s} [{done_count}/{total_count}]"
        if self.contents:
            s = f"{s}\n{self.recreate_contents()}"
        if self.children:
            s = f"{s}\n{self.recreate_children()}"
        return s.rstrip()

    def self_only_keeps(self):
        s = f"{self.power*'*'} {self.header}"
        if self.track_todo_num:
            total_count, done_count = self.recreate_count_only_keeps()
            if total_count:
                s = f"{s} [{done_count}/{total_count}]"
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
            block = block.strip()
            split_block = block.split()
            assert len(list(set(split_block[0]))) == 1
            power = len(list(split_block[0]))
            possible_counter_text = block.split('\n')[0].split()[-1]
            end = len(block.split('\n')[0])
            if possible_counter_text.startswith("[") and possible_counter_text.endswith("]"):
                end = block.split('\n')[0].index(possible_counter_text)
            elements.append(
                    emacs_element(power, block.split('\n')[0][power+1:end], '\n'.join(block.split('\n')[1:]), block))

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
                        top_powers[ele.power].parent.children.append(ele)
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
        possible_counter_text = split_block[0].split()[-1]
        end = len(block.split('\n')[0])
        if possible_counter_text.startswith("[") and possible_counter_text.endswith("]"):
            end = block.split('\n')[0].index(possible_counter_text)
        elements.append(emacs_element(1, split_block[0][2:end], '\n'.join(contents), block))

    for ele in elements:
        ele.build_children()
        recreated = ele.recreate_self()
        # print("recreated")
        # print(recreated)
        # print("RAW")
        # print(ele.raw_self.rstrip())
        # assert recreated == ele.raw_self.rstrip()
    known_heads = {}
    for ele in elements:
        head = ele.head()
        if head.split()[-1].startswith("[") and head.split()[-1].endswith("]"):
            head = head[:head.index(head.split()[-1])].strip()
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
        total_keepers = len([child.keep for child in master_child.children if child.keep])
        if total_keepers:
            final_texts.append(master_child.self_only_keeps())
    return '\n\n'.join(final_texts)


def main():
    # stdin = sys.argv[1]
    # with open("test.txt", 'w') as fh:
    #     fh.write(stdin)
    # stdin = BUFFER_TEXT
    stdin = BUFFER_TEXT_2

    heads = parse_journal_text(stdin)
    final_text = trim_heads(heads)
    print(final_text, end='')


if __name__ == "__main__":
    main()
