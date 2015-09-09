#include<vector>
using std::vector;
#include<numeric>
using std::accumulate;
#include<cmath>
using std::pow; using std::sqrt; using std::sin; using std::cos; using std::abs;

//This was just for testing arrays
double add_array(double* ary, int sz){
  double sum = 0;
  for(int i = 0; i < sz; ++i){
    sum += ary[i];
  }
  return sum;
}

float inline adding_squares(float tot, float val){
  //Inline function made for accumulate in sphere_function
  return tot + (val*val);
}

float cpp_sphere(double* vals, long sz){
  //Accumulates the squares of all vals
  return accumulate(vals, vals + sz, 0.0, adding_squares);
}

float cpp_rosenbrock(double* vals, long sz){
  //The rosenbrock function! It does things!
  double tot = 0.0, adjusted_val, adjusted_next = vals[0] * 0.004;
  for(long i = 0; i < (sz - 1); ++i){
    adjusted_val = adjusted_next;
    adjusted_next = vals[i + 1] * 0.004;
    tot += (100.0 * pow(adjusted_next - (pow(adjusted_val, 2)), 2) + pow(adjusted_val - 1, 2));
  }
  return tot;
}

float cpp_rana(double* vals, long sz, double* weights){
  //The rana function! It does more things! Wow!
  double tot = 512.0, x, y;
  for(long i = 0; i < sz; ++i){
    x = vals[i];
    if(i == (sz - 1)){
      y = vals[0];
    }
    else{
      y = vals[i + 1];
    }
    tot += weights[i] * (x * sin(sqrt(abs(y + 1 - x))) * cos(sqrt(abs(x + y + 1)))
			 + (y + 1) * cos(sqrt(abs(y + 1 - x))) * sin(sqrt(abs(x + y + 1))));
  }
  return tot;
}

float cpp_schafferf7(double* vals, long sz){
  //The schafferf7 function! It does other things!
  double tot = 0.0, norm = 1.0/sz, si, adjusted_val, adjusted_next = vals[0] / 512.0 * 100.0;
  for(long i = 0; i < (sz - 1); ++i){
    adjusted_val = adjusted_next;
    adjusted_next = vals[i + 1] / 512.0 * 100.0;
    si = sqrt(pow(adjusted_val, 2) + pow(adjusted_next, 2));
    tot += pow(norm * sqrt(si) * (sin(50 * pow(si, 0.20)) + 1), 2);
  }
  return tot;
}

float cpp_deceptive(double* vals, long sz){
  //The deceptive function. It does stuff.
  double decep = 0.2, best = 1.0, decep_best = 0.7, tot = 1.0, adjusted_val;
  for(long i = 0; i < sz; ++i){
    adjusted_val = (vals[i] + 512.0) / 1024.0;
    if(adjusted_val < decep){
      tot -= (adjusted_val * (-1.0 / decep) + best);
    }
    else{
      tot -= ((adjusted_val - decep) * (decep_best / (1.0 - decep)));
    }
  }
  return tot / sz;
}

float inline schwefel_sum(float tot, float val){
  //Inline function for the sum portion of the schwefel function
  return tot + (-1 * val * sin(sqrt(abs(val))));
}

float cpp_schwefel(double* vals, long sz){
  //The schwefel function. This is new!
  double alpha = 418.982887;
  return accumulate(vals, vals + sz, alpha * sz, schwefel_sum);
}
