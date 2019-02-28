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
    return min(len(t1-t2), len(t2-t1), len(t1.intersection(t2)))

def score(sol):
    total_score = 0
    for i in xrange(len(sol) - 1):
        total_score += interested(sol[i], sol[i+1])
        print i, interested(sol[i], sol[i+1])
    return total_score

def generate_output(sol, input_file):
    num_slides = len(sol)
    with open(input_file+'.out', 'w') as f:
        f.write(str(num_slides))
        f.write('\n')
        for slide in sol:
            f.write(' '.join([str(s) for s in slide[0]]))
            f.write('\n')

def vertical_merger(in_processed):
    verticals = []
    horizontals = []
    for image in in_processed:
        if image[1] == 'V':
            verticals.append(image)
        else:
            horizontals.append(image)
        if len(verticals) > 1:
            t1 = set(verticals[0][2])
            t2 = set(verticals[1][2])
            horizontals.append([verticals[0][0] + verticals[1][0], 'H', list(t1.union(t2))])
            del verticals[:]
    return horizontals

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

    # ([id], 'H' or 'V', [tags])

    # merge verticals
    final_processed = vertical_merger(in_processed)

    # preform solution
    # [([id], 'H' or 'V', [tags])]
    sol = optimizer(final_processed)
    
    # score our solution
    s = score(sol)
    print "Score is:\t{}".format(s)
    
    # generate output
    generate_output(sol, input_file)
    

if __name__ == "__main__":
    main('a_example.txt')
