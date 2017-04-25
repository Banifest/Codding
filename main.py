from coders import hemming
from coders.interference import GenInterference

if __name__ == '__main__':
    #  print(GetCombinations(4, 3))
    c = 'a'
    a = hemming.Coder(15)
    print(a.Encoding(18801))
    print(a.Decoding([1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1]))
#    print(a.Encoding(11))
#    print(a.Encoding(10))
    #    print(a.Decoding([1,0,1,1,0,0,0]))
    #    for x in range(31,0,-1):
    #        print(a.Encoding(x))
    #        print(a.Decoding(a.Encoding(x)))

    print(GenInterference(a.Encoding(13), 0.0000000002))


else:
    pass
