import ac

def changeElementBgColor(element, Bgr, Bgb, Bgg):
    ac.setBackgroundColor(element, Bgr, Bgb, Bgg)
    ac.setBackgroundOpacity(element, 1)
    ac.drawBackground(element, 1)


def changeElementText(element, text):
    ac.setText(element, text)