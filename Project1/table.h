#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include "D:\מכון לב\שנה ד\אקסלנטים\jsoncpp\include\json\json.h"
//#include "jsoncpp\include\nlohmann\json.hpp"
class RowDescription {
public:
	std::string m_nameFile;
	int m_rowNumber;
	RowDescription();
	RowDescription(std::string nameFile, int rowNumber)
	{
		m_rowNumber = rowNumber;
		m_nameFile = nameFile;

	}

	std::string show() {

		return "( " + m_nameFile + " " + std::to_string(m_rowNumber) + " )";
	}


};
class vectorWord {
public:
	int m_numOfChar;
	//int m_numberRowInFile;
	std::string m_words;
	RowDescription m_DescriptionVector;

};

class Table
{
private:

	int m_row;
	std::string m_path;
	std::map<std::string, RowDescription> m_tableMap;
public:
	Table(int numOfchar, std::string path)
	{
		m_path = path;
		std::fstream(myfile);

		myfile.open(m_path);
		int countRow = 0;
		for (std::string line; getline(myfile, line); )//run line by line
		{
			countRow++;
			for (char i = 'a'; i <= 'z'; i++)
			{
				for (char j = 'a'; j <= 'z'; j++)
				{
					vectorWord tmp;
					tmp.m_numOfChar = 2;
					tmp.m_words = i + j;
					for (i = 0; i < line.length();i++)
					{

						char a = line[i];
						char b = line[i + 1];
						if (tmp.m_words == std::to_string(a + b))
						{
							tmp.m_DescriptionVector = RowDescription(path, 2);
							m_tableMap.emplace(tmp.m_words, tmp.m_DescriptionVector);

						}
					}



				}
			}


		}



		myfile.close();
		Json::Value jsonMap;
		std::map<std::string, RowDescription>::const_iterator it = m_tableMap.begin(), end = m_tableMap.end();
		for (; it != end; ++it) {

			jsonMap[it->first] = "( " + it->second.m_nameFile + " " + std::to_string(it->second.m_rowNumber) + " )";
			// ^ beware: std::to_string is C++11
		}
		//todo
		//Json::Value root;
		//root["2Char"] = "m_Table";
		//root["Map2char"] = jsonMap; // use the Json::Value instead of mymap

		//Json::StreamWriter writer = ;
		//const std::string output = writer.write(root);

		std::ofstream file_id;
		file_id.open("fileGoogle.txt");

		Json::Value value_obj;
		//populate 'value_obj' with the objects, arrays etc.

		Json::StyledWriter styledWriter;
		file_id << styledWriter.write(value_obj);

		file_id.close();
		//
	}
	void setPath(std::string path)
	{
		m_path = path;
	}

};
