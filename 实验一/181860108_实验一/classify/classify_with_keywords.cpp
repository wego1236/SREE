#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
int main()
{
	vector <string> issue;
	vector<vector<string>> reqs;
	fstream open_issue("C:\\Users\\Echo\\Desktop\\open_issue.txt");
	fstream closed_issue("C:\\Users\\Echo\\Desktop\\closed_issue.txt");
	fstream req("C:\\Users\\Echo\\Desktop\\req.txt");
	ofstream output("C:\\Users\\Echo\\Desktop\\result.txt");
	ofstream requirement("C:\\Users\\Echo\\Desktop\\require.txt");
	string line;
	int i = 0;
	while (getline(req, line))
	{
		vector<string> a;
		a.push_back(line);
		line.clear();
		reqs.push_back(a);
	}
	while (getline(open_issue, line))
	{	
		transform(line.begin(), line.end(), line.begin(), ::tolower);
		for (i = 0; i < reqs.size(); i++)
		{
			std::size_t found = line.find(reqs[i][0]);
			if (found != std::string::npos)
				reqs[i].push_back(line);
		}
		//issue.push_back(line);
		line.clear();	
	}
	while (getline(closed_issue, line))
	{
		transform(line.begin(), line.end(), line.begin(), ::tolower);
		for (i = 0; i < reqs.size(); i++)
		{
			std::size_t found = line.find(reqs[i][0]);
			if (found != std::string::npos)
				reqs[i].push_back(line);
		}
		//issue.push_back(line);
		line.clear();
	}
	for (i = 0; i < reqs.size(); i++)
	{
		if (reqs[i].size() > 20)
		{	requirement<< reqs[i][0] << " :" << reqs[i].size() - 1 << endl;
			output << reqs[i][0] << " :" << reqs[i].size() - 1 << endl;
			for (int j = 1; j < reqs[i].size(); j++)
				output << reqs[i][j] << endl;
			output << endl;
		}

	}

	
}