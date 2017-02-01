import numpy as np
import itertools
import pdb
import copy

def complete_minor(A):
    B = copy.copy(A)
    C = copy.copy(A)
    B[-1,-1]=1
    C[-1,-1]=0
    a_0 = float(np.linalg.det(C))
    a_1 = float(np.linalg.det(B))
    if a_1==a_0:
        return 0, 0
    else:
        stdz = (1.0/np.abs(a_1-a_0)+np.abs(a_0)/((a_1-a_0)**2));
        weight = (1.0/(stdz**2));
        return -float(a_1)/(a_1-a_0)+1, weight

def get_close_minors(x,r,i,k,iterations,distances):
    non_zero = np.where(np.logical_not(np.isnan(x[i,:])))[0]
    if len(non_zero)<(r-1):
        minor_matrices = np.zeros((0,r,r))
        NROWS = 0
    else:
        non_zero = list(non_zero)
        if k in non_zero:
            non_zero.remove(k)
        combinations = list(itertools.combinations(non_zero,r-1))
        combinations = np.array(combinations)
        dist_rep = np.zeros((len(combinations),r-1))
        for kappa in range(len(combinations)):
            dist_rep[kappa,:] = distances[combinations[kappa,:]]
        distance_to_target = np.sum(np.abs(np.log(dist_rep)-np.log(distances[k])),1);
        indices = np.argsort(distance_to_target)
        if len(indices)==1:
            combinations = combinations[indices[:1],:]
        else:
            combinations = combinations[indices[:2],:]
        it = 0
        minor_matrices = []
        NROWS = 0
        for j in range(combinations.shape[0]):
            ix = np.array(list(combinations[j,:])+[k])
            no_rows = np.sum(np.prod(np.logical_not(np.isnan(x[:,ix])),1))
            NROWS += no_rows
            have_same_col = np.where(np.sum(np.logical_not(np.isnan(x[:,list(combinations[j,:])+[k]])),1)==r)[0]
            if len(have_same_col)>=r-1:
                for tau in range(iterations):
                    perm = np.random.permutation(len(have_same_col))
                    row_ix = list(have_same_col[perm[:r-1]])+[i]
                    col_ix = list(combinations[j,:])+[k]
                    minor_matrices.append(x[row_ix,:][:,col_ix])
        if len(minor_matrices)>0:
            minor_matrices = np.array(minor_matrices)[np.random.permutation(len(minor_matrices))]
            minor_matrices = minor_matrices[:iterations]
        else:
            minor_matrices = np.zeros((0,r,r))
    return minor_matrices, NROWS

def get_all_minors(x,r,i,k,iterations):
    non_zero = np.where(np.logical_not(np.isnan(x[i,:])))[0]
    if len(non_zero)<(r-1):
        minor_matrices = np.zeros((0,r,r))
    else:
        non_zero = list(non_zero)
        if k in non_zero:
            non_zero.remove(k)
        combinations = list(itertools.combinations(non_zero,r-1))
        combinations = np.array(combinations)
        it = 0
        minor_matrices = []
        for j in range(combinations.shape[0]):
            ix = np.array(list(combinations[j,:])+[k])
            have_same_col = np.where(np.sum(np.logical_not(np.isnan(x[:,list(combinations[j,:])+[k]])),1)==r)[0]
            if len(have_same_col)>=r-1:
                for tau in range(iterations):
                    perm = np.random.permutation(len(have_same_col))
                    row_ix = list(have_same_col[perm[:r-1]])+[i]
                    col_ix = list(combinations[j,:])+[k]
                    minor_matrices.append(x[row_ix,:][:,col_ix])
        if len(minor_matrices)>0:
            minor_matrices = np.array(minor_matrices)[np.random.permutation(len(minor_matrices))]
            minor_matrices = minor_matrices[:iterations]
        else:
            minor_matrices = np.zeros((0,r,r))
    return minor_matrices

def lmc(x,tbc,method_conf,min_no_minors=5,quiet=1,close=1):
    y = copy.copy(x)
    ix_x, ix_y = np.where(tbc)
    for i in range(len(ix_x)):
        local_r = method_conf['r']  
        if not quiet:
            print i
        while True:
            print local_r
            if local_r==0:
                not_nan_x, not_nan_y = np.where(np.logical_not(np.isnan(x)))
                y[ix_x[i],ix_y[i]] = np.mean(x[ix_x,:][:,ix_y].flatten())
                break
            else:
                if close:
                    minors, NROWS = get_close_minors(x,local_r+1,ix_x[i],ix_y[i],\
                            method_conf['alg_iterations'],method_conf['distances']) 
                else:
                    minors = get_all_minors(x,local_r+1,ix_x[i],ix_y[i],\
                            method_conf['alg_iterations'])
                pred = np.zeros(minors.shape[0])
                weight = np.zeros(minors.shape[0])
                if NROWS>min_no_minors:
                    for j in range(minors.shape[0]):
                        pred[j], weight[j] = complete_minor(minors[j,:,:])
                    weight = weight/np.sum(weight)
                    y[ix_x[i],ix_y[i]] = np.sum(weight*pred)
                    break
                else:
                    local_r=local_r-1
    return y
        
if __name__=='__main__':
    pass
