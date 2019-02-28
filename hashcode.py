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
    sorted_slds = sorted(final_processed, key=lambda s: len(s[2]))
    done = [0] * len(sorted_slds)
    done[0] = 1
    output = [sorted_slds[0]]

    for _ in range(1, len(sorted_slds)):
        sld = output[-1]
        tags = sld[2]
        max_intr = -1
        for j in range(len(sorted_slds)):
            if done[j]:
                continue

            other_sld = sorted_slds[j]
            other_tags = other_sld[2]

            intr = interested(sld, other_sld)
            if intr > max_intr:
                max_intr = intr
                best_match = j

            if intr == max_possible_intrested(sld, other_sld):
                break

        done[j] = 1
        output.append(sorted_slds[j])
    
    return output

def max_possible_intrested(s1, s2):
    return min(len(s1), len(s2)) / 2

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
