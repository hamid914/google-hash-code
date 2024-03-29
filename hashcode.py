import os
from tqdm import tqdm
import random

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
        input_touple.append(([i], alignment, set(tags), 0))
    return images_num, input_touple


def interested(s1, s2):
    '''
        receives two slide and returns the interested factor
    '''
    t1 = s1[2]
    t2 = s2[2]
    return min(len(t1-t2), len(t2-t1), len(t1.intersection(t2)))

def interested_idx(processed, i1, i2):
    processed_len = len(processed)
    if 0 <= i1 < processed_len and 0 <= i2 < processed_len:
        return interested(processed[i1], processed[i2])
    return 0

def score(sol):
    '''
        score our final solution
    '''
    total_score = 0
    for i in xrange(len(sol) - 1):
        total_score += interested(sol[i], sol[i+1])
        #print i, interested(sol[i], sol[i+1])
    return total_score

def generate_output(sol, input_file):
    '''
        receives the final solution and writes the output in right format
    '''
    num_slides = len(sol)
    with open(input_file+'.out', 'w') as f:
        f.write(str(num_slides))
        f.write('\n')
        for slide in sol:
            f.write(' '.join([str(s) for s in slide[0]]))
            f.write('\n')

def vertical_merger(in_processed):
    '''
        merges all vertical slides into horizental slides
    '''
    verticals = []
    horizontals = []
    for image in in_processed:
        if image[1] == 'V':
            verticals.append(image)
        else:
            horizontals.append(image)
    verticals = sorted(verticals, key=lambda x: len(x[2]))
    for i in range(0, len(verticals) - 1, 2):
        t1 = verticals[i][2]
        t2 = verticals[i + 1][2]
        horizontals.append(
            [verticals[i][0] + verticals[i + 1][0], 'H', t1.union(t2)])
    return horizontals

def random_swap(opt_processed, swaps):
    opt_processed_len = len(opt_processed)
    for _ in tqdm(range(swaps)):
        i1 = random.randint(0, opt_processed_len - 1)
        i2 = random.randint(0, opt_processed_len - 1)
        i1, i2 = max(i1, i2), min(i1, i2)
        if i1 - i2 < 2:
            continue
        cur_interested = 0
        cur_interested += interested_idx(opt_processed, i1 - 1, i1)
        cur_interested += interested_idx(opt_processed, i1, i1 + 1)
        cur_interested += interested_idx(opt_processed, i2 - 1, i2)
        cur_interested += interested_idx(opt_processed, i2, i2 + 1)

        swp_interested = 0
        swp_interested += interested_idx(opt_processed, i2 - 1, i1)
        swp_interested += interested_idx(opt_processed, i1, i2 + 1)
        swp_interested += interested_idx(opt_processed, i1 - 1, i2)
        swp_interested += interested_idx(opt_processed, i2, i1 + 1)

        if swp_interested > cur_interested:
            opt_processed[i1], opt_processed[i2] = opt_processed[i2], opt_processed[i1]
    return opt_processed

def optimizer(final_processed):
    '''
        optimize the list of all horizental slides into the best sequence
    '''
    sorted_slds = sorted(final_processed, key=lambda s: len(s[2]), reverse=True)
    done = [0] * len(sorted_slds)
    done[0] = 1
    output = [sorted_slds[0]]

    sorted_slds_len = len(sorted_slds)
    for i in tqdm(xrange(1, sorted_slds_len)):
        sld = output[-1]
        tags = sld[2]
        max_intr = -1
        max_lookup = 0

        best_match = None
        j = i
        k = i
        for _ in xrange(sorted_slds_len):
            j = (j + 1) % sorted_slds_len
            if done[j]:
                continue
            other_sld = sorted_slds[j]
            other_tags = other_sld[2]

            intr = interested(sld, other_sld)
            if intr > max_intr:
                max_intr = intr
                best_match = j
                max_lookup = 0
            elif intr == max_intr and len(sorted_slds[j][2]) < len(sorted_slds[best_match][2]):
                max_intr = intr
                best_match = j
                max_lookup = 0
            max_lookup += 1

            if max_lookup > 1000 and max_intr >= 0:
                break

            #if intr == max_possible_intrested(sld, other_sld):
            #    break

        done[best_match] = 1
        output.append(sorted_slds[best_match])

    return output

def max_possible_intrested(s1, s2):
    '''
        calculates max possible score between two given slides
    '''
    return min(len(s1), len(s2)) / 2


def main(input_file):
    # Reads input
    if os.path.exists(input_file):
        img_num, in_processed = read_input(input_file)

        #print img_num, in_processed
        # ([id], 'H' or 'V', [tags])

        # merge verticals
        final_processed = vertical_merger(in_processed)

        # preform solution
        # [([id], 'H' or 'V', [tags])]
        opt_processed = optimizer(final_processed)

        opt_processed = random_swap(opt_processed, 10000)
        # score our solution
        s = score(opt_processed)
        print "Score is:\t{}".format(s)

        # generate output
        generate_output(opt_processed, input_file)

    else:
        print "File does not exists"


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
