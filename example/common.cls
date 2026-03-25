% Add common class elements here
\LoadClass{article}
\usepackage{graphicx}
\RequirePackage{multirow,tabularx}
\usepackage[svgnames]{xcolor}

\newcommand{\createTable}[3]{
    \smallskip
    {\noindent\large\bfseries#1}\par
    \smallskip
    \begin{tabularx}{15em}{#2}
    #3
    \end{tabularx}
    \medskip
}
\newcommand{\cvh}[1]{
    {\color{Purple}\bfseries{#1}}
}