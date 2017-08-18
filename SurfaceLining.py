print("This program calculates the minimum length and width (in inches) of the lining roll you need to cover all your surface area.")
lengths = []
widest = 0
total = 0
more_input = True
while more_input:
    area_string = input(
        "Enter 'length, width' in this format to add surface area. Enter 'quit' to find out your total: ")
    if area_string.startswith('q'):
        if len(lengths) == 0:
            print("You have not entered any area to calculate.")
        else:
            more_input = False
            for length in lengths:
                total = total + length
            print("You need a roll " + str(total) + " inches long and " + str(widest) + " inches wide.")
    elif ',' in area_string:
        dimensions = area_string.split(", ")
        i = 0
        for x in dimensions:
            integer_dimension = int(x)
            dimensions[i] = integer_dimension
            i = i + 1
        if dimensions[0] > dimensions[1]:
            length = dimensions[0]
            width = dimensions[1]
        else:
            length = dimensions[1]
            width = dimensions[0]
        if width > widest:
            widest = width
        lengths.append(length)
