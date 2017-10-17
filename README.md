# Dockerfile for TurboParser using TurboTextAnalysis

## Create the docker
```
docker build -t turboparser .
```

## Run the docker
```
docker run -rm -p 5000:5000 -v <MODELS_PATH>:/models turboparser
```

## Running
```
curl -H "Content-type: text/plain" -X POST "http://127.0.0.1:5000" --data "Battle-tested Japanese industrial managers here always buck up nervous newcomers with the tale of the first of their countrymen to visit Mexico, a boatload of samurai warriors blown ashore 375 years ago."
```

```
0	6	1	Battle	battle	NN	O	3	HMOD	_	_	_	_	_	_	_	_
6	7	2	-	-	:	O	3	P	_	_	_	_	_	_	_	_
7	13	3	tested	test	VBN	O	0	ROOT	_	_	_	_	_	_	_	_
14	22	4	Japanese	japanese	JJ	B-MISC	6	NMOD	(1	_	AM-LOC	_	_	_	_	_
23	33	5	industrial	industrial	JJ	O	6	NMOD	_	_	A1	_	_	_	_	_
34	42	6	managers	manager	NNS	O	3	OBJ	1)	manager.01	A0	_	_	_	_	_
43	47	7	here	here	RB	O	3	LOC	_	_	_	_	_	_	_	_
48	53	8	alous	alous	JJ	O	9	NMOD	_	_	_	_	_	_	_	_
54	63	9	newcomers	newcomer	NNS	O	3	OBJ	_	_	_	_	_	_	_	_
64	68	10	with	with	IN	O	9	NMOD	_	_	_	_	_	_	_	_
69	72	11	the	the	DT	O	12	NMOD	_	_	_	_	_	_	_	_
73	77	12	tale	tale	NN	O	10	PMOD	_	tale.01	_	_	_	_	_	_
78	80	13	of	of	IN	O	12	NMOD	_	_	_	A1	_	_	_	_
81	84	14	the	the	DT	O	15	NMOD	_	_	_	_	_	_	_	_
85	90	15	first	first	JJ	O	13	PMOD	_	_	_	_	_	A0	_	_
91	93	16	of	of	IN	O	15	NMOD	_	_	_	_	_	_	_	_
94	99	17	their	their	PRP$	O	18	NMOD	(1)	_	_	_	A1	_	_	_
100	110	18	countrymen	countryman	NNS	O	16	PMOD	_	countryman.01	_	_	A0	_	_	_
111	113	19	to	to	TO	O	15	NMOD	_	_	_	_	_	_	_	_
114	119	20	visit	visit	VB	O	19	IM	_	visit.01	_	_	_	_	_	_
120	126	21	Mexico	mexico	NNP	B-LOC	20	OBJ	_	_	_	_	_	A1	_	_
126	127	22	,	,	,	O	15	P	_	_	_	_	_	_	_	_
128	129	23	a	a	DT	O	24	NMOD	_	_	_	_	_	_	_	_
130	138	24	boatload	boatload	NN	O	15	APPO	_	boatload.01	_	_	_	_	_	A1
139	141	25	of	of	IN	O	24	NMOD	_	_	_	_	_	_	A1	_
142	149	26	samurai	samurai	NN	O	27	NMOD	_	_	_	_	_	_	_	_
150	158	27	warriors	warrior	NNS	O	25	PMOD	_	_	_	_	_	_	_	_
159	164	28	blown	blow	VBN	O	24	APPO	_	blow.01	_	_	_	_	_	_
165	171	29	ashore	ashore	RB	O	28	ADV	_	_	_	_	_	_	_	AM-DIR
172	175	30	375	375	CD	O	31	NMOD	_	_	_	_	_	_	_	_
176	181	31	years	years	NNS	O	32	AMOD	_	_	_	_	_	_	_	_
182	185	32	ago	ago	RB	O	28	TMP	_	_	_	_	_	_	_	AM-TMP
185	186	33	.	.	.	O	3	P	_	_	_	_	_	_	_	_
```

## Models
This code should work with any model file trained in TurboParser. To load the TurboParser models, use the [configuration file](https://github.com/Priberam/TurboTextAnalysis/blob/master/Data/config.cfg) provided by TurboTextAnalysis.

Trained models are not available in this repository.