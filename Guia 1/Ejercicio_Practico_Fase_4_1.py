mis_amigos = []
for i in range(1,6):
    nombre = input(f"Ingresa el nombre de tu amigo {i}: ")
    mis_amigos.append(nombre)
print(" ")
for amigo in mis_amigos:
    print(f"Hola {amigo}.")