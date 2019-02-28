import os


def read_input(input_file):
    '''
        reads input file and create a touple structure
        # (id, 'H' or 'V', [tags])
    '''
    f = open(input_file, 'r')
    images_num = f.readline().strip()
    input_touple = []
    # (id, 'H' or 'V', [tags])
    for i, line in enumerate(f):
        line = line.strip()
        splitted = line.split(' ')
        alignment = splitted[0]
        tags = splitted[2:]
        input_touple.append(([i], alignment, tags))
    return images_num, input_touple


def interested(s1, s2):
    t1 = set(s1[2])
    t2 = set(s2[2])
    return min(len(t1-t2), len(t2-t1), len(t1.union(t2)))

def score(sol):
    total_score = 0
    for i in xrange(len(sol) - 1):
        total_score += interested(sol[i], sol[i+1])
    return total_score

def generate_output(sol, input_file):
    pass

def vertical_merger(in_processed):
    pass

def optimizer(final_processed):
    opt_processed = sorted(final_processed, key=lambda s: len(s[2]))
    return opt_processed

def main(input_file):
    # Reads input
    if os.path.exists(input_file):
        img_num, in_processed = read_input(input_file)
        print img_num, in_processed
    else:
        print "File does not exists"

    # (id, 'H' or 'V', [tags])

    # merge verticals
    final_processed = vertical_merger(in_processed)

    # preform solution
    # output format is [[id], [id,id], [id], ...]
    sol = optimizer(final_processed)

    # score our solution
    
    score(sol)

    # generate output
    #sol = [[0], [1,2], [3]]
    generate_output(sol, input_file)
    

if __name__ == "__main__":
    main('a_example.txt')
