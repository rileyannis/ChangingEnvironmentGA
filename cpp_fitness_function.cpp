#include<vector>
using std::vector;
#include<numeric>
using std::accumulate;
#include<cmath>
using std::pow; using std::sqrt; using std::sin; using std::cos; using std::abs;

float cpp_flat_function(vector<float> vals){
  return 0.0;
}

float inline adding_squares(float tot, float val){
  return tot + (val*val);
}

float cpp_sphere_function(vector<float> vals){
  return accumulate(vals.begin(), vals.end(), 0.0, adding_squares);
}

float cpp_rosenbrock_function(vector<float> vals){
  float tot = 0.0;
  for(int i = 0; i < (vals.size() - 1); ++i){
    tot += (100.0 * pow(vals[i+1] - (pow(vals[i], 2)), 2) + pow(vals[i] - 1, 2));
  }
  return tot;
}

vector<float> cpp_initialize_rana_weights(vector<float> vals){
  //Will actually fix later/probably never use
  vector<float> vec;
  return vec;
}

float cpp_rana_function(vector<float> vals, vector<float> weights){
  float tot = 0.0, x, y;
  for(int i = 0; i < vals.size(); ++i){
    x = vals[i];
    if(i == (vals.size() - 1)){
      y = vals[0];
    }
    else{
      y = vals[i + 1];
    }
    tot += weights[i] * x * sin(sqrt(abs(y + 1 - x))) * cos(sqrt(abs(x + y + 1)))
      + (y + 1) * cos(sqrt(abs(y + 1 - x))) * sin(sqrt(abs(x + y + 1)));
  }
  return tot;
}

float cpp_schafferF7(vector<float> vals){
  float tot = 0.0, norm = 1.0/vals.size(), si;
  for(int i = 0; i < (vals.size() - 1); ++i){
    si = sqrt(pow(vals[i], 2) + pow(vals[i + 1], 2));
    tot += pow(norm * sqrt(si) * (sin(50 * pow(si, 0.20)) + 1), 2);
  }
  return tot;
}

float cpp_deceptive(vector<float> vals){
  float decep = 0.20, best = 1.0, decep_best = 0.7, tot = 0.0;
  int dim = vals.size();
  for(int i = 0; i < dim; ++i){
    if(vals[i] < decep){
      tot += vals[i] * (-1.0 / decep) + best;
    }
    else{
      tot += (vals[i] - decep) * (decep_best / (1.0 - decep));
    }
  }
  return tot / dim;
}
