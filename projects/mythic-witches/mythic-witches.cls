\ProvidesClass{mythic-witches}[witches doc format]

\LoadClass{extarticle}
\RequirePackage{accsupp}
\RequirePackage[margin=2cm]{geometry}
\usepackage{imakeidx}
\usepackage{multind}
\usepackage{ifthen}
\usepackage{fancyhdr}
\pagestyle{fancy}

\RequirePackage{xcolor}
\RequirePackage{tikz}
\usetikzlibrary{calc}
\usetikzlibrary{arrows}
\RequirePackage[skins]{tcolorbox}
\RequirePackage[inline]{enumitem}
\RequirePackage{graphicx}
\RequirePackage{dashrule}
\RequirePackage{multirow,tabularx}

% --------------------------
\usepackage{paracol}
\usepackage[dvipsnames]{xcolor}
\usepackage{lipsum}
\usepackage[object=vectorian]{pgfornament}
\usepackage{calc}
\usepackage[table]{xcolor}
\usepackage[pgf]{rpgicons}

\usepackage[rm]{roboto}
\usepackage[defaultsans]{lato}
\usepackage{yfonts}

\setlength{\parindent}{0pt}

% -----------------------------------------
% Colors
% -----------------------------------------
\definecolor{VLRed}{HTML}{8F3D3A}
\definecolor{VLYellow}{HTML}{CFAE23}
\definecolor{VLPurple}{HTML}{665C71}
\definecolor{VLGreen}{HTML}{6e7649}
\definecolor{LightGrey}{HTML}{DDDDDD}
\definecolor{MidGrey}{HTML}{999999}
\definecolor{DarkGrey}{HTML}{333333}

% -----------------------------------------
% Basic Formatting
% -----------------------------------------
\newcommand\HUGE{\@setfontsize\Huge{100}{100}}
\newcommand{\divider}{
    \textcolor{VLRed}{\hdashrule{\linewidth}{0.5pt}{0.4ex}}\smallskip
}
\newcommand{\header}{\LARGE\bfseries}
\newcommand{\titleFont}{\LARGE\rmfamily\bfseries}
\newcommand{\subtitleFont}{\large\rmfamily\bfseries}
\newcommand{\sectionName}[1]{%
    \bigskip
    {\color{VLRed}\noindent\subtitleFont#1}
    \\ \divider \\
}
\newcommand{\keyword}[1]{
    {\bfseries{\color{VLPurple}#1}}
}
\newcommand{\randomHelpers}[5]{
    \noindent{\color{VLPurple}Person:} #1 \sep {\color{VLPurple}Name:} #2 \sep {\color{VLPurple}Aspect:} #3 \sep {\color{VLPurple}Object:} #4 \sep {\color{VLPurple}Beast:} #5
}
\newcommand{\sep}[0]{
    {\color{VLRed}$\cdot$}
}
\newcommand{\mainTitle}[2]{
    \begin{center}
        {\titleFont\bfseries{\color{VLRed}#1}}\\
        {\large #2}
    \end{center}
    \par\noindent{\color{VLRed}\rule{\linewidth}{1pt}\par}
}
\newcommand{\statBlock}[1]{
    ({\small\color{VLPurple}#1})
}
\setlist{leftmargin=*,labelsep=0.5em,nosep,itemsep=0.25\baselineskip,after=\vspace{0.25\baselineskip}}
\newcommand{\pageBorder}{
    \begin{tikzpicture}[remember picture,overlay]
        \draw[line width=5pt, color=VLRed]
            ($(current page.north west) + (10pt,-10pt)$) rectangle
            ($(current page.south east) + (-10pt,10pt)$);
    \end{tikzpicture}
}

% -----------------------------------------
% Witches
% -----------------------------------------
\newcommand{\witchName}[4]{
    \addcontentsline{toc}{section}{#2}
    \noindent
    \colorbox{VLRed}{
        \begin{minipage}[c][2em][c]{1.8em}
            \Huge \bfseries \color{white} \textgoth{#1}
        \end{minipage}
    }
    \begin{minipage}{3.2em}
        \pgfornament[height=2.6em,color=VLRed]{7}
    \end{minipage}
    \begin{minipage}{25em}
        \medskip
        {\color{VLRed}\titleFont\MakeUppercase{#2}}\\%
        \smallskip
        {\subtitleFont #3}
    \end{minipage}
    \begin{minipage}{18em}
        \hfill
        \colorbox{VLRed}{
            \begin{minipage}[c][2em][c]{8em}
                \hspace{1em}
                \color{white}\Huge\textgoth{Witches}
            \end{minipage}
        }
    \end{minipage}
    \par\noindent{\color{VLRed}\rule{\linewidth}{1pt}\par}
    \vspace{1em}
    \includegraphics[width=\textwidth]{img/#4}
}
\newcommand{\startWitchPage}[4]{
    \witchName{#1}{#2}{#3}{#4}
    \medskip
    \columnratio{0.5}
    \begin{paracol}{2}
    \setlength{\columnsep}{3em} 
}
\newcommand{\finishWitchPage}[0]{
    \end{paracol}
    \smallskip
    \par\noindent{\color{VLRed}\rule{\linewidth}{1pt}\par}
}
\newcommand{\aspectCallout}[2]{
    \smallskip
    \noindent{\large\bfseries{\color{VLRed}#1}}
    \smallskip
    #2
    \medskip
}
\newcommand{\itemName}[2]{
    \index{#1}
    \par\noindent\hspace{1em}\hangindent=2em{\bfseries\color{DarkGrey}#1}: #2
}

% -----------------------------------------
% Rules
% -----------------------------------------
\newcommand{\rulesHeader}{
    \begin{minipage}{2.9em}
        \pgfornament[height=2.6em,color=VLRed]{7}
    \end{minipage}
    \colorbox{VLRed}{
        \begin{minipage}[c][2em][c]{\linewidth-4.5em}
            {\color{white}\titleFont\huge Rules Addendum}
        \end{minipage}
    }
    \smallskip
    \par\noindent{\color{VLRed}\rule{\linewidth}{1pt}\par}
    \vspace{1em}
}

% -----------------------------------------
% Tables
% -----------------------------------------
\newcommand{\createTable}[3]{
    \smallskip
    {\noindent\large\bfseries\color{VLRed}#1}\par
    \smallskip
    \begin{tabularx}{\linewidth}{#2}
    #3
    \end{tabularx}
    \medskip
}
\newcommand{\emphrow}{
    \rowcolor{LightGrey!20}
}
\newcommand{\normrow}{}
\newcommand{\headrow}{
    \rowcolor{VLRed!10}
}
\newcommand{\cvh}[1]{
    \bfseries{#1}
}
\newcommand{\rvh}[1]{
    {\color{VLRed}\bfseries{#1}}
}

% -----------------------------------------
% Myths
% -----------------------------------------
\newcommand{\mythName}[4]{
    \addcontentsline{toc}{section}{#2}
    \noindent
    \colorbox{VLRed}{
        \begin{minipage}[c][2em][c]{1.8em}
            \Huge \bfseries \color{white} \textgoth{#1}
        \end{minipage}
    }
    \begin{minipage}{3.2em}
        \pgfornament[height=2.6em,color=VLRed]{7}
    \end{minipage}
    \begin{minipage}{25em}
        \medskip
        {\color{VLRed}\titleFont\MakeUppercase{#2}}\\%
        \smallskip
        {\subtitleFont #3}
    \end{minipage}
    \begin{minipage}{18em}
        \hfill
        \colorbox{VLRed}{
            \begin{minipage}[c][2em][c]{6em}
                \hspace{0.5em}
                \color{white}\Huge\textgoth{Myth}
            \end{minipage}
        }
    \end{minipage}
    \par\noindent{\color{VLRed}\rule{\linewidth}{1pt}\par}
    \vspace{1em}
    \includegraphics[width=\textwidth]{img/myths/#4}
}
\newcommand{\startMythPage}[4]{
    \mythName{#1}{#2}{#3}{#4}
    \columnratio{0.5}
    \begin{paracol}{2}
    \setlength{\columnsep}{4em} 
    \medskip
}
\newcommand{\finishMythPage}[0]{
   \end{paracol} 
}
\newcommand{\omen}[2]{
    \colorbox{VLRed}{
        \begin{minipage}[c][2em][c]{1.2em}
            \Huge \bfseries \color{white} \textgoth{#1}
        \end{minipage}
    }
    \hspace{1em}
    \begin{minipage}{\linewidth-1.5em}
        #2 \\%
    \end{minipage} \\%
}
\newcommand{\red}[1]{
{\color{VLRed}#1}
}
\def\attrBlock#1{\attrBlockSplit#1\relax}
\def\attrBlockSplit#1 #2 #3 #4\relax{
    \keyword{VIG} \red{#1}, \keyword{CLA} \red{#2}, \keyword{SPI} \red{#3}, \keyword{GD} \red{#4}
}
\newcommand{\castEntry}[5]{
    \begin{center}
        {\Large \color{VLRed} #1} \\%
        \attrBlock{#2} \\%
        #3 \\%
        #4 \\%
        \ifthenelse{\equal{#5}{}}{}{
            \keyword{#5} \\%
        }
    \end{center}
}
\newcommand{\mythQuote}[1]{
    {\color{VLPurple}"#1"}
}
\newcommand{\spacedDivider}{
    \smallskip
    \divider
    \smallskip
}