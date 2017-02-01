#include <math.h>
#include<stdio.h>
#include <stdlib.h>
#include <gsl/gsl_matrix.h>


void non_zero_indices(gsl_vector *v, int lenz, int *places, int *nz) {
    int i;
    for (i = 0; i < lenz; i++) {
        double a = gsl_vector_get(v, i);
        if (a!=0) {
            places[*nz] = i;
            *nz = *nz+1;
        }
    }
}


void random_solution(int *row_indices, gsl_matrix *data, int no_nz, 
                     gsl_vector *userdata, int *event_ix, int pred_ix, 
                     double *prediction, double *weight) {

    int r1 = rand() % no_nz;
    int r2 = rand() % no_nz;
    while (r1==r2) {
        r2 = rand() % no_nz;
    }

    double A11, A12, A13, A21, A22, A23, A31, A32;
    A11 = log(gsl_matrix_get(data,event_ix[0],row_indices[r1]));
    A12 = log(gsl_matrix_get(data,event_ix[1],row_indices[r1]));
    A13 = log(gsl_matrix_get(data,pred_ix,row_indices[r1]));
    A21 = log(gsl_matrix_get(data,event_ix[0],row_indices[r2]));
    A22 = log(gsl_matrix_get(data,event_ix[1],row_indices[r2]));
    A23 = log(gsl_matrix_get(data,pred_ix,row_indices[r2]));
    A31 = log(gsl_vector_get(userdata,event_ix[0]));
    A32 = log(gsl_vector_get(userdata,event_ix[1]));

    double a0, a1;
    a0 = A11*A22*0-A11*A23*A32-A12*A21*0+A12*A23*A31+A13*A21*A32-A13*A22*A31;
    a1 = A11*A22*1-A11*A23*A32-A12*A21*1+A12*A23*A31+A13*A21*A32-A13*A22*A31;

    double stdz;
    stdz = 1.0/fabs(a1-a0)+fabs(a0)/pow(a1-a0,2);
    *prediction = -a1/(a1-a0)+1;
    *weight = 1.0/pow(stdz,2);
    if isinf(*prediction) {
        *prediction = 0;
        *weight = 0;
    }
}


double weighted_average(double *toav, double *weightz, int lenz) {
    int i;
    double weight_sum;
    double sum;
    for (i=0; i < lenz; i++) {
        weight_sum = weight_sum + weightz[i];
        sum = sum + weightz[i]*toav[i];
    }
    return sum/weight_sum;
}


int main(int argc, char *argv[]) {
    int ev_pred = *argv[1]-'0';
    FILE *fp;
    FILE *fp2;

    fp = fopen("/Users/blythed/work/repo/running_calculator/male.txt", 
               "r");
    fp2 = fopen("topredict.txt","r");

    int lenz = 5735;

    gsl_vector *topred = gsl_vector_alloc(10);
    gsl_vector_fscanf(fp2, topred); 
    int events[2];
    int ne = 0;
    int i;
    non_zero_indices(topred,10,events,&ne);

    gsl_matrix *a = gsl_matrix_alloc(10,lenz);
    gsl_matrix_fscanf(fp, a); 

    gsl_vector *u = gsl_vector_alloc(lenz);
    gsl_vector *v = gsl_vector_alloc(lenz);
    gsl_vector *w = gsl_vector_alloc(lenz);

    gsl_matrix_get_row(u, a, ev_pred);
    gsl_matrix_get_row(v, a, events[0]);
    gsl_matrix_get_row(w, a, events[1]);
    gsl_vector_mul(u, v);
    gsl_vector_mul(u, w);

    int places[lenz];
    int nz = 0;
    non_zero_indices(u,lenz,places,&nz);

    int iterations = 1000;;
    double prediction;
    double weight;
    double solutions[iterations];
    double weights[iterations];

    for (i = 0; i < iterations; i++) {
        random_solution(places, a, nz, topred, events, ev_pred, 
                        &prediction, &weight);
        solutions[i] = prediction;
        weights[i] = weight;
    }

    printf("%g\n",exp(weighted_average(solutions,weights,iterations)));
    return 0;

}
