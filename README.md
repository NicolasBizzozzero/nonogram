# nonogram
<p align="center">
    <img src="https://github.com/NicolasBi/nonogram/blob/master/nonogram/res/tux.gif?raw=true" alt="tux gif"/>
</p>


# Installation
The following line will install the **nonogram** package on your computer and add an entry point to the software
```shell
~$ pip install nonogram
```

# Usage
Launching the software is pretty straightforward. All the parameters have been already configured to help you during your day-to-day nonogram solving routine. Here's the command to use for solving the grid whose constraints has been saved in the file **constraints.txt** :
```shell
~$ nonogram constraints.txt
```

# Requirements
The linear-programming solver need the <b><a href="http://www.gurobi.com">Gurobi Optimizer</a></b> software to be installed and properly configured.

# Dependencies
* numpy ≥ 1.12.0
* docopt ≥ 0.6.2

# Contributing
1. Fork the project.
2. Create your feature branch : `git checkout -b my-new-feature`.
3. Commit your changes : `git commit -am 'Added some cool feature !'`.
4. Push to the branch  : `git push origin my-new-feature`.
5. Submit a pull request.

# Todo
* Add the following parameters :
    * encoding
    * verbose (tell when a bloc has been placed)
    * progressbar
    * output = (stdout in raw format | picture in window | picture saved)
    * picture_output_path
    * grid_path (with an non-empty grid)
* Add a decorator outputing the current grid when a ctrl + c happen

# Acknowledgments
We would like to thanks the **Pierre et Marie Curie University** (UPMC), for giving us the possibility and authorization to release this project.  
We also want to thanks professor <a href="http://www-poleia.lip6.fr/~escoffier/">Bruno Escoffier</a> for offering us the knowledge and oppoortunities needed to build this software.


# License
This project is licensed under the GPLv3 License - see the [LICENSE.txt](LICENSE.txt) file for details.

# References

