#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage %s input_file out_training_file out_validation_file validation_sample_ratio [seed]

Split a TextCorpus into a Training and validation set

This will output 2 textfiles; one out_validation_file
that contains random lines from the input (validation_sample_ratio \% of the lines are used)
file and a file out_training_file that contains all other files
"""

import sys
import random

def get_lines(file_name):
    file = open(file_name)
    lines = range(sum(1 for line in file))
    file.close()
    return lines

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print __doc__ % sys.argv[0].split("/")[-1]
        sys.exit(1)

    in_file, out_training, out_validation, validation_sample_ratio = sys.argv[1:5]


    if len(sys.argv) >= 6:
        print("seeding prng with {}".format(sys.argv[5]))
        random.seed(sys.argv[5])


    print('counting lines')
    lines = get_lines(in_file)

    validation_samples = int((float(len(lines)) / 100) * float(validation_sample_ratio))
    print("generating training sets from {} with {} lines for validation".format(in_file, validation_samples))


    #shuffle the lines
    random.shuffle(lines)

    #create the sets
    validation_lines = lines[:validation_samples]

    print("extracted {} random lines for validation from a total of {} lines".format(len(validation_lines), len(lines)))

    input_file = open(in_file)
    train_out_file = open(out_training, 'w')
    validation_out_file = open(out_validation, 'w')

    for num, line in enumerate(input_file):
        if num in validation_lines:
            validation_out_file.write(line)
        else:
            train_out_file.write(line)


    train_out_file.close()
    validation_out_file.close()
    input_file.close()

    print("done")
    print('')
