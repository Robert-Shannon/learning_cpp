#include <iostream>

int doubler(int x)
{
    return x * 2;
}


int main()
{
	std::cout << "Enter a number: ";
    int x{}; // define variable x to hold user input (and value-initialize it)
    std::cin >> x;
	int x2 { doubler(x) };

    std::cout << "You entered " << x << " and " << x << " doubled is " << x2 << '\n';
    return 0;
}



int old_main()
{
    std::cout << "Hello, world!";
	// return 0;
	std::cin.clear(); // reset any error flags
	std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // ignore any characters in the input buffer until we find an enter character
	std::cin.get(); // wait for user to press enter

	std::cout << "Enter two numbers separated by a space: ";

    int x{}; // define variable x to hold user input (and value-initialize it)
    int y{}; // define variable y to hold user input (and value-initialize it)
    std::cin >> x >> y; // get two numbers and store in variable x and y respectively

    std::cout << "You entered " << x << " and " << y << '\n';
    return 0;
}