import os
import sys
import glob


gv_text = r"""

digraph g {

rankdir = "LR"

}

""".strip()



html_text = r"""

<!DOCTYPE html>
<html lang="pt-br" xmlns="http://www.w3.org/1999/xhtml">
<head>
   <meta http-equiv="refresh" content="1">
   <title>$$$</title>
   <style>
       html, body, img { width: 98%; height: 98%; }
   </style>
</head>

<body>
   <img src="$$$.svg">
</body>

""".strip()



render_sh_text = r"""

#!/bin/bash

dot -T svg -o "$$$.svg" "$$$.gv"

""".strip()



nome = __file__.split(os.sep)[-2]

with open("{}.gv".format(nome), 'w') as gv:
    gv.write(gv_text)

with open("{}.html".format(nome), 'w') as html:
    html.write(html_text.replace('$$$', nome))

with open("render.sh", 'w') as sh:
    sh.write(render_sh_text.replace('$$$', nome))


if ('win' in sys.platform):
    gvexepath = glob.glob(r"c:\*\Graphviz*\bin\dot.exe")[0]
    print gvexepath
    render_bat_text = r"""
@echo off
:loop
"###" -T svg -o "$$$.svg" "$$$.gv"
timeout /t 2
goto loop""".strip().replace("###", gvexepath)

    with open("render.bat", 'w') as bat:
        bat.write(render_bat_text.replace('$$$', nome))
else:
    with open("render.sh", 'w') as sh:
        sh.write(render_sh_text.replace('$$$', nome))
