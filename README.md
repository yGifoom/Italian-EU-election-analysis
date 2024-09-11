# Italian-EU-election-analysis
An analysis of the impact that towny candidates had on the 2019 european elections in Italy, and some other fun stuff!

# The Question
Do filler candidates influence the election on a national level?

## Dataset
2019 European election in italy (only local, no estero)

## Definitions
- a candidate belongs to a party
- circoscrizione > regione > provincia > comune
- all candidates belong to at least one circoscrizione
- a national candidate is a candidate which gets all the votes that expressed no preference in a certain circoscrizione
- are filler candidate (riempi-lista) is a candidate who is used by the party just to increase the number of preferences to the lista.
(
QUANTITATIVE DEF:
- def 1, for a party: given the total number of preferences for a party, if a candidate has a low proportion of preferences party-wise q% (E.g. q=0.5),
but on the total of preferences for the same party in a comune is > p% (E.g. p=50)then it is a filler candidate for a party.
- def 2, in general: a candidate which gets q% (E.g. q=70) of their preferences from comuni in which the same candidate gets p% (E.g. p=70) of the votes, is a filler candidate
this def 2 is flawed
)

## Steps
### Dataset pre processing __GIOVANNI__
[x] get the dataset in csv
[x] organize dataset for python parsing 
[x] examine the dataset and clean it (17/08)

### division of comuni by population __GIOVANNI__ (19/08)
[X] how the preferences are spread out in a cumune by population 
[X] how the preferences are spread out in a cumune by population 
[] group by circoscrizione and highlight party __GIOVANNI__(21/08)

### find filler candidates
[] set percentages for filler candidates classification __ALESSANDRO CON DEF1__(21/08)
[] consider big, small city effects 
[] Does their birthplace have any correlation with origin of votes? __LORENZO__(21/08)

### Quantify the effect of filler candidates
[] scope of the party
[] scope of the elections

### examine elected candidates votes
[] where do succesful candidates get their votes 
[] Does their birthplace have any correlation with origin of votes?
[] how candidates get elected in their party in relation with the votes they got 
(where they voted directly or where they pushed up by their party?) 
[x] how are votes distributed in a party? __LORENZO__
[] how actually elected canddates distribute per party __LORENZO__ (21/08 PRIORITA)

### representance, spread and polarization
[] how representative are the elected candidates
[] how polarized were the elections

## Conclusions



#### misceleneous
- majority of people did not express preferenze
- for visualization I random sampled from the population weighting on the population of the settlement,
correlation was kept at the same values roughly + some variation

- there seems to be no correlation between area/population/density and homogeneousness of votes
perhaps there is too much noise, clustering by parties might make this better

- how much compromise must parties have to reach a high consensus? depending on the circoscrizione this number changes.

- checking how polarized elections are in different parts of italy
