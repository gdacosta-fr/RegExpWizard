**RegExp Wizard usage**

This tool helps you creating regular expressions (RE), mainly for the Gramps genealogy program.

This small document does not cover Gramps idiosyncrasies, for example, it does not explain how names are searched in Gramps database (surname, first name, alternate names,...).

REs help you to find a string of characters, in lines of text.

The power of REs is that you can search many variations of a string at the same time.

The searched string must be divided into substrings, or individual characters, where:

- the substring must be found literally in the lines. The simplest case.
- the substring may be one of many possibilities.
- the substring may be optional.
- the character must belong to a finite set of characters; useful for diacritics, e.g. when you search a string with some variations on the letter "e": it may be "e", "é", "è", "ê", "ë",...

Furthermore, you can narrow the search by saying that the searched string must be at the beginning of the line, or at the end of the line.

RegExp Wizard helps you building the full RE one substring at a time.

You can check that the RE behaves as expected by entering some text in the test field.  
