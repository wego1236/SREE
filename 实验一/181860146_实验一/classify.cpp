#include <fstream>
#include <string>
#include <iostream>
using namespace std;

int main()
{
	ifstream in;
	ofstream out("classified_by_keywords.txt");
	string words[200] =
	{
		"edit", "debug", "api", "extensions", "file", "font", "git", 
		"gramma", "install", "config", "keybindings", "language", "windows", 
		"linux", "mac", "search", "theme", "workbench", "history", "launch", 
		"command", "bar", "support", "auto", "encod"
	};
	string line;
	int flag = 0;
	for (int i = 0; words[i] != ""; i++)
	{
		flag = 0;
		in.open("VSCode_PR_Closed.txt", ios::in);
		in.seekg(std::ios::beg);
		//cout << in.tellg() << endl;
		out << "\"" << words[i] << "\":" << endl;
		while (getline(in, line))
		{
			if (line.find(words[i]) != -1)
			{
				out << line << endl;
				flag++;
			}
		}
		out << flag << endl;
		out << endl << endl << endl << endl << endl << endl;
		in.close();
	}

	return 0;
}