#include <iostream>
#include <fstream>
#include <iomanip>
 
using namespace std;
 
void trapezoide (int n, float h, float *f, float & sum);
void simpson (int n, float h, float *f, float & sum);
 
int main() {
 
   cout << "Integracion numerica\n\n";
 
   ifstream label1 ("datos//datos.in");
 
   int n, i;
 
   float h, *f, sum;
 
   label1 >> n >> h;
 
   f = new float [n];
 
   cout << "Numero de valores de f(x) = " << n << "\n\n";
 
   cout << "Valor de h = " << h << "\n\n";   
 
   cout << "Valores de f(x)\n   f(x)\n";
 
   for (i = 0; i < n; i++){
 
      label1 >> f[i];
 
      cout << setw(5) << setiosflags(ios::right) << f[i] << "\n";
 
   }
 
   cout << endl;
 
   sum = 0;
 
   simpson (n, h, f, sum);
 
   cout << "Regla de Simpson\n";
 
   cout << "area = " << sum << "\n\n";
 
   sum = 0;
 
   trapezoide (n, h, f, sum);
 
   cout << "Regla del Trapezoide\n";
 
   cout << "area = " << sum << "\n\n";
 
   return 0;
 
}
 
void trapezoide (int n, float h, float *f, float & sum) {
 
   int i;
 
   for (i = 1; i < n -1; i+=2){
 
      sum = sum + (h/2)*(f[i-1] + 2*f[i] + f[i + 1]);
 
   }
 
}
 
void simpson (int n, float h, float *f, float & sum) {
 
   int i;
 
   for (i = 1; i < n -1; i+=2){
 
      sum = sum + (h/3)*(f[i-1] + 4*f[i] + f[i + 1]);
 
   }
 
}