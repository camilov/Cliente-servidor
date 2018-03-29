#include<iostream>
using namespace std;

double a,b,g,fa,x1,fx1,fb,w;

void main()

{
	cout << "digite primer valor: "; cin >> a;
	cout << "digite segundo valor: "; cin >> b;
	h = (b-a)/2
	x1 = a + h;
	fa = exp(-1 *pow(a,2));
	fb = exp(-1 *pow(b,2));
	fx1 = exp(-1 *pow(x1, 2));
	w = (h / 3)*(fa + (4*fx1)+fb);
	cout << "el resultado es: " << w << endl;
	system("pause");


}