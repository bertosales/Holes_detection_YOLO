import ezdxf

# Carregue o arquivo DXF a ser analisado
doc = ezdxf.readfile("C:\\Users\\yansa\\PycharmProjects\\PycharmProjects\\pythonProject1\\TCC\\peca_1.dxf")

retangulos = []
furos = []
num_furo = 0

msp = doc.modelspace()
for entity in msp:
    if entity.dxftype() == "LWPOLYLINE":
        retangulos.append(list(entity.get_points()))
    elif entity.dxftype() == "CIRCLE":
        furo = entity.dxf.center
        furos.append(furo)
        num_furo += 1
        print(f"Raio do Furo {num_furo}: {entity.dxf.radius}mm")

print("\n")
if len(retangulos) > 0:
    retangulo = retangulos[0]

    x_min = min([point[0] for point in retangulo])
    x_max = max([point[0] for point in retangulo])
    y_min = min([point[1] for point in retangulo])
    y_max = max([point[1] for point in retangulo])

    for j, furo in enumerate(furos):
        x_furo = furo.x
        y_furo = furo.y

        dist_lado_esquerdo = x_furo - x_min
        dist_lado_direito = x_max - x_furo
        dist_lado_superior = y_max - y_furo
        dist_lado_inferior = y_furo - y_min

        print(f"  Furo {j + 1}:")
        print(f"    Lado esquerdo: {dist_lado_esquerdo:.2f} mm")
        print(f"    Lado direito: {dist_lado_direito:.2f} mm")
        print(f"    Lado superior: {dist_lado_superior:.2f} mm")
        print(f"    Lado inferior: {dist_lado_inferior:.2f} mm")