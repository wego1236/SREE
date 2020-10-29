#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
int main()
{
	vector <string> labels;
	fstream f("C:\\Users\\Echo\\Desktop\\raw.txt");
	ofstream f2("C:\\Users\\Echo\\Desktop\\notraw.txt");
	string line;
	int i = 0; int count = 0;
	while (getline(f, line))
	{
		for ( i= 0; i < labels.size(); i++)
		{
			if (line == labels[i])
				break;
		}
		if (i == labels.size())
			labels.push_back(line);
		transform(line.begin(), line.end(), line.begin(), ::tolower);
		f2 << line<<endl;
		line.clear();
		count++;
	}
	cout << count << " " << labels.size();
}