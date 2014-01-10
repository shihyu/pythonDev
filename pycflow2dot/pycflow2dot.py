# -*- coding: utf-8 -*-

"""
Copyright 2010 developer (unknown): https://code.google.com/p/cflow2dot/
Copyright 2013 Dabaichi Valbendan
Copyright 2013 Ioannis Filippidis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import argparse
import subprocess
import locale
import re
import networkx as nx # make this an optional dependency
try:
    import pydot
except:
    pydot = None

debug_msg_verbosity = 0
def dprint(verbosity, s):
    """Debug mode printing."""
    #TODO make this a package
    if verbosity < debug_msg_verbosity:
        print(s)

def bytes2str(b):
    encoding = locale.getdefaultlocale()[1]
    return b.decode(encoding)

def get_max_space(lines):
    space = 0
    for i in range(0, len(lines)):
        if lines[i].startswith(space * 4 * ' '):
            i = 0
            space += 1
    return space

def get_name(line):
    name = ''
    for i in range(0, len(line)):
        if line[i] == ' ':
            pass
        elif line[i] == '(':
            break
        else:
            name += line[i]
    return name

def call_cflow(c_fname, cflow, numbered_nesting=True, preprocess=False):
    cflow_cmd = [cflow]
    
    if numbered_nesting:
        cflow_cmd += ['-l']
    
    # None when -p passed w/o value
    if preprocess == None:
        cflow_cmd += ['--cpp']
    elif preprocess != False:
        cflow_cmd += ['--cpp=' +preprocess]
    
    cflow_cmd += [c_fname]
    
    dprint(2, 'cflow command:\n\t' +str(cflow_cmd) )
    
    cflow_data = subprocess.check_output(cflow_cmd)
    cflow_data = bytes2str(cflow_data)
    dprint(2, 'cflow returned:\n\n' +cflow_data)
    
    return cflow_data

def cflow2dot_old(data, offset=False, filename = ''):
    color = ['#eecc80', '#ccee80', '#80ccee', '#eecc80', '#80eecc']
    shape = ['box', 'ellipse', 'octagon', 'hexagon', 'diamond']
    
    dot = 'digraph G {\n'
    dot += 'node [peripheries=2 style="filled,rounded" '+ \
           'fontname="Vera Sans Mono" color="#eecc80"];\n'
    dot += 'rankdir=LR;\n'
    dot += 'label="' +filename +'"\n'
    dot += 'main [shape=box];\n'
    
    lines = data.replace('\r', '').split('\n')
    
    max_space = get_max_space(lines)
    nodes = set()
    edges = set()
    for i in range(0, max_space):
        for j in range(0, len(lines)):
            if lines[j].startswith((i + 1) *4 *' ') \
            and not lines[j].startswith((i +2) *4 *' '):
                cur_node = get_name(lines[j] )
                
                # node already seen ?
                if cur_node not in nodes:
                    nodes.add(cur_node)
                    print('New Node: ' +cur_node)
                
                # predecessor \exists ?
                try:
                    pred_node
                except NameError:
                    raise Exception('No predecessor node defined yet! Buggy...')
                
                # edge already seen ?
                cur_edge = (pred_node, cur_node)
                if cur_edge not in edges:
                    edges.add(cur_edge)
                else:
                    continue
                
                dot += (('node [color="%s" shape=%s];edge [color="%s"];\n') % (
                        color[i % 5], shape[i % 5], color[i % 5] ) )
                dot += (pred_node + '->' + cur_node +'\n')
            elif lines[j].startswith(i *4 *' '):
                pred_node = get_name(lines[j] )
            else:
                raise Exception('bug ?')
    dot += '}\n'
    
    dprint(2, 'dot dump str:\n\n' +dot)
    return dot

def cflow2nx(cflow_str, c_fname):
    lines = cflow_str.replace('\r', '').split('\n')
    
    g = nx.DiGraph()
    stack = dict()
    for line in lines:
        #dprint(2, line)
        
        # empty line ?
        if line == '':
            continue
        
        # defined in this file ?
        # apparently, this check is not needed: check this better
        
        # get source line #
        src_line_no = re.findall(':.*>', line)
        if src_line_no != []:
            src_line_no = int(src_line_no[0][1:-1] )
        else:
            src_line_no = -1
        
        # trim
        s = re.sub(r'\(.*$', '', line)
        s = re.sub(r'^\{\s*', '', s)
        s = re.sub(r'\}\s*', r'\t', s)
        
        # where are we ?
        (nest_level, func_name) = re.split(r'\t', s)
        nest_level = int(nest_level)
        cur_node = is_reserved_by_dot(func_name)
        
        dprint(1, 'Found function:\n\t' +func_name
              +',\n at depth:\n\t' +str(nest_level)
              +',\n at src line:\n\t' +str(src_line_no) )
        
        stack[nest_level] = cur_node
        
        # not already seen ?
        if cur_node not in g:
            g.add_node(cur_node, nest_level=nest_level, src_line=src_line_no)
            dprint(0, 'New Node: ' +cur_node)
        
        # not root node ?
        if nest_level != 0:
            # then has predecessor
            pred_node = stack[nest_level -1]
            
            # new edge ?
            if g.has_edge(pred_node, cur_node):
                # avoid duplicate edges
                # note DiGraph is so def
            
                # buggy: coloring depends on first occurrence ! (subjective)
                continue
            
            # add new edge
            g.add_edge(pred_node, cur_node)
            dprint(0, 'Found edge:\n\t' +pred_node +'--->' +cur_node)
    
    return g

def is_reserved_by_dot(word):
    reserved = {'graph', 'strict', 'digraph', 'subgraph', 'node', 'edge'}
    
    # dot is case-insensitive, according to:
    #   http://www.graphviz.org/doc/info/lang.html
    if word.lower() in reserved:
        word = word +'_'
    return word

def dot_preamble(c_fname, for_latex):
    if for_latex:
        c_fname = re.sub(r'_', r'\\\\_', c_fname)
    
    dot_str = 'digraph G {\n'
    dot_str += 'node [peripheries=2 style="filled,rounded" '+ \
           'fontname="Vera Sans Mono" color="#eecc80"];\n'
    dot_str += 'rankdir=LR;\n'
    dot_str += 'label="' +c_fname +'"\n'
    dot_str += 'main [shape=box];\n'
    
    return dot_str

def choose_node_format(node, nest_level, src_line, defined_somewhere,
                       for_latex, multi_page):
    colors = ['#eecc80', '#ccee80', '#80ccee', '#eecc80', '#80eecc']
    shapes = ['box', 'ellipse', 'octagon', 'hexagon', 'diamond']
    sl = '\\\\' # after fprintf \\ and after dot \, a single slash !
    
    # color, shape ?
    if nest_level == 0:
        color = colors[0]
        shape = 'box'
    else:
        color = colors[(nest_level -1) % 5]
        shape = shapes[nest_level % 5]
    
    # fix underscores ?
    if for_latex:
        label = re.sub(r'_', r'\\\\_', node)
    else:
        label = node
    dprint(1, 'Label:\n\t: ' +label)
    
    # src line of def here ?
    if src_line != -1:
        if for_latex:
            label = label +'\\n' +str(src_line)
        else:
            label = label +'\\n' +str(src_line)
    
    # multi-page pdf ?
    if multi_page:
        if src_line != -1:
            # label
            label = sl +'descitem{' +node +'}\\n' +label
        else:
            # link only if LaTeX label will appear somewhere
            if defined_somewhere:
                label = sl +'descref[' +label +']{' +node +'}'
        
    dprint(1, 'Node dot label:\n\t: ' +label)
    
    return (label, color, shape)

def dot_format_node(node, nest_level, src_line, defined_somewhere,
                    for_latex, multi_page):
    (label, color, shape) = choose_node_format(node, nest_level, src_line,
                                               defined_somewhere,
                                               for_latex, multi_page)
    dot_str = node
    dot_str += '[label="' +label +'" '
    dot_str += 'color="' +color +'" '
    dot_str += 'shape=' +shape +'];\n\n'
    
    return dot_str

def dot_format_edge(from_node, to_node, color):
    dot_str = 'edge [color="' +color +'"];\n\n'
    dot_str += from_node +'->' +to_node +'\n'
    
    return dot_str

def node_defined_in_other_src(node, other_graphs):
    defined_somewhere = False
    
    for graph in other_graphs:
        if node in graph:
            src_line = graph.node[node]['src_line']
            
            if src_line != -1:
                defined_somewhere = True
    
    return defined_somewhere

def dump_dot_wo_pydot(graph, other_graphs, c_fname, for_latex, multi_page):
    dot_str = dot_preamble(c_fname, for_latex)
    
    for node in graph:
        node_dict = graph.node[node]
        
        defined_somewhere = node_defined_in_other_src(node, other_graphs)
        
        nest_level = node_dict['nest_level']
        src_line = node_dict['src_line']
        
        dot_str += dot_format_node(node, nest_level, src_line, defined_somewhere,
                                   for_latex, multi_page)
    
    for from_node, to_node in graph.edges_iter():
        # call order affects edge color, so use only black
        color = '#000000'
        dot_str += dot_format_edge(from_node, to_node, color)
    
    dot_str += '}\n'
    dprint(2, 'dot dump str:\n\n' +dot_str)
    
    return dot_str

def write_dot_file(dot_str, dot_fname):
    try:
        dot_path = dot_fname +'.dot'
        with open(dot_path, 'w') as fp:
            fp.write(dot_str)
            dprint(0, 'Dumped dot file.')
    except:
        raise Exception('Failed to save dot.')
    
    return dot_path

def write_graph2dot(graph, other_graphs, c_fname, img_fname,
                    for_latex, multi_page, layout):
    if pydot is None:
        print('Pydot not found. Exporting using pycflow2dot.write_dot_file().')
        dot_str = dump_dot_wo_pydot(graph, other_graphs, c_fname,
                                    for_latex=for_latex, multi_page=multi_page)
        dot_path = write_dot_file(dot_str, img_fname)
    else:
        # dump using networkx and pydot
        pydot_graph = nx.to_pydot(graph)
        
        pydot_graph.set_splines('true')
        if layout == 'twopi':
            pydot_graph.set_ranksep(5)
            pydot_graph.set_root('main')
        else:
            pydot_graph.set_overlap(False)
            pydot_graph.set_rankdir('LR')
        
        dot_path = img_fname +'.dot'
        pydot_graph.write(dot_path, format='dot')
    
    return dot_path

def write_graphs2dot(graphs, c_fnames, img_fname, for_latex, multi_page, layout):
    dot_paths = []
    counter = 0
    for graph, c_fname in zip(graphs, c_fnames):
        other_graphs = list(graphs)
        other_graphs.remove(graph)
        
        cur_img_fname = img_fname +str(counter)
        dot_paths += [write_graph2dot(graph, other_graphs, c_fname, cur_img_fname,
                                     for_latex, multi_page, layout) ]
        counter += 1
    
    return dot_paths

def check_cflow_dot_availability():
    required = ['cflow', 'dot']
    
    dep_paths = []
    for dependency in required:
        path = subprocess.check_output(['which', dependency] )
        path = bytes2str(path)
        
        if path.find(dependency) < 0:
            raise Exception(dependency +' not found in $PATH.')
        else:
            path = path.replace('\n', '')
            print('found ' +dependency +' at: ' +path)
            dep_paths += [path]
    
    return dep_paths

def dot2img(dot_paths, img_format, layout):
    print('This may take some time... ...')
    for dot_path in dot_paths:
        img_fname = str(dot_path)
        img_fname = img_fname.replace('.dot', '.' +img_format)
    
        dot_cmd = [layout, '-T'+img_format, '-o', img_fname, dot_path]
        dprint(1, dot_cmd)
        
        subprocess.check_call(dot_cmd)
    print(img_format +' produced successfully from dot.')

def latex_preamble_str():
    """Return string for LaTeX preamble.
    
    Used if you want to compile the SVGs stand-alone.
    
    If SVGs are included as part of LaTeX document, then copy required
    packages from this example to your own preamble.
    """
    
    latex = r"""
    \documentclass[12pt, final]{article}
    
    usepackage{mybasepreamble}
    % fix this !!! to become a minimal example

    \usepackage[paperwidth=25.5in, paperheight=28.5in]{geometry}
    
    \newcounter{desccount}
    \newcommand{\descitem}[1]{%
        	\refstepcounter{desccount}\label{#1}
    }
    \newcommand{\descref}[2][\undefined]{%
    	\ifx#1\undefined%
        \hyperref[#2]{#2}%
    	\else%
    	    \hyperref[#2]{#1}%
    	\fi%
    }%
    """
    return latex

def write_latex():
    latex_str = latex_preamble_str()

def usage():
    doc = 'cflow2dot.py file1 file2 ..... --output[-o] outputfilename\n'
    doc += 'output file format is svg\n'
    doc += '--version (-v) show version\n'
    doc += '--help (-h) show this document.'
    print(doc)

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--input-filenames', nargs='+',
                        help='filename(s) of C source code files to be parsed.')
    parser.add_argument('-o', '--output-filename', default='cflow',
                        help='name of dot, svg, pdf etc file produced')
    parser.add_argument('-f', '--output-format', default='svg',
                        choices=['dot', 'svg', 'pdf', 'png'],
                        help='output file format')
    parser.add_argument('-l', '--latex-svg', default=False, action='store_true',
                        help = 'produce SVG for import to LaTeX via Inkscape')
    parser.add_argument('-m', '--multi-page', default=False, action='store_true',
                        help = 'produce hyperref links between function calls '
                              +'and their definitions. Used for multi-page '
                              +'PDF output, where each page is a different '
                              +'source file.')
    parser.add_argument('-p', '--preprocess', default=False, nargs='?',
                        help='pass --cpp option to cflow, '
                        +'invoking C preprocessor, optionally with args.')
    parser.add_argument(
        '-g', '--layout', default='dot',
        choices=['dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp'],
        help='graphviz layout algorithm.'
    )
    parser.add_argument(
        '-x', '--exclude', default='',
        help='file listing functions to ignore'
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    
    return args

def rm_excluded_funcs(list_fname, graphs):
    # nothing ignored ?
    if not list_fname:
        return
    
    # load list of ignored functions
    rm_nodes = [line.strip() for line in open(list_fname).readlines() ]
    
    # delete them
    for graph in graphs:
        for node in rm_nodes:
            if node in graph:
                graph.remove_node(node)

def main():
    """Run cflow, parse output, produce dot and compile it into pdf | svg."""
    
    copyright_msg = """
    PyCflow2dot v0.1 - licensed under GNU GPL v3
    """
    print(copyright_msg)
    
    # input
    (cflow, dot) = check_cflow_dot_availability()
    
    args = parse_args()
    
    c_fnames = args.input_filenames
    img_format = args.output_format
    for_latex = args.latex_svg
    multi_page = args.multi_page
    img_fname = args.output_filename
    preproc = args.preprocess
    layout = args.layout
    exclude_list_fname = args.exclude
    
    dprint(0, 'C src files:\n\t' +str(c_fnames) +", (extension '.c' omitted)\n"
           +'img fname:\n\t' +str(img_fname) +'.' +img_format +'\n'
           +'LaTeX export from Inkscape:\n\t' +str(for_latex) +'\n'
           +'Multi-page PDF:\n\t' +str(multi_page) )
    
    cflow_strs = []
    for c_fname in c_fnames:
        cur_str = call_cflow(c_fname, cflow, numbered_nesting=True,
                                 preprocess=preproc)
        cflow_strs += [cur_str]
    
    graphs = []
    for cflow_out, c_fname in zip(cflow_strs, c_fnames):
        cur_graph = cflow2nx(cflow_out, c_fname)
        graphs += [cur_graph]
    
    rm_excluded_funcs(exclude_list_fname, graphs)
    dot_paths = write_graphs2dot(graphs, c_fnames, img_fname, for_latex,
                                 multi_page, layout)
    dot2img(dot_paths, img_format, layout)

if __name__ == "__main__":
    main()
