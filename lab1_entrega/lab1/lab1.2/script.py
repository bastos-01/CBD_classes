letter_count = {} #guarda as letras iniciais e o respetivo número de nomes de cada letra

with open("female-names.txt","r") as reader:
    for line in reader:
        firstLetter = line[0].upper()
        if firstLetter not in letter_count:
            letter_count[firstLetter] = 0       #caso não esteja no dicionaário, adiciona a letra
        
        letter_count[firstLetter] = letter_count[firstLetter] + 1   #incrementa o valor de nomes com a respetiva letra

with open("initials4redis.txt","w") as writer:
    for key, value in letter_count.items():
        writer.write(f" SET {key} {value}\n")