#include <ctime>
#include <cmath>
#include <iostream>
using namespace std;

int main()
{
	float x, y, interval=.0000001;            //define x and y coordiantes
	long int count_inside = 0, points=0;    //how many tries you want
	for(x=0; x<=1; x+=interval)
	{
		for(y=0; y<=1; y+= interval)
		{
			if(x*x+y*y<=1)                //check if square root is equal or less to 1
				count_inside++;                //if it is then add 1 to count_inside
			points++;
		}
	}
	//printf("%lf\n", 4*double(count_inside)/points);
	cout << 4*double(count_inside)/points << endl;    //calculate the pi by the formula given above
}
