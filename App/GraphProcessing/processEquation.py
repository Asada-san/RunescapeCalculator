def get_data(user_input):

    windowHeight = user_input['windowHeight']
    windowWidth = user_input['windowWidth']

    if windowHeight % 2 == 0:
        yMax = (windowHeight - 1) / 2
        yMin = - windowHeight + yMax
    else:
        yMax = windowHeight / 2
        yMin = -yMax

    if windowWidth % 2 == 0:
        xMax = (windowWidth - 1) / 2
        xMin = - windowWidth + xMax
    else:
        xMax = windowWidth / 2
        xMin = -xMax

    split_eq = user_input['equation'].split("=")

    x = range(int(xMin) + 1, int(xMax) + 1)
    y = eval(split_eq[1])

    data = {'x': list(x),
            'y': list(y)}

    return data
