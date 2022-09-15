from errorHandler import handleError

def childToParent(child, parent):
    try:
        parent.children.append(child)
    except Exception as err:
        handleError(err)