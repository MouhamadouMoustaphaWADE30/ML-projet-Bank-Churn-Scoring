

CREATE TABLE predictions(
	id int AUTO_INCREMENT PRIMARY KEY ,
	age INT,
	sexe VARCHAR(10),
	pays VARCHAR(12),
	cart_Credit INT,
	membre_actif INT,
	nb_produit int,
	credit_score int,
	solde_compte int,
	nb_annee int,
	salaire int,
	proba_churn int,
	pred varchar(15),
	color_proba varchar(10),
	color_class varchar(10)
	

)

INSERT INTO predictions(age, sexe, pays, cart_credit, membre_actif, nb_produit, credit_score, solde_compte, nb_annee, salaire, proba_churn, pred)
VALUES (10, "Féminin", "Allemagne", 1, 1, 4,650, 50, 4, 500, 82, "Will Exit" )