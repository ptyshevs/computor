
### Bonuses

* Error management
* Input\output in a natural norm
* Display intermediate steps
* Handle different variable names
* Regex
* Jokes

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

`f(x) = 1 + x - 1` should be simplified to `f(x) = x`, but `f(x) = 1 + 2 * (x - 1) = 2 * x - 1`.

If one doesn't implement this simplification, all the bonuses are discarded.