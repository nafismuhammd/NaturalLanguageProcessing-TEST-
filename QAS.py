# -*- coding: utf-8 -*-
"""
Created on Sat May  2 13:10:01 2020

@author: mnafi
"""

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class preprocessing:
    
    #Fungsi penghilangan angka, tanda baca, dan karakter   
    def removal(self):
        alphabet = re.sub("[^a-zA-Z0-9]"," ",self)
#        self = alphabet
        return alphabet
    
    #Fungsi pemotongan string input perkata
    def tokenization(self):
        token = self.split()
        self = token
        return token
    
    #Fungsi pengubahan semua huruf menjadi huruf kecil
    def caseFolding(self):
        lower = self.lower()
        self = lower
        return lower
    
    def stemming(self):
        factory = StemmerFactory()
        ps = factory.create_stemmer()
        words = list()
        for i in self:
            afterStemming = ps.stem(i)
            words.append(afterStemming)
        return words
    
    def hasil(doc):
        new = preprocessing.removal(doc)
        new = preprocessing.caseFolding(new)
        new = preprocessing.tokenization(new)
        new = preprocessing.stemming(new)
        return new
    
class proses:
    def cariJenis(q):
        jns = ""
        if 'siapa' in q:
            jns = 'PERSON'
        elif 'berapa' and 'harga' in q:
            jns = 'MONEY'
        elif 'berapa' in q and ('pukul' or 'jam' or 'waktu' in q):
            jns = 'TIME'
        elif 'mana' in q:
            jns = 'GPE'
        elif 'kapan' in q:
            jns = 'TIME'
        elif 'apa' in q:
            jns = 'apa'
        return jns
        
    def passage(q,doc):
        doc.append(q)
        vectorizerdoc = CountVectorizer().fit_transform(doc)
        vectordoc = vectorizerdoc.toarray()
        bantu = []
        bid = ""
        for i in range(len(doc)-1):
            vec1 = vectordoc[i].reshape(1, -1)
            vec2 = vectordoc[len(doc)-1].reshape(1, -1)
            bantu.append(cosine_similarity(vec1,vec2)[0][0])
        doc.remove(q)
        for i in range(len(bantu)):
            if max(bantu)==bantu[i]:
                bid = i
        return bid    
        
            
    
    def ask(q,doc):
        nlp = spacy.load('id_ud-tag-dep-ner-1.0.0')
        print("\nQ : "+q)
        doc = nlp(doc)
        jns = proses.cariJenis(preprocessing.hasil(q))
        if jns == 'apa':
            qnlp = nlp(q)
            bantu = 0
            for i in qnlp:
                if 'VSA' == i.tag_:
                    bantu +=1
            if bantu == 0 :
                for i in doc:
                    if 'VSA' == i.tag_:
                        print("A : "+i.text)
                        break
            elif bantu >= 0 :
                for i in doc:
                    if 'X--' == i.tag_:
                        print("A : "+i.text)
                        break
        else:
            for i in doc.ents:
                if i.label_ == jns:
                    print("A : "+i.text)
                    break
                
    def jawab(q,doc):
        proses.ask(q,doc[proses.passage(q,doc)])
                            
        

class jalankan:
    def RUN():
        doc = ["Jokowi adalah Presiden Indonesia","Muhammad Nafis tinggal di kota Medan","Muhammad Nafis suka membaca buku","Setiap pukul 07.00 WIB Andi selalu masuk kerja","Muti membeli kosmetik dengan harga Rp9000000"]
        q1 = "Pukul berapa Andi masuk kerja?"
        proses.jawab(q1,doc)

        q2 = "Siapa yang suka membaca buku?"
        proses.jawab(q2,doc)

        q3 = "Siapa presiden Indonesia?"
        proses.jawab(q3,doc)

        q4 = "Berapa harga kosmetik muti?"
        proses.jawab(q4,doc)

        q5 = "Dimana Muhammad Nafis tinggal?"
        proses.jawab(q5,doc)

        q6 = "Siapa yang tinggal di kota Medan?"
        proses.jawab(q6,doc)

        q7 = "Kapan Andi masuk kerja?"
        proses.jawab(q7,doc)

        q8 = "Apa yang disukai Muhammad Nafis?"
        proses.jawab(q8,doc)

        q9 = "Apa yang dibeli Muti?"
        proses.jawab(q9,doc)

        q10 = "Siapa yang masuk kerja pukul 10.00 WIB?"
        proses.jawab(q10,doc)


        
    if __name__ == "__main__":
        RUN()