#include<stdio.h>
#include<stdlib.h>

int main(){
  int n;
  scanf("%d", &n);
  if(n < 3){
    printf("0\n");
  }
  int* p = new int[n];

  for(int i=0; i<n; i++){
    scanf("%d", &p[i]);
  }

  int sum = 0;
  int left = 0;
  int right = 0;
  int A;
  for(int i = 1; i < n-1; i++){
    A = p[i];
    left = 0;
    right = 0;
    for(int j=0; j<i; j++){
      if(p[j] < A){
        left++;
      }
    }
    for(int j=i+1; j<n; j++){
      if(p[j] < A){
        right++;
      }
    }

    //printf("A=%d,left=%d,right=%d\n", A, left, right);
    sum += left * right;
  }

  printf("%d\n", sum);
}