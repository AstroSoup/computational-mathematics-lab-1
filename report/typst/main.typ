#import "title.typ": * 

#set text(
  lang: "ru",
  size: 14pt,
  font: "New Computer Modern",
)


#show math.cases: math.display

#show link: it => underline(text(fill: blue)[#it])

#context id.update("1")

#context name.update("Решение СЛАУ")

#context group.update("P3208")

#context student.update("Горин Семён Дмитриевич")

#context teacher.update("Рыбаков Степан Дмитриевич")

#context year.update(datetime.today().year())

#context variant.update(2)

#include "title.typ"

#set page(
  margin: 1.5cm,
  numbering: ("1")
)

#include "table_of_contents.typ"

#pagebreak()

#show heading: set align(left)
#show heading: set text(size: 14pt)
#set heading(numbering: "1.",)
#set enum(numbering: "  1)")
#set par(
  first-line-indent: (all: true, amount: 1em),
  hanging-indent: 1em,
  justify: true,
)
#set figure.caption(separator: [ --- ])

#let style-number(number) = text(gray)[#number:]

#show raw.where(block: true): it => grid(
  columns: 2,
  align: (right, left),
  gutter: 0.5em,
  ..it.lines
    .enumerate()
    .map(((i, line)) => (style-number(i + 1), line))
    .flatten()
)

#include "content.typ"
