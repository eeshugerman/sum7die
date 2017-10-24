
# introduction
In order to determine the distribution of scores, we need to generate the following data for each possible score: the number of gumball sequences which produce the score ("paths"), and the number of gumballs in each sequence ("steps"). In other words, we need the distribution of number of paths vs number of path steps for each score. This problem may not be solved by a brute-force approach, as the number of paths blows up quickly. 

# solution
## synopsis
To generate the path vs step distributions for all scores, we first need this same distribution for all numbers less than or equal to the threshold. (I suppose we don't really need this data for numbers less than 37, but we'll find it along the way.) The rules determining the paths to a number <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.830040000000002pt height=14.102549999999994pt/> depend on whether or not <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.830040000000002pt height=14.102549999999994pt/> is greater than the ''critical point'' <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/11f29671c9a023d84560a9a7ca22d779.svg?invert_in_darkmode" align=middle width=15.682755000000002pt height=14.102549999999994pt/>.

\[ n_c = T - A + 1 \]

where T is the threshold.


The critical point is the number at which, when reached in a path, A switches to 1. Equivalently, it is the highest number which may not be reached by a path that includes 1.

Thus, there are three regions, each with their own rules for choosing paths:



<img src="https://github.com/eeshugerman/sum7die/blob/master/svgs/6ef6232f98cea5faa9ac83829cfea318.svg?invert_in_darkmode" align=middle width=65.259975pt height=24.56552999999997pt/>

<img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/138644dfd1adcf3497eaa74a981ebaa8.svg?invert_in_darkmode" align=middle width=67.296735pt height=24.56552999999997pt/>

<img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/c4a38fa577a79d548a77db6057a23263.svg?invert_in_darkmode" align=middle width=98.18952pt height=24.56552999999997pt/>


For each region, a function is defined to generate the path vs step distributions for numbers in the region. The results for region <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode" align=middle width=8.656725000000002pt height=14.102549999999994pt/> are used to compute the results for <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/4bdc8d9bcfb35e1c9bfb51fc69687dfc.svg?invert_in_darkmode" align=middle width=7.028488500000004pt height=22.745910000000016pt/>, the results for <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode" align=middle width=8.656725000000002pt height=14.102549999999994pt/> and <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/4bdc8d9bcfb35e1c9bfb51fc69687dfc.svg?invert_in_darkmode" align=middle width=7.028488500000004pt height=22.745910000000016pt/> are used to compute the results for <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode" align=middle width=7.087278000000003pt height=14.102549999999994pt/>. These functions are described in section 2.2.

Once the path vs step distributions are calculated for region <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode" align=middle width=7.087278000000003pt height=14.102549999999994pt/>, the problem is nearly solved. But one final bit of insight is required: the probability that a path will be traversed is not equal for all paths. When a single path branches into two, the relative probability that either child branch will be traversed is <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/d5d5564ce0bb9999695f32da6ba7af42.svg?invert_in_darkmode" align=middle width=24.56553pt height=24.56552999999997pt/> to the parent's 1; a second branching will create paths with probability <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/5b86d915fa363500989d7ece86014d29.svg?invert_in_darkmode" align=middle width=31.093590000000003pt height=26.70657pt/>. In our case, 7 branches diverge each step of the way, so the relative probability that a path with <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/6f9bad7347b91ceebebd3ad7e6f6f2d1.svg?invert_in_darkmode" align=middle width=7.676740500000004pt height=14.102549999999994pt/> steps will be traversed is <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/af90f00d3127ec87bada29ec3726e088.svg?invert_in_darkmode" align=middle width=30.58176pt height=26.70657pt/>. Thus, we must scale the path vs step distributions for each score in the following manner:

\[ p_t(s) = (1 / s^2)p_e(x) \]

where <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/fb71038316827ef9d7cbe35f7b614d4c.svg?invert_in_darkmode" align=middle width=13.186965000000002pt height=14.102549999999994pt/> is the (un-normalized) distribution of paths \textit{actually taken} and <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/4235d7a9f2ef9e47837093380da6376a.svg?invert_in_darkmode" align=middle width=14.453340000000003pt height=14.102549999999994pt/> is the distribution of paths which \textit{exist} or \textit{could be taken}.

Finally, we can now construct our score distribution. The relative probability for each score is the sum of the corresponding <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/fb71038316827ef9d7cbe35f7b614d4c.svg?invert_in_darkmode" align=middle width=13.186965000000002pt height=14.102549999999994pt/>.

## Counting functions

First, some notation:


Let <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/138e3040a04be5fff2963b435b67c923.svg?invert_in_darkmode" align=middle width=25.728780000000004pt height=24.56552999999997pt/> denote the number of paths to <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.830040000000002pt height=14.102549999999994pt/>, with gumballs drawn from <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/3cf4fbd05970446973fc3d9fa3fe3c41.svg?invert_in_darkmode" align=middle width=8.398995000000005pt height=14.102549999999994pt/>. <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/3cf4fbd05970446973fc3d9fa3fe3c41.svg?invert_in_darkmode" align=middle width=8.398995000000005pt height=14.102549999999994pt/> is <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/1b16165ec13522209f4bb000597661b0.svg?invert_in_darkmode" align=middle width=133.13767499999997pt height=24.56552999999997pt/>, <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/51132181a078db5176cb6fc6509a7c02.svg?invert_in_darkmode" align=middle width=145.12971000000002pt height=24.56552999999997pt/>, or <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/3686a69eb488dedb301218b9f7cd832f.svg?invert_in_darkmode" align=middle width=156.730365pt height=24.56552999999997pt/>.



Let <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/e56c228e9cc317db54aad972ab7f99e9.svg?invert_in_darkmode" align=middle width=18.92847pt height=24.56552999999997pt/> (no subscript) denote the number of paths to <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/e56c228e9cc317db54aad972ab7f99e9.svg?invert_in_darkmode" align=middle width=18.92847pt height=24.56552999999997pt/>, given the rules of the gumball game (i.e., the values we are looking for).



Note: The algorithms below merely count the number of paths to a number n. However, the number of paths \textit{for each path length} is required to solve the problem. The functions in the python code are essentially equivalent to those here, except instead of returning a single number, they return a distribution as a dict, with number of steps as keys and number of paths as values. These functions call each other (or lookup data computed by the others). When the dict [n] is computed as a sum, and [m] is an elelement in this sum, the value <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/21f4687e6d54c9fdbda51c0e7f3aa78e.svg?invert_in_darkmode" align=middle width=160.00759499999998pt height=24.56552999999997pt/> is added to (the accumulator for) <img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/ff84d120c6d5a359939d87740cff47f3.svg?invert_in_darkmode" align=middle width=183.690045pt height=24.56552999999997pt/>.\\ 

### region a



\[
	[n] = \sum_{i=0}^{\vert H \vert}
		<p align="center"><img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/c8e46703012914262fdcd5df28ef1742.svg?invert_in_darkmode" align=middle width=183.3282pt height=68.9865pt/></p>
\]

### region b


\[
	[n] = \sum_{i=0}^{\vert H \vert}
		<p align="center"><img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/c8e46703012914262fdcd5df28ef1742.svg?invert_in_darkmode" align=middle width=183.3282pt height=68.9865pt/></p>
\]

### region c


\[
	[n] = \sum_{i=0}^{\vert L \vert}
		<p align="center"><img src="https://rawgit.com/eeshugerman/sum7die/None/svgs/a686da01134a7dff040d8550eabed055.svg?invert_in_darkmode" align=middle width=180.67005pt height=49.131389999999996pt/></p>
\]
