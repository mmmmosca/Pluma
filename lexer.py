def tokenize(line):
    tokens = []
    l = len(line)

    i = 0
    while i < l:
        if line[i].isalpha() or line[i] == "_":
            j = i

            while j < l and (line[j].isalnum() or line[j] == "_"):
                j += 1

            result = line[i:j]

            if result == "stampa":
                tokens.append("STAMPA")
            elif result == "lista":
                tokens.append("LISTA")
            elif result == "con":
                tokens.append("CON")
            elif result == "se":
                tokens.append("SE")
            elif result == "altrimenti":
                tokens.append("ALTRIMENTI")
            elif result == "perogni" or result == "perogniqualvolta":
                tokens.append("PEROGNI")
            elif result == "mentre":
                tokens.append("MENTRE")
            elif result == "allora":
                tokens.append("ALLORA")
            elif result == "in":
                tokens.append("IN")
            elif result == "da":
                tokens.append("DA")
            elif result == "sia":
                tokens.append("SIA")
            elif result == "funzione":
                tokens.append("FUNZIONE")
            elif result == "ritorna":
                tokens.append("RITORNA")
            elif result == "e":
                tokens.append("E")
            elif result == "o":
                tokens.append("O")
            else:
                tokens.append(("IDENTIFICATORE", result))

            i = j
            continue
        elif line[i].isdigit():
            j = i

            while j < l and line[j].isdigit():
                j += 1

            result = int(line[i:j])

            tokens.append(("NUMERO", result))

            i = j
            continue
        elif line[i] == '"':
            i += 1
            j = i

            while j < l and line[j] != '"':
                j += 1

            if j >= l:
                raise SyntaxError("stringa non terminata")

            result = line[i:j]
            tokens.append(("STRINGA", result))

            i = j + 1
            continue
        elif line[i] == '#':
            break
        elif line[i] == '>':
            if i + 1 < l and line[i+1] == '=':
                tokens.append("MAGGIORE_UGUALE")
                i += 1
            else:
                tokens.append("MAGGIORE")
        elif line[i] == '<':
            if i + 1 < l and line[i+1] == '=':
                tokens.append("MINORE_UGUALE")
                i += 1
            else:
                tokens.append("MINORE")
        elif line[i] == '+':
            tokens.append("PIU")
        elif line[i] == '-':
            tokens.append("MENO")
        elif line[i] == '*':
            tokens.append("PER")
        elif line[i] == '/':
            tokens.append("DIVISO")
        elif line[i] == '(':
            tokens.append("PARENTESI_S")
        elif line[i] == ')':
            tokens.append("PARENTESI_D")
        elif line[i] == ',':
            tokens.append("VIRGOLA")
        elif line[i] == '=':
            if i + 1 < l and line[i+1] == '=':
                tokens.append("UGUALE_A")
                i += 1
            else:
                tokens.append("UGUALE")
        elif line[i] not in " \t":
            raise SyntaxError("carattere non valido: " + repr(line[i]))
        i += 1
    return tokens


def tokenize_source(source):
    tokens = []
    indents = [0]

    righe = source.split("\n")

    for numero in range(len(righe)):
        riga = righe[numero]
        senza_rientro = riga.lstrip(" \t")

        if senza_rientro == "" or senza_rientro[0] == "#":
            continue

        rientro = riga[:len(riga) - len(senza_rientro)]
        if " " in rientro and "\t" in rientro:
            raise SyntaxError("riga " + str(numero + 1) + ": tab e spazi mischiati")

        livello = len(rientro)

        if livello > indents[-1]:
            indents.append(livello)
            tokens.append("INDENT")
        while livello < indents[-1]:
            indents.pop()
            tokens.append("DEDENT")
        if livello != indents[-1]:
            raise SyntaxError("riga " + str(numero + 1) + ": indentazione incoerente")

        try:
            tokens.extend(tokenize(senza_rientro))
        except SyntaxError as e:
            raise SyntaxError("riga " + str(numero + 1) + ": " + e.msg) from None
        tokens.append("NEWLINE")

    while len(indents) > 1:
        indents.pop()
        tokens.append("DEDENT")

    return tokens


programma = '''\
sia x = 0

se x < 1 allora
    stampa x
altrimenti
    stampa 0

# un commento

sia numeri = lista con 1, 2, 3, 4, 5 # commento inline

perogni numero in numeri allora
    stampa numero

funzione fattoriale con n
    se n <= 1 allora
        ritorna 1
    altrimenti
        ritorna n * fattoriale con n-1
'''

if __name__ == "__main__":
    for t in tokenize_source(programma):
        print(t)
