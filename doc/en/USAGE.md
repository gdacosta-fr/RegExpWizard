**RegExp Wizard usage**

This tool helps you creating regular expressions (RE), for the Gramps genealogy program.

In each Gramps view where a "Filter" gramplet is installed (or may be installed), add the "Regular Expressions" gramplet.

When you have finished constructing the regular expression by clicking on buttons, click on the "Paste" button: it will paste the regular expression in the "Filter" gramplet, in the same Gramps view.
___
This add-on does not use the Gramps database: it can't harm your data (but a backup is always welcome).

In case of problem, just delete the "RegExpWizard" directory created under "plugins" in the [INSTALL.md](INSTALL.md) document.
___
This small document does not cover Gramps idiosyncrasies, for example, it does not explain how names are searched in Gramps database (surname, first name, alternate names,...).

REs help you to find a string of characters, in lines of text.

The power of REs is that you can search many variations of a string at the same time.

The searched string must be divided into substrings, or individual characters, where:

- the substring must be found literally in the lines. The simplest case.
- the substring may be one of many possibilities.
- the substring may be optional.
- the character must belong to a finite set of characters; useful for diacritics, e___
This add-on does not use the Gramps database: it can't harm your data (but a backup is always welcome).

In case of problem, just delete the "RegExpWizard" directory created under "plugins" in the [INSTALL.md](INSTALL.md) document.
___.g. when you search a string with some variations on the letter "e": it may be "e", "é", "è", "ê", "ë",...

Furthermore, you can narrow the search by saying that the searched string must be at the beginning of the line, or at the end of the line.

RegExp Wizard helps you building the full RE one substring at a time.

You can check that the RE behaves as expected by entering some text in the test field.



