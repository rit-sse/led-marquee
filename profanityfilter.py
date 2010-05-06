import re

class ProfanityFilter:

    #arbitrary spacing between letters = [\s]*

    def readProfanities():
        profanities = []
        
        word_file = open('badwords.txt', 'r')
        
        for line in word_file:
            line = line.strip()
            entry = line.split(' : ')
            
            #comments
            if ( len(entry) >= 1 and entry[0].startswith('#') ):
                continue
            
            if ( len(entry) == 3 ):
                if ( entry[2] == 'regex' ):
                    profanities.append([entry[0], entry[1]])
                else:
                    addword = ''
                    for letter in entry[0]:
                        addword += letter + '+'
                    #addword = addword[0:len(addword)-5]
                    profanities.append([addword, entry[1]])
            elif ( len(entry) == 2):
                addword = ''
                for letter in entry[0]:
                    addword += letter + '+'
                #addword = addword[0:len(addword)-5]
                profanities.append([addword, entry[1]])
            elif ( len(entry) == 0 ):
                continue
            elif ( len(entry) == 1 ):
                if ( entry[0] == '' ):
                    continue
                else:
                    addword = ''
                    for letter in entry[0]:
                        addword += letter + '+'
                    profanities.append([addword, 'spoot'])
                
        #print(profanities)
        
        return profanities
 
    profanities = readProfanities()
 
    def replaceProfanity( self, query ):
        for w, profanity in enumerate( self.profanities ):
            badword = profanity[0]
            replacement = profanity[1]
            p = re.compile(badword , re.I)
            query = p.sub(replacement, query)
        print 'Sending: ' + query
        return query
    

#if __name__ == '__main__':
#    pro = ProfanityFilter()
#    print(pro.replaceProfanity('I fucked your mom'))
