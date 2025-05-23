import numpy as np
import sys
import csv

# Needleman-Wunsch algorithm, here we set the values for match, mismatch and gap
match = +1
gap = -2
mismatch = -1

# Next I build the matrices for the algorithm with the sequences as input
def build_matrices(s1, s2):
    
    M = len(s1)
    N = len(s2)
   #using the lenghts of the sequences to make the number matrix and the trace matrix 
    matrix = np.zeros((N+1, M+1))
    trace_mat = np.zeros((N+1, M+1), dtype=object)

   # filling the first row and column of the matrix with the gap values, it will also add the movement to the trace matrix
    for i in range(N+1):
        matrix[i, 0] = i * gap  # [0, -2, -4...] on the y axis
        if i > 0:    
            trace_mat[i, 0] = 'V'  

    for j in range(M+1):            # [0, -2, -4...] on the x axis
        matrix[0, j] = j * gap
        if j > 0:
            trace_mat[0, j] = 'H'  

    # Here we fill the matrix with the values of the scores, we will also add the movement to the trace matrix
    # we will use the max score between the diagonal, vertical and horizontal scores. if the characters match, it rewards
    # with match score if not, it will penalize with mismatch score. vertical more is a gap in the first sequence, horizontal
    # move is a gap in the second sequence
    for i in range(1, N+1):
        for j in range(1, M+1):
            if s2[i-1] == s1[j-1]:
                diag_score = matrix[i-1, j-1] + match     
            else:
                diag_score = matrix[i-1, j-1] + mismatch  
   
            vert_score = matrix[i-1, j] + gap  
            horz_score = matrix[i, j-1] + gap  

           # here the max score will be the the value for the alignment or where it will go 
            max_score = max(diag_score, vert_score, horz_score)
            matrix[i, j] = max_score

           
          # this will set up the the trace map for the sequences to work. PS. this took me a whole day of debugging to figure out
            if max_score == vert_score:
                trace_mat[i, j] = 'V'
            elif max_score == horz_score:
                trace_mat[i, j] = 'H'
            else:
                trace_mat[i, j] = 'D'

    return matrix, trace_mat
# this function will recieve the tracemat and sequences to create the new alignments. 
def traceback(s1, s2, trace_mat):
  
    aligned_s1 = ''
    aligned_s2 = ''

    i, j = len(s2), len(s1)
#it iterates throught the tracemat, if the move is diagonal, it will add the characters to the aligned sequences
#if its a vertical move, it will add a gap to the first sequence. if its a horizontal move, it will add a gap to the second sequence
    while i > 0 or j > 0:
        move = trace_mat[i, j]
        if move == 'D':  
            aligned_s1 = s1[j-1] + aligned_s1
            aligned_s2 = s2[i-1] + aligned_s2
            i -= 1
            j -= 1
        elif move == 'V':  
            aligned_s1 = '-' + aligned_s1
            aligned_s2 = s2[i-1] + aligned_s2
            i -= 1
        else:  
            aligned_s1 = s1[j-1] + aligned_s1
            aligned_s2 = '-' + aligned_s2
            j -= 1

    return aligned_s1, aligned_s2

def main():
   if len(sys.argv) < 2:
        sys.exit(1)

   input_file = sys.argv[1]
   with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader, None)

       # this was for a specific test case where it returned "sequence1 sequence2 7" so it passes over this test case so the output is correct   
        if first_row and first_row[0].lower() == 'sequence1' and first_row[1].lower() == 'sequence2':
              pass  
        else:
            # this will iterate over the csv file and extract and trims the sequence from the row. then it will build the matrices and trace matrices and go though the traceback function
            # throught the traceback function for the aligned sequences and the score. Once we have those values we print them out 
           if first_row and len(first_row) == 2:
               seq1, seq2 = first_row[0].strip(), first_row[1].strip()
               matrix, trace_mat = build_matrices(seq1, seq2)
               aln1, aln2 = traceback(seq1, seq2, trace_mat)
               score = int(matrix[len(seq2), len(seq1)])
               print(f"{aln1} {aln2} {score}")

     #just in case theres no header sentence on other csv files
        for row in reader:
         if len(row) != 2:
            continue  

         seq1, seq2 = row[0].strip(), row[1].strip()
         matrix, trace_mat = build_matrices(seq1, seq2)
         aln1, aln2 = traceback(seq1, seq2, trace_mat)
         score = int(matrix[len(seq2), len(seq1)])
         print(f"{aln1} {aln2} {score}")
          


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()