import gensim
import numpy
import pandas as pd
#importamos nuestros documentos
wiki = pd.read_csv("data/tweets5.csv", sep=";") #['id' 'twitter_id' 'user_id' 'text' 'createdat' 'keyword']

texts = wiki["text"].values.tolist()

texts = [text.split() for text in texts]

#creamos un diccionario con las palabras de los textos
dictionary = gensim.corpora.Dictionary(texts)
#guardamos nuestro diccionario
dictionary.save('lda/dictionary.dict')
stoplist = "\n 1 2 3 4 5 !! mi ni da esta for ha unos soy i pa you x d son qué ... ! uno de en la rt el y su a que un no te si tu con se los las más me the por para una lo como q del le al es o muy - — yo ya and to | of is in mas pero , .".split(" ")
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
dictionary.filter_tokens(stop_ids)
#creamos el corpus para darle al modelo (segun el formato de esta libreria)
corpus = [dictionary.doc2bow(text) for text in texts]

gensim.corpora.MmCorpus.serialize('lda/corpora.mm',corpus)


#modelo LDA
lda=gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=4, update_every=1, chunksize=1000, passes=1) #Aca se cambia el numero de topicos

print(lda.print_topics(100))

#Ahora rescatamos todos los topicos con sus palabras representativas y los guardamos en el archivo topicslda.txt
#num_topics es el numero de topicos que quiero ver, con -1 los muestra todos, num_words es la cantidad de palabras por topico
#que quiero ver.
topics = lda.show_topics(num_topics=4, num_words=20, log=False, formatted=True) #Aca cambiamos el numero de palabras por topicos

f = open('lda/topicslda_5.csv', 'w', encoding="utf8") #Aca cambiamos el nombre del archivo
for i, topic in enumerate(topics):
    f.write(str(i)+ ';')
    topic = topic[1]
    for palabras in topic.split('+'):
        pal = palabras.split("*")
        if len(pal)==2 :
            f.write(pal[1].replace('"',"" ) + ";")
    f.write("\n")
f.close()

#esta parte imprime para cada documento(fila) una tupla que corresponde a (numero_topico, probabilidad). 
#la lbreria por defecto tiene un umbral de 0,001, eso quiere decir que si un topico tiene un valor igual o menor a 0.01 
#para ese documento, no aparecera en esta lista. En otras palabras, para cada documento solo aparece la tupla (topico, prob) donde prob es mayor
# a 0.01
doctop = open('lda/docTop_5.csv','w') #Aca cambiamos el nombre del archivo
topics = lda[corpus]

for t in topics:
    mt = 0
    ind = 0
    for b in t:
        if len(b)==2:
            if(b[1] > mt):
               mt = b[1]
               ind = b[0]

    doctop.write(str(ind))
    doctop.write('\n')
doctop.close()
#Agradecimientos a Constanza Contreras.
