
### Computor v1 bonuses

* Error management
* Input\output in a natural norm
* Display intermediate steps
* Handle different variable names
* Regex
* Jokes

### Computor v2 bonuses

* History
* Environment
* Verbose mode
* Functions
* Truly Rational

Token can be one of the following:

* Rational or Complex Number
* Function
* Operators: +-/*^ and assignment sign =
* Matrix
* Polynomial expression

Functions design

Function are hard to handle only during creation, otherwise standard shunting yard algorithm works with them as expected.
In order to create a function, one should do something like `fun_name(x) = x^2 + 3 * x - 3`. Special attention is given to
simplification process:
