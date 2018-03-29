#include<iostream>
#include<math.h>
#include <omp.h>
using namespace std;

float a,b,n,h,suma,x,resultado;


int main()
{
	cout << "Ingrese limite inferior: ";  cin >> a;
	cout << "Ingrese limite superior: "; cin >> b;
	cout << "Ingrese el valor de n(debe de ser par): "; 	  cin >> n;
	//cout << "Ingrese funcion a evaluar: "; cin >> f;
	h = (b-a)/n;
	suma = 0.0;
	#pragma omp parallel for
		for(int i =1 ;i<n;i++){
			x = a + i*h;

			if(i %2 == 0){
				suma = suma + 2 * sin(x);

			}else{
				suma = suma + 4 * sin(x);

			}
		}
	suma = suma + sin(a) +sin(b);

	resultado = suma * (h/3);

	cout << "resultado: " << resultado << endl;
	return 0;
}



//compilarlo  g++ -std=c++11 -fopenmp -o si  si.cpp 
//correrlo    /si