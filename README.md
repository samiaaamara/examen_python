Question1:Il faut souvent enregistrer (commit) le film (Movie) avant d’ajouter des acteurs (Actors) car ces derniers dépendent de la clé primaire du film (souvent un id auto-généré). Tant que le film n’est pas enregistré, son id n’existe pas, ce qui empêche de créer une relation valide via la clé étrangère (movie_id). Cela garantit l’intégrité référentielle et évite les erreurs liées aux contraintes de clé étrangère.
question2:Différence entre lazy loading et eager loading (joinedload) en SQLAlchemy :
Lazy loading (chargement paresseux) :
Les données liées (ex : acteurs d’un film) ne sont chargées que lorsque tu y accèdes. Cela provoque une requête supplémentaire à ce moment-là.
Risque : beaucoup de requêtes si tu accèdes à plusieurs relations (problème N+1).

Eager loading (joinedload) (chargement anticipé) :
Les données liées sont chargées immédiatement avec la requête principale via un JOIN.
Avantage : une seule requête pour récupérer le film et ses acteurs, plus rapide si tu as besoin des relations directement.
question3:Pour formater la liste des acteurs récupérés depuis la base de données en une chaîne de caractères utilisable dans un prompt pour un LLM, il suffit d’utiliser une compréhension de liste avec join, comme ceci : ", ".join(actor.actor_name for actor in movie.actors). Cela transforme une liste d’acteurs en une phrase fluide, par exemple : "Leonardo DiCaprio, Tom Hardy", ce qui permet d’intégrer naturellement les noms dans un prompt du type : « Génère un résumé du film Inception (2010), réalisé par Christopher Nolan et mettant en vedette Leonardo DiCaprio, Tom Hardy. »


