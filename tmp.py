coordinates_in_degree = "77°24'12\"E"


def degree_to_decmial(coordinates_in_degree):
    nos = list(map(float,
                   coordinates_in_degree
                   .replace("°", " ")
                   .replace("'", " ")
                   .replace('"', " ")
                   .split()[:3]))

    return nos[0] + nos[1]/60 + nos[2]/3600


print(degree_to_decmial(coordinates_in_degree))

