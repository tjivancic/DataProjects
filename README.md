# Storm Builder

Storm Builder is a small python package designed to take an existing storm (as a folder of nc files or as a three dimensional numpy array [t,x,y]) and replicate its fractal structure and precipitation volume while redistributing precipitaion both spatially and temporally resulting in a new realistic storm.

This code was designed with two specific examples in mind but can likely to be extended to answer a number of other questions
1) When calculating flood risk it is standard practice to design based on a single 'design storm', namely the worst observed precipitation event in an area. By using Storm Builder, it is possible to generate any number of possible design storms.
2) Streamflow and flood forecasting often takes advantage of ensemble weather forecasts to determine the likelihood of different flow conditions. This is done by forcing a hydrologic model with a number of weather forecasts. However, due to the computational expense of weather models there are often a limited number of ensemble members. Storm Builder can be used to take a low likelihood but high impact ensemble member and give a number of possible scenarios that can be used to asses the danger to a specific watershed.
