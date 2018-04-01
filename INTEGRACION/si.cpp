#include<iostream>
#include<math.h>
#include <omp.h>
using namespace std;

float a,b,n,h,suma,x,resultado;


int main()
{
	cout << "Ingrese limite inferior: ";  cin >> a;
	cout << "Ingrese limite superior: "; cin >> b;
	cout << "Ingrese el valor de n(debe de ser par): "; cin >> n;
	
	h = (b-a)/n;
	suma = 0.0;

	#pragma omp parallel 
	{	
		int id = omp_get_thread_num();
		int nthreads = omp_get_num_threads();
		for(int i =id ;i<n;i=i+nthreads){
			x = a + i*h;

			if(i %2 == 0){
				#pragma omp critical
					{suma = suma + 2 * sin(x);}
					

			}else{
				#pragma omp critical
					{suma = suma + 4 * sin(x);}
				
			}
		}
		


	}	
	suma = suma + sin(a) +sin(b);

	resultado = suma * (h/3);

	cout << "resultado: " << resultado << endl;
	return 0;
}



//compilarlo  g++ -std=c++11 -fopenmp -o si  si.cpp 
//correrlo    /si