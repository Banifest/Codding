from GUI.MainWindow import InitMainWindow
from coders.convolutional import сonvolutional

if __name__ == '__main__':
    InitMainWindow()
    #    a = hemming.Coder(5)
    """print(a.Encoding(18801))
    print(a.Decoding([1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1]))
    print(a.Encoding(11))
    print(a.Encoding(10))
    print(a.Decoding([1, 0, 1, 1, 1, 1, 0]))
    for x in range(31,0,-1):
        print(a.Encoding(x))
        print(a.Decoding(a.Encoding(x)))

   # print(GenInterference(a.Encoding(13), 0.0000000002))
"""
    """
    b = cyclical.Coder(4)

    print(b.Encoder(13))
    print(b.Decoder([1, 1, 0, 1, 0, 0, 0]))
    """
    c = сonvolutional.Coder(2, [7, 5], 1, 2, 2)

# print(c.Encoding([0, 1, 1, 0]))



else:
    raise Exception()
