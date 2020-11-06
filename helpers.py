def delete_child_contours(contours,hierarchy):
    #
    new_contours = []
    for i in range(len(hierarchy)):
        if hierarchy[i][3] == -1:
            new_contours.append(contours[i])
    return new_contours

def switch_letters_to_numbers(string):
    # Tesseract often mistakes some digits for letters.
    # This function tries to corrects the most common mistakes.
    # WARNING: Use this function only when images don't contain text.
    new_string = ''
    for i in range(len(string)):
        if string[i] == 'g':
            new_string += '9'
        elif string[i] == 'T':
            new_string += '7'
        elif string[i] == 'O':
            new_string += '0'
        elif string[i] == ']':
            new_string += '1'
        elif string[i] == '?':
            new_string += '2'
        elif string[i] == '$':
            new_string += '5'
        else:
            new_string += string[i]
    return new_string

