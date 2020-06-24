**Mode d'emploi simplifié de l'assistant d'expressions rationnelles**

Cet outil vous aide à créer des expressions rationnelles (*regular expressions* = RE), pour le programme de généalogie Gramps.

Dans chaque vue de Gramps où un gramplet "Filtre" est installé (ou peut être installé), ajoutez le gramplet "Expressions rationnelles".

Quand vous avez fini de construire l'expression rationnelle en cliquant sur les boutons, cliquez sur le bouton "Coller": l'expression rationnelle sera collée dans le gramplet "Filtre" de la même vue de Gramps..
___
Ce greffon n'utilise pas la base de données de Gramps: il ne peut pas corrompre vos données (mais une sauvegarde ne fait jamais de mal).

En cas de problème, détruisez simplement le répertoire "RegExpWizard" créé sous "plugins" dans le document [INSTALL.md](INSTALL.md).
___

Ce court document ne couvre pas les particularités de Gramps, par exemple il n'explique pas comment les noms sont cherchés dans la base de données de Gramps (nom de famille, prénom, alias,...).

Les RE vous aident à trouver une chaîne de caractères dans des lignes de texte.

La puissance des RE réside dans la possibilité de chercher simultanément plusieurs variantes d'une chaîne de caractères.

La chaîne cherchée doit être décomposée en sous-chaînes, ou en caractères individuels, où:

- la sous-chaîne doit être trouvée telle quelle dans les lignes. Cas le plus simple.
- la sous-chaîne peut être une parmi plusieurs possibilités. 
- la sous-chaîne peut être facultative.
- le caractère doit appartenir à un ensemble fini de caractères; utile pour les diacritiques, par exemple quand vous cherchez une chaînes avec des variantes de la lettre "e"qui peuvent être "e", "é", "è", "ê", "ë",...

De plus, vous pouvez affiner la recherche en demandant que la chaîne cherchée soit au début ou à la fin de la ligne.

L'assistant d'expressions rationnelles vous aide à construire la RE complète, une sous-chaîne à la fois.

Vous pouvez vous assurer que la RE a l'effet escompté en la confrontant à un texte arbitraire dans le champ de test.