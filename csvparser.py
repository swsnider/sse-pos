import sys


def main():
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            trans_id = line[0]
            items = eval(line[2].replace(";", ","))
            for item in items:
                print "UPDATE LineItem2 SET transaction='%s' WHERE LineItem2.key = '%s';" % (trans_id, item)


if __name__ == "__main__": main()