print ("--Bienvenido a nuestro simulador de parque de diversiones--")
print (" ")
juego = input ("En el momento solo tenemos disponible la montaña rusa, desear subir (si/no): ")

if juego == "si":
    print ("Perfecto, confirma los siguientes datos")
    print (" ")
    print ("Confirmame tu estatura y tu edad")
    Estatura = input ("Estatura (cm): ")
    Float = float(Estatura)
    Edad = input ("Edad: ")
    Entero = int(Edad)

    if Float >= 150 and Entero >= 12:
        print ("Acceso permitido, espero que disfrutes esta experiencia que te ofrecemos")

    else:
        print ("Acceso denegado, no cumples los requisitos. Perdon")

else:
    print ("Vuelve pronto, te esperamos con ansias")

    